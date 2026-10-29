from pathlib import Path
import sqlite3
import qrcode
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data'/'campusspace.db'
OUT=ROOT/'qr_codes'; OUT.mkdir(exist_ok=True)
if not DB.exists(): raise SystemExit('Database not found. Run python scripts/init_db.py first.')
conn=sqlite3.connect(DB)
for name, code, identifier in conn.execute('SELECT name,code,qr_code_identifier FROM canteens ORDER BY id'):
    image=qrcode.make(identifier)
    path=OUT/f'{code}.png'; image.save(path)
    (OUT/f'{code}.txt').write_text(f'Canteen: {name}\nCode: {code}\nQR payload: {identifier}\n',encoding='utf-8')
    print(path)
conn.close()
