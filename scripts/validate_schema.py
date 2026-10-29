from pathlib import Path
import sqlite3
ROOT=Path(__file__).resolve().parents[1]; DB=ROOT/'data'/'campusspace.db'
if not DB.exists(): raise SystemExit('Database missing. Run scripts/init_db.py')
con=sqlite3.connect(DB); con.execute('PRAGMA foreign_keys=ON')
problems=con.execute('PRAGMA foreign_key_check').fetchall()
print('Foreign-key check:', 'PASS' if not problems else problems)
for table in ['blocks','floors','classrooms','canteens','timetable_entries','users','fault_reports','canteen_visits']:
 print(f'{table}:',con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0])
if problems: raise SystemExit(1)
con.close()
