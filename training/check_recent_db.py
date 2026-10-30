import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3

conn = sqlite3.connect("backend/app/noteguard.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(predictions)")
print([col[1] for col in cursor.fetchall()])

cursor.execute("SELECT id, denomination, authenticity, confidence, original_image_url FROM predictions ORDER BY id DESC LIMIT 5")
for r in cursor.fetchall():
    print(r)
