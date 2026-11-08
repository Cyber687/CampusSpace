from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, time
from pathlib import Path
from typing import Optional
import csv, io, sqlite3, uuid

from fastapi import FastAPI, HTTPException, Depends, Header, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

from backend.config import settings, ROOT_DIR
from backend.security import hash_password, verify_password, create_token, decode_token


def connect():
    if not settings.database_path.exists():
        raise HTTPException(503, "Database not initialized. Run: python scripts/init_db.py")
    conn = sqlite3.connect(settings.database_path, timeout=20, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def dictrow(row): return dict(row) if row is not None else None

def now_sql(): return datetime.now().replace(microsecond=0).isoformat(sep=" ")

def ensure_expired(conn):
    now = now_sql()
    conn.execute("UPDATE canteen_visits SET status='Expired' WHERE status='Active' AND expires_at <= ?", (now,))
    conn.execute("UPDATE fault_reports SET status='Escalated to Higher Authority', is_escalated=1, updated_at=? WHERE status IN ('Submitted','In Progress') AND created_at <= datetime('now','-7 days') AND is_escalated=0", (now,))

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", description="CampusSpace campus assistance and resource management MVP", lifespan=lifespan)

# UPDATED CORS FOR MOBILE BROWSERS
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=False,  # Must be False for mobile to allow wildcard origins
    allow_methods=["*"], 
    allow_headers=["*"]
)

FRONTEND = ROOT_DIR / "frontend"
if FRONTEND.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    department: str = Field(min_length=2, max_length=80)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class VerificationIn(BaseModel):
    reported_status: str

class FaultIn(BaseModel):
    category: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=5, max_length=2000)
    classroom_id: Optional[int] = None
    canteen_id: Optional[int] = None
    is_urgent: bool = False

class FaultUpdateIn(BaseModel):
    status: str
    note: str = ""
    assigned_to_user_id: Optional[int] = None

class CheckinIn(BaseModel):
    qr_identifier: str

class BookingIn(BaseModel):
    starts_at: datetime
    ends_at: datetime
    purpose: str = Field(default="Study", max_length=120)

class UserUpdateIn(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    is_active: Optional[bool] = None


def current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Sign in to continue")
    payload = decode_token(authorization.split(" ",1)[1], settings.jwt_secret_key)
    if not payload: raise HTTPException(401, "Session is invalid or expired")
    conn = connect()
    try:
        row = conn.execute("SELECT u.*, c.department, c.is_active FROM users u JOIN user_credentials c ON c.user_id=u.id WHERE u.id=?", (int(payload["sub"]),)).fetchone()
        if not row or not row["is_active"]: raise HTTPException(401, "Account is unavailable")
        return dictrow(row)
    finally: conn.close()


def roles(*allowed):
    def check(user=Depends(current_user)):
        if user["role"] not in allowed: raise HTTPException(403, "You do not have permission for this action")
        return user
    return check


def audit(conn, user_id, action, entity, entity_id=None):
    conn.execute("INSERT INTO admin_audit_log(actor_user_id,action,entity,entity_id) VALUES(?,?,?,?)", (user_id, action, entity, str(entity_id) if entity_id is not None else None))

@app.get("/")
def root(): return {"app": settings.app_name, "status": "running", "docs": "/docs", "frontend": "/static/index.html"}

@app.get("/health/live")
def health(): return {"status":"ok", "app":settings.app_name}

@app.get("/api/v1/health")
def api_health(): return {"status":"ok"}

@app.post("/api/v1/auth/register", status_code=201)
def register(data: RegisterIn):
    conn = connect()
    try:
        if conn.execute("SELECT 1 FROM users WHERE lower(email)=lower(?)", (data.email,)).fetchone(): raise HTTPException(409, "An account with this email already exists. Please sign in.")
        cur = conn.execute("INSERT INTO users(full_name,email,role,escalation_authority) VALUES(?,?, 'student',0)", (data.full_name.strip(), data.email.lower()))
        uid = cur.lastrowid
        conn.execute("INSERT INTO user_credentials(user_id,password_hash,department) VALUES(?,?,?)", (uid, hash_password(data.password), data.department.strip()))
        conn.commit()
        return {"message":"Account created. You can now sign in.", "user_id":uid}
    finally: conn.close()

@app.post("/api/v1/auth/login")
def login(data: LoginIn):
    conn = connect()
    try:
        row = conn.execute("SELECT u.*,c.password_hash,c.department,c.is_active FROM users u JOIN user_credentials c ON c.user_id=u.id WHERE lower(u.email)=lower(?)", (data.email,)).fetchone()
        if not row or not row["is_active"] or not verify_password(data.password, row["password_hash"]): raise HTTPException(401, "Email or password is incorrect")
        token = create_token(row["id"], row["role"], settings.jwt_secret_key, settings.token_expire_minutes)
        return {"access_token":token,"token_type":"bearer","user":{"id":row["id"],"full_name":row["full_name"],"email":row["email"],"role":row["role"],"department":row["department"]}}
    finally: conn.close()

@app.get("/api/v1/auth/me")
def me(user=Depends(current_user)):
    return {k:user[k] for k in ("id","full_name","email","role","department","escalation_authority")}

@app.get("/api/v1/blocks")
def blocks(user=Depends(current_user)):
    conn=connect()
    try: return [dictrow(r) for r in conn.execute("SELECT b.*, (SELECT COUNT(*) FROM floors f WHERE f.block_id=b.id) floor_count, (SELECT COUNT(*) FROM classrooms c JOIN floors f ON f.id=c.floor_id WHERE f.block_id=b.id) classroom_count FROM blocks b ORDER BY b.id")]
    finally: conn.close()

@app.get("/api/v1/classrooms")
def classrooms(block_id: Optional[int]=None, floor_number: Optional[int]=None, search: Optional[str]=None, ac: bool=False, quiet: bool=False, user=Depends(current_user)):
    sql="SELECT c.*,f.floor_number,b.id block_id,b.name block_name,b.code block_code FROM classrooms c JOIN floors f ON f.id=c.floor_id JOIN blocks b ON b.id=f.block_id WHERE 1=1"
    args=[]
    if block_id: sql+=" AND b.id=?"; args.append(block_id)
    if floor_number: sql+=" AND f.floor_number=?"; args.append(floor_number)
    if search: sql+=" AND (c.room_number LIKE ? OR b.name LIKE ?)"; args.extend([f"%{search}%",f"%{search}%"])
    if quiet: sql+=" AND c.is_quiet_zone=1"
    sql+=" ORDER BY b.id,f.floor_number,c.room_number LIMIT 500"
    conn=connect()
    try:
        rows=[dictrow(r) for r in conn.execute(sql,args)]
        for room in rows:
            room["amenities"]={"ac_count":room["ac_count"],"student_sockets":room["student_sockets"],"faculty_sockets":room["faculty_sockets"],"quiet_zone":bool(room["is_quiet_zone"])}
            room["availability"] = _room_status(conn, room["id"])
        return rows
    finally: conn.close()

def _room_status(conn, classroom_id):
    now=datetime.now(); day=now.strftime("%A"); current=now.strftime("%H:%M:%S")
    scheduled=conn.execute("SELECT subject_name,start_time,end_time FROM timetable_entries WHERE classroom_id=? AND day_of_week=? AND is_break_slot=0 AND start_time<=? AND end_time>?",(classroom_id,day,current,current)).fetchone()
    if scheduled: return {"status":"Scheduled class","confidence":"high","detail":scheduled["subject_name"]}
    ver=conn.execute("SELECT reported_status,reported_at FROM classroom_verifications WHERE classroom_id=? ORDER BY reported_at DESC LIMIT 1",(classroom_id,)).fetchone()
    if ver:
        try: age=(now-datetime.fromisoformat(ver["reported_at"])).total_seconds()/60
        except Exception: age=99999
        if age <= settings.verification_ttl_minutes:
            return {"status":ver["reported_status"],"confidence":"recent report","reported_at":ver["reported_at"]}
    booking=conn.execute("SELECT id FROM classroom_bookings WHERE classroom_id=? AND status='Active' AND starts_at<=? AND ends_at>? LIMIT 1",(classroom_id,now.isoformat(sep=" "),now.isoformat(sep=" "))).fetchone()
    if booking: return {"status":"Booked","confidence":"high"}
    return {"status":"No scheduled class","confidence":"unconfirmed","detail":"Timetable slot is empty; physical vacancy is not confirmed."}

@app.get("/api/v1/classrooms/available")
def available_classrooms(block_id: Optional[int]=None, floor_number: Optional[int]=None, search: Optional[str]=None, user=Depends(current_user)):
    all_rooms=classrooms(block_id=block_id,floor_number=floor_number,search=search,user=user)
    return [r for r in all_rooms if r["availability"]["status"] in ("No scheduled class","Reported Available")]

@app.get("/api/v1/classrooms/{classroom_id}")
def classroom_detail(classroom_id:int,user=Depends(current_user)):
    conn=connect()
    try:
        row=conn.execute("SELECT c.*,f.floor_number,b.name block_name,b.code block_code FROM classrooms c JOIN floors f ON f.id=c.floor_id JOIN blocks b ON b.id=f.block_id WHERE c.id=?",(classroom_id,)).fetchone()
        if not row: raise HTTPException(404,"Classroom not found")
        result=dictrow(row); result["availability"]=_room_status(conn,classroom_id)
        result["timetable"]=[dictrow(r) for r in conn.execute("SELECT * FROM timetable_entries WHERE classroom_id=? ORDER BY day_of_week,start_time",(classroom_id,))]
        result["open_faults"]=[dictrow(r) for r in conn.execute("SELECT id,ticket_id,category,status,is_urgent FROM fault_reports WHERE classroom_id=? AND status!='Completed'",(classroom_id,))]
        return result
    finally: conn.close()

@app.post("/api/v1/classrooms/{classroom_id}/verifications",status_code=201)
def verify_classroom(classroom_id:int,data:VerificationIn,user=Depends(current_user)):
    allowed={"Reported Available","Reported Occupied","Restricted"}
    if data.reported_status not in allowed: raise HTTPException(422,f"reported_status must be one of {sorted(allowed)}")
    conn=connect()
    try:
        if not conn.execute("SELECT 1 FROM classrooms WHERE id=?",(classroom_id,)).fetchone(): raise HTTPException(404,"Classroom not found")
        cur=conn.execute("INSERT INTO classroom_verifications(classroom_id,user_id,reported_status,reported_at) VALUES(?,?,?,?)",(classroom_id,user["id"],data.reported_status,now_sql()))
        conn.commit(); return {"id":cur.lastrowid,"classroom_id":classroom_id,"reported_status":data.reported_status,"reported_at":now_sql(),"expires_in_minutes":settings.verification_ttl_minutes}
    finally: conn.close()

@app.post("/api/v1/classrooms/{classroom_id}/bookings",status_code=201)
def book_classroom(classroom_id:int,data:BookingIn,user=Depends(current_user)):
    if data.ends_at <= data.starts_at: raise HTTPException(422,"End time must be after start time")
    conn=connect()
    try:
        if not conn.execute("SELECT 1 FROM classrooms WHERE id=?",(classroom_id,)).fetchone(): raise HTTPException(404,"Classroom not found")
        day=data.starts_at.strftime("%A")
        conflict=conn.execute("SELECT 1 FROM timetable_entries WHERE classroom_id=? AND day_of_week=? AND is_break_slot=0 AND start_time < ? AND end_time > ?",(classroom_id,day,data.ends_at.strftime("%H:%M:%S"),data.starts_at.strftime("%H:%M:%S"))).fetchone()
        if conflict: raise HTTPException(409,"Classroom has a scheduled class during this period")
        overlap=conn.execute("SELECT 1 FROM classroom_bookings WHERE classroom_id=? AND status='Active' AND starts_at < ? AND ends_at > ?",(classroom_id,data.ends_at.isoformat(sep=" "),data.starts_at.isoformat(sep=" "))).fetchone()
        if overlap: raise HTTPException(409,"Classroom is already booked for this period")
        cur=conn.execute("INSERT INTO classroom_bookings(classroom_id,user_id,starts_at,ends_at,purpose) VALUES(?,?,?,?,?)",(classroom_id,user["id"],data.starts_at.isoformat(sep=" "),data.ends_at.isoformat(sep=" "),data.purpose))
        conn.commit(); return {"id":cur.lastrowid,"message":"Classroom booking created","starts_at":data.starts_at,"ends_at":data.ends_at}
    finally: conn.close()

@app.get("/api/v1/canteens")
def canteens(user=Depends(current_user)):
    conn=connect()
    try:
        ensure_expired(conn); conn.commit()
        rows=conn.execute("SELECT ca.*,b.name block_name,f.floor_number FROM canteens ca JOIN blocks b ON b.id=ca.block_id JOIN floors f ON f.id=ca.floor_id ORDER BY b.id").fetchall()
        result=[]
        for r in rows:
            d=dictrow(r); count=conn.execute("SELECT COUNT(*) n FROM canteen_visits WHERE canteen_id=? AND status='Active' AND expires_at>? AND check_out_time IS NULL",(r["id"],now_sql())).fetchone()["n"]
            pct=count/max(1,r["capacity"]); d["active_registrations"]=count; d["crowd_level"]="High" if pct>=.7 else ("Medium" if pct>=.35 else "Low"); d["estimate_note"]="QR registrations estimate crowd; they are not a physical headcount."; result.append(d)
        return result
    finally: conn.close()

@app.post("/api/v1/canteens/check-in",status_code=201)
def canteen_checkin(data:CheckinIn,user=Depends(current_user)):
    conn=connect()
    try:
        ensure_expired(conn)
        canteen=conn.execute("SELECT * FROM canteens WHERE qr_code_identifier=? OR code=?",(data.qr_identifier,data.qr_identifier)).fetchone()
        if not canteen: raise HTTPException(404,"Unknown canteen QR identifier")
        existing=conn.execute("SELECT * FROM canteen_visits WHERE canteen_id=? AND user_id=? AND status='Active' AND expires_at>? AND check_out_time IS NULL ORDER BY id DESC LIMIT 1",(canteen["id"],user["id"],now_sql())).fetchone()
        if existing:
            conn.commit(); return {"visit":dictrow(existing),"message":"You already have an active visit at this canteen."}
        duration=int(canteen["default_visit_duration_min"] or settings.default_canteen_visit_minutes)
        start=datetime.now().replace(microsecond=0); expiry=start+timedelta(minutes=duration)
        cur=conn.execute("INSERT INTO canteen_visits(canteen_id,user_id,check_in_time,expires_at,status) VALUES(?,?,?,?,'Active')",(canteen["id"],user["id"],start.isoformat(sep=" "),expiry.isoformat(sep=" ")))
        conn.commit(); return {"visit_id":cur.lastrowid,"canteen":canteen["name"],"check_in_time":start,"expires_at":expiry,"duration_minutes":duration,"message":"Check-in confirmed. Crowd count is an estimate."}
    finally: conn.close()

@app.get("/api/v1/canteen-visits/mine")
def my_visits(user=Depends(current_user)):
    conn=connect()
    try:
        ensure_expired(conn); conn.commit()
        return [dictrow(r) for r in conn.execute("SELECT v.*,c.name canteen_name,c.code canteen_code FROM canteen_visits v JOIN canteens c ON c.id=v.canteen_id WHERE v.user_id=? ORDER BY v.id DESC LIMIT 100",(user["id"],))]
    finally: conn.close()

@app.post("/api/v1/canteen-visits/{visit_id}/checkout")
def checkout(visit_id:int,user=Depends(current_user)):
    conn=connect()
    try:
        row=conn.execute("SELECT * FROM canteen_visits WHERE id=?",(visit_id,)).fetchone()
        if not row: raise HTTPException(404,"Visit not found")
        if row["user_id"] != user["id"] and user["role"] not in ("admin",): raise HTTPException(403,"You can only check out your own visit")
        if row["status"]=="Active": conn.execute("UPDATE canteen_visits SET status='Checked Out',check_out_time=? WHERE id=?",(now_sql(),visit_id)); conn.commit()
        return {"message":"Visit checked out","visit_id":visit_id}
    finally: conn.close()

@app.get("/api/v1/fault-reports")
def fault_reports(status:Optional[str]=None, mine:bool=False, user=Depends(current_user)):
    conn=connect()
    try:
        ensure_expired(conn); conn.commit()
        sql="SELECT fr.*,u.full_name reporter_name,c.room_number,b.name block_name FROM fault_reports fr JOIN users u ON u.id=fr.reported_by_user_id LEFT JOIN classrooms c ON c.id=fr.classroom_id LEFT JOIN floors f ON f.id=c.floor_id LEFT JOIN blocks b ON b.id=f.block_id WHERE 1=1"; args=[]
        if mine or user["role"]=="student": sql+=" AND fr.reported_by_user_id=?"; args.append(user["id"])
        if status: sql+=" AND fr.status=?"; args.append(status)
        sql+=" ORDER BY fr.is_urgent DESC,fr.created_at DESC"
        return [dictrow(r) for r in conn.execute(sql,args)]
    finally: conn.close()

@app.post("/api/v1/fault-reports",status_code=201)
def create_fault(data:FaultIn,user=Depends(current_user)):
    if not data.classroom_id and not data.canteen_id: raise HTTPException(422,"Select a classroom or canteen location")
    conn=connect()
    try:
        if data.classroom_id and not conn.execute("SELECT 1 FROM classrooms WHERE id=?",(data.classroom_id,)).fetchone(): raise HTTPException(404,"Classroom not found")
        if data.canteen_id and not conn.execute("SELECT 1 FROM canteens WHERE id=?",(data.canteen_id,)).fetchone(): raise HTTPException(404,"Canteen not found")
        dup=conn.execute("SELECT ticket_id FROM fault_reports WHERE category=? AND COALESCE(classroom_id,0)=COALESCE(?,0) AND COALESCE(canteen_id,0)=COALESCE(?,0) AND status IN ('Submitted','In Progress','Escalated to Higher Authority') AND created_at >= datetime('now','-24 hours') LIMIT 1",(data.category,data.classroom_id,data.canteen_id)).fetchone()
        if dup: return {"message":"A similar open report already exists; please follow its ticket.","ticket_id":dup["ticket_id"],"possible_duplicate":True}
        ticket="CS-"+datetime.now().strftime("%y%m%d")+"-"+uuid.uuid4().hex[:6].upper()
        cur=conn.execute("INSERT INTO fault_reports(ticket_id,classroom_id,canteen_id,reported_by_user_id,category,description,is_urgent,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",(ticket,data.classroom_id,data.canteen_id,user["id"],data.category,data.description,int(data.is_urgent),now_sql(),now_sql()))
        conn.execute("INSERT INTO maintenance_updates(fault_report_id,actor_user_id,status,note) VALUES(?,?,?,?)",(cur.lastrowid,user["id"],"Submitted","Report received"))
        conn.commit(); return {"id":cur.lastrowid,"ticket_id":ticket,"status":"Submitted","is_urgent":data.is_urgent,"message":"Fault report submitted successfully"}
    finally: conn.close()

@app.get("/api/v1/fault-reports/{report_id}")
def fault_detail(report_id:int,user=Depends(current_user)):
    conn=connect()
    try:
        row=conn.execute("SELECT * FROM fault_reports WHERE id=? OR ticket_id=?",(report_id,str(report_id))).fetchone()
        if not row: raise HTTPException(404,"Report not found")
        if user["role"]=="student" and row["reported_by_user_id"]!=user["id"]: raise HTTPException(403,"You can only view your own reports")
        result=dictrow(row); result["updates"]=[dictrow(r) for r in conn.execute("SELECT m.*,u.full_name actor_name FROM maintenance_updates m LEFT JOIN users u ON u.id=m.actor_user_id WHERE fault_report_id=? ORDER BY m.id",(row["id"],))]
        return result
    finally: conn.close()

@app.patch("/api/v1/fault-reports/{report_id}")
def update_fault(report_id:int,data:FaultUpdateIn,user=Depends(roles("maintenance","admin"))):
    allowed={"Submitted","In Progress","Completed","Escalated to Higher Authority"}
    if data.status not in allowed: raise HTTPException(422,f"status must be one of {sorted(allowed)}")
    conn=connect()
    try:
        row=conn.execute("SELECT * FROM fault_reports WHERE id=?",(report_id,)).fetchone()
        if not row: raise HTTPException(404,"Report not found")
        if data.assigned_to_user_id and user["role"]!="admin": raise HTTPException(403,"Only administrators can assign staff")
        conn.execute("UPDATE fault_reports SET status=?,updated_at=?,assigned_to_user_id=COALESCE(?,assigned_to_user_id),is_escalated=CASE WHEN ?='Escalated to Higher Authority' THEN 1 ELSE is_escalated END WHERE id=?",(data.status,now_sql(),data.assigned_to_user_id,data.status,report_id))
        conn.execute("INSERT INTO maintenance_updates(fault_report_id,actor_user_id,status,note) VALUES(?,?,?,?)",(report_id,user["id"],data.status,data.note[:1000]))
        conn.commit(); return {"message":"Report updated","id":report_id,"status":data.status}
    finally: conn.close()

@app.get("/api/v1/maintenance/summary")
def maintenance_summary(user=Depends(roles("maintenance","admin"))):
    conn=connect()
    try:
        ensure_expired(conn); conn.commit()
        return {r["status"]:r["n"] for r in conn.execute("SELECT status,COUNT(*) n FROM fault_reports GROUP BY status")}
    finally: conn.close()

@app.get("/api/v1/admin/users")
def admin_users(user=Depends(roles("admin"))):
    conn=connect()
    try: return [dictrow(r) for r in conn.execute("SELECT u.id,u.full_name,u.email,u.role,u.escalation_authority,c.department,c.is_active,c.created_at FROM users u JOIN user_credentials c ON c.user_id=u.id ORDER BY u.id")]
    finally: conn.close()

class AdminUserCreateIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    department: str = Field(min_length=2, max_length=80)
    role: str = "admin"

@app.post("/api/v1/admin/users", status_code=201)
def admin_create_user(data: AdminUserCreateIn, user=Depends(roles("admin"))):
    if data.role not in ("student", "maintenance", "admin"):
        raise HTTPException(422, "Role must be student, maintenance, or admin")
    conn=connect()
    try:
        if conn.execute("SELECT 1 FROM users WHERE lower(email)=lower(?)", (str(data.email),)).fetchone():
            raise HTTPException(409, "An account with this email already exists")
        cur=conn.execute(
            "INSERT INTO users(full_name,email,role,escalation_authority) VALUES(?,?,?,?)",
            (data.full_name.strip(), str(data.email).lower(), data.role, 1 if data.role == "admin" else 0),
        )
        uid=cur.lastrowid
        conn.execute(
            "INSERT INTO user_credentials(user_id,password_hash,department) VALUES(?,?,?)",
            (uid, hash_password(data.password), data.department.strip()),
        )
        audit(conn, user["id"], "create_user", "users", uid)
        conn.commit()
        return {"message":"User created", "user_id":uid, "email":str(data.email).lower(), "role":data.role}
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise HTTPException(409, "Could not create user; the email may already be in use") from e
    finally:
        conn.close()

@app.patch("/api/v1/admin/users/{user_id}")
def admin_update_user(user_id:int,data:UserUpdateIn,user=Depends(roles("admin"))):
    if data.role and data.role not in ("student","maintenance","admin"): raise HTTPException(422,"Invalid role")
    conn=connect()
    try:
        row=conn.execute("SELECT * FROM users WHERE id=?",(user_id,)).fetchone()
        if not row: raise HTTPException(404,"User not found")
        for key in ("full_name","email","role"):
            value=getattr(data,key)
            if value is not None: conn.execute(f"UPDATE users SET {key}=? WHERE id=?",(str(value).lower() if key=="email" else value,user_id))
        if data.department is not None: conn.execute("UPDATE user_credentials SET department=? WHERE user_id=?",(data.department,user_id))
        if data.password: conn.execute("UPDATE user_credentials SET password_hash=? WHERE user_id=?",(hash_password(data.password),user_id))
        if data.is_active is not None: conn.execute("UPDATE user_credentials SET is_active=? WHERE user_id=?",(int(data.is_active),user_id))
        audit(conn,user["id"],"update_user","users",user_id); conn.commit(); return {"message":"User updated"}
    except sqlite3.IntegrityError as e: raise HTTPException(409,"Email address is already in use") from e
    finally: conn.close()

@app.delete("/api/v1/admin/users/{user_id}")
def admin_delete_user(user_id:int,user=Depends(roles("admin"))):
    if user_id==user["id"]: raise HTTPException(400,"You cannot delete your own active admin account")
    conn=connect()
    try:
        if not conn.execute("SELECT 1 FROM users WHERE id=?",(user_id,)).fetchone(): raise HTTPException(404,"User not found")
        audit(conn,user["id"],"delete_user","users",user_id); conn.execute("DELETE FROM users WHERE id=?",(user_id,)); conn.commit(); return {"message":"User deleted"}
    finally: conn.close()

@app.get("/api/v1/admin/overview")
def admin_overview(user=Depends(roles("admin"))):
    conn=connect()
    try:
        ensure_expired(conn); conn.commit()
        scalar=lambda q: conn.execute(q).fetchone()[0]
        return {"blocks":scalar("SELECT COUNT(*) FROM blocks"),"floors":scalar("SELECT COUNT(*) FROM floors"),"classrooms":scalar("SELECT COUNT(*) FROM classrooms"),"canteens":scalar("SELECT COUNT(*) FROM canteens"),"users":scalar("SELECT COUNT(*) FROM users"),"open_faults":scalar("SELECT COUNT(*) FROM fault_reports WHERE status!='Completed'"),"urgent_faults":scalar("SELECT COUNT(*) FROM fault_reports WHERE is_urgent=1 AND status!='Completed'"),"active_canteen_visits":scalar("SELECT COUNT(*) FROM canteen_visits WHERE status='Active' AND expires_at>datetime('now') AND check_out_time IS NULL")}
    finally: conn.close()

@app.get("/api/v1/timetable")
def timetable(classroom_id:Optional[int]=None,day_of_week:Optional[str]=None,user=Depends(current_user)):
    conn=connect()
    try:
        sql="SELECT t.*,c.room_number,b.name block_name,f.floor_number FROM timetable_entries t JOIN classrooms c ON c.id=t.classroom_id JOIN floors f ON f.id=c.floor_id JOIN blocks b ON b.id=f.block_id WHERE 1=1"; args=[]
        if classroom_id: sql+=" AND t.classroom_id=?"; args.append(classroom_id)
        if day_of_week: sql+=" AND lower(t.day_of_week)=lower(?)"; args.append(day_of_week)
        sql+=" ORDER BY t.day_of_week,t.start_time LIMIT 1000"
        return [dictrow(r) for r in conn.execute(sql,args)]
    finally: conn.close()

@app.post("/api/v1/admin/timetable/import")
def import_timetable(file:UploadFile=File(...),user=Depends(roles("admin"))):
    if not file.filename.lower().endswith(".csv"): raise HTTPException(415,"Upload a CSV file")
    content=file.file.read(2_000_001)
    if len(content)>2_000_000: raise HTTPException(413,"CSV file must be under 2 MB")
    try: text=content.decode("utf-8-sig")
    except UnicodeDecodeError: raise HTTPException(400,"CSV must be UTF-8 encoded")
    reader=csv.DictReader(io.StringIO(text)); required={"classroom_id","subject_name","day_of_week","start_time","end_time"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)): raise HTTPException(400,"CSV columns required: classroom_id, subject_name, day_of_week, start_time, end_time; optional is_break_slot")
    conn=connect(); inserted=0
    try:
        for row in reader:
            if not conn.execute("SELECT 1 FROM classrooms WHERE id=?",(row["classroom_id"],)).fetchone(): raise HTTPException(400,f"Unknown classroom_id {row['classroom_id']}")
            conn.execute("INSERT INTO timetable_entries(classroom_id,subject_name,day_of_week,start_time,end_time,is_break_slot) VALUES(?,?,?,?,?,?)",(int(row["classroom_id"]),row["subject_name"],row["day_of_week"].title(),row["start_time"],row["end_time"],int(row.get("is_break_slot") or 0))); inserted+=1
        audit(conn,user["id"],"import_timetable","timetable_entries",inserted); conn.commit(); return {"message":"Timetable imported","rows_inserted":inserted}
    except Exception:
        conn.rollback(); raise
    finally: conn.close()

@app.get("/api/v1/campus/map")
def campus_map(user=Depends(current_user)):
    conn=connect()
    try: return {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":r["id"],"name":r["name"],"code":r["code"],"note":"Coordinates are not configured; map placement is illustrative."},"geometry":None} for r in conn.execute("SELECT * FROM blocks ORDER BY id")]}
    finally: conn.close()
