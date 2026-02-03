import sqlite3
import os

DB_PATH_ENV = os.environ.get("DB_PATH", "patient_health_data.db")
# Resolve DB path: prefer absolute path or project-root-relative file if present
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
candidate = DB_PATH_ENV if os.path.isabs(DB_PATH_ENV) else os.path.join(project_root, DB_PATH_ENV)
if os.path.exists(candidate):
    DB_PATH = candidate
elif os.path.exists(DB_PATH_ENV):
    DB_PATH = DB_PATH_ENV
else:
    DB_PATH = DB_PATH_ENV  # fallback; file may not exist

OUT_FILE = os.path.join(project_root, "schemas.txt")

print(f"Reading schema from: {DB_PATH}")
if not os.path.exists(DB_PATH):
    print(f"Database file not found: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND sql NOT NULL AND name NOT LIKE 'sqlite_%';")
rows = cur.fetchall()

if not rows:
    print("No tables found in database or database missing.")
else:
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for i, (name, sql) in enumerate(rows):
            # Normalise whitespace and ensure SQL statement ends with semicolon
            stmt = sql.strip()
            if not stmt.endswith(";"):
                stmt += ";"
            f.write(stmt)
            if i != len(rows) - 1:
                f.write("\n&\n")
    print(f"Wrote {len(rows)} table schemas to {OUT_FILE}")

conn.close()