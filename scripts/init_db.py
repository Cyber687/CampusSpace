from pathlib import Path
import sqlite3, sys
ROOT = Path(__file__).resolve().parents[1]
sql_file = ROOT / "data" / "schema" / "Campus_Space_Dummy_Data.sql"
db_file = ROOT / "data" / "campusspace.db"
ROOT.joinpath("data").mkdir(exist_ok=True)
if db_file.exists():
    if "--reset" not in sys.argv:
        print(f"Database already exists: {db_file}\nUse --reset to rebuild it (this deletes current local data).")
        raise SystemExit(0)
    db_file.unlink()
conn = sqlite3.connect(db_file)
conn.execute("PRAGMA foreign_keys=OFF")
conn.executescript(sql_file.read_text(encoding="utf-8"))
conn.execute("PRAGMA foreign_keys=ON")
conn.executescript("""
CREATE TABLE IF NOT EXISTS user_credentials (
  user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  password_hash TEXT NOT NULL,
  department TEXT NOT NULL DEFAULT 'General',
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS maintenance_updates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fault_report_id INTEGER NOT NULL REFERENCES fault_reports(id) ON DELETE CASCADE,
  actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
  status TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS classroom_bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  classroom_id INTEGER NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  starts_at TEXT NOT NULL,
  ends_at TEXT NOT NULL,
  purpose TEXT NOT NULL DEFAULT 'Study',
  status TEXT NOT NULL DEFAULT 'Active',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS admin_audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_user_id INTEGER,
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")
# Give seeded demo accounts a shared documented password, stored only as PBKDF2 hashes.
sys.path.insert(0, str(ROOT))
from backend.security import hash_password
for row in conn.execute("SELECT id,email,role FROM users").fetchall():
    uid, email, role = row
    department = "Administration" if role == "admin" else ("Facilities" if role == "maintenance" else "Engineering")
    conn.execute("INSERT OR IGNORE INTO user_credentials(user_id,password_hash,department) VALUES(?,?,?)", (uid, hash_password("CampusDemo123!"), department))

# Bootstrap administrator requested for this project. Store only a salted password hash.
bootstrap_email = "anonymous1@campusspace.edu.in"
bootstrap_password = "campusspace1234"
existing = conn.execute("SELECT id FROM users WHERE lower(email)=lower(?)", (bootstrap_email,)).fetchone()
if existing:
    bootstrap_id = existing[0]
    conn.execute("UPDATE users SET full_name=?, role='admin', escalation_authority=1 WHERE id=?", ("Anonymous Admin", bootstrap_id))
    conn.execute("UPDATE user_credentials SET password_hash=?, department='Administration', is_active=1 WHERE user_id=?", (hash_password(bootstrap_password), bootstrap_id))
else:
    cur = conn.execute("INSERT INTO users(full_name,email,role,escalation_authority) VALUES(?,?, 'admin', 1)", ("Anonymous Admin", bootstrap_email))
    bootstrap_id = cur.lastrowid
    conn.execute("INSERT INTO user_credentials(user_id,password_hash,department,is_active) VALUES(?,?, 'Administration', 1)", (bootstrap_id, hash_password(bootstrap_password)))
conn.commit()
print(f"Initialized {db_file}")
print("Seeded 4 blocks, 32 floors, 320 classrooms, 4 canteens, 40 timetable rows, and demo users.")
print("Demo password for seeded accounts: CampusDemo123! (change before any real use)")
print("Bootstrap administrator ensured: anonymous1@campusspace.edu.in")
conn.close()
