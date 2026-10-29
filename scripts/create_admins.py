"""Promote an existing account to admin without exposing password hashes."""
from pathlib import Path
import sqlite3, getpass, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from backend.security import hash_password
DB=ROOT/'data'/'campusspace.db'
if not DB.exists(): raise SystemExit('Run scripts/init_db.py first')
email=input('Existing account email: ').strip().lower()
con=sqlite3.connect(DB); row=con.execute('SELECT id FROM users WHERE lower(email)=?',(email,)).fetchone()
if not row: con.close(); raise SystemExit('Account not found. Register it in the app first.')
con.execute("UPDATE users SET role='admin',escalation_authority=1 WHERE id=?",(row[0],))
if input('Set/reset password too? [y/N] ').strip().lower()=='y':
 password=getpass.getpass('New password (8+ chars): ')
 if len(password)<8: con.close(); raise SystemExit('Password must contain at least 8 characters')
 con.execute('UPDATE user_credentials SET password_hash=? WHERE user_id=?',(hash_password(password),row[0]))
con.commit(); con.close(); print('Admin role updated.')
