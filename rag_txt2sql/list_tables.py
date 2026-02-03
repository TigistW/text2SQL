import sqlite3
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(project_root, 'patient_health_data.db')
print('Checking DB at', db_path)
if not os.path.exists(db_path):
    print('Database file not found')
else:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND sql NOT NULL AND name NOT LIKE 'sqlite_%';")
    rows = cur.fetchall()
    print('Found', len(rows), 'tables')
    for name, sql in rows:
        print('---', name)
        print(sql)
    conn.close()