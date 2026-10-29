from pathlib import Path
import sqlite3
DB=Path(__file__).resolve().parents[1]/'data'/'campusspace.db'
if not DB.exists(): raise SystemExit('Run scripts/init_db.py first')
c=sqlite3.connect(DB)
checks={'blocks':4,'floors':32,'classrooms':320,'canteens':4,'users':8,'timetable_entries':40}
failed=False
for table, expected in checks.items():
 got=c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
 ok=got==expected; print(('PASS' if ok else 'FAIL'),table,got,'expected',expected); failed|=not ok
c.close()
if failed: raise SystemExit(1)
