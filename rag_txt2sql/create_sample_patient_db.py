import sqlite3
from datetime import date

DB_PATH = "patient_health_data.db"

def create_tables(conn):
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        Id TEXT PRIMARY KEY,
        FIRST TEXT,
        LAST TEXT,
        BIRTHDATE TEXT,
        ETHNICITY TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS conditions (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        START TEXT,
        STOP TEXT,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        BASE_COST REAL,
        PAYER_COVERAGE REAL,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS careplans (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        START TEXT,
        STOP TEXT,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS allergies (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        START TEXT,
        STOP TEXT,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        START TEXT,
        STOP TEXT,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS immunizations (
        Id TEXT PRIMARY KEY,
        PATIENT TEXT,
        DESCRIPTION TEXT,
        START TEXT,
        FOREIGN KEY(PATIENT) REFERENCES patients(Id)
    )
    """)

    conn.commit()


def seed_data(conn):
    c = conn.cursor()

    patients = [
        ("p1", "Alice", "Smith", "1985-06-12", "Hispanic"),
        ("p2", "Bob", "Jones", "1972-11-03", "White"),
        ("p3", "Charlie", "Nguyen", "2008-02-20", "Asian"),
    ]

    c.executemany("INSERT OR IGNORE INTO patients VALUES (?,?,?,?,?)", patients)

    conditions = [
        ("c1", "p1", "asthma", "2010-05-01", None),
        ("c2", "p2", "hypertension", "2015-08-15", None),
        ("c3", "p3", "flu", "2023-01-10", "2023-01-20"),
        ("c4", "p1", "diabetes", "2019-03-01", None),
    ]
    c.executemany("INSERT OR IGNORE INTO conditions VALUES (?,?,?,?,?)", conditions)

    medications = [
        ("m1", "p1", "albuterol", 25.0, 20.0),
        ("m2", "p2", "lisinopril", 15.0, 10.0),
    ]
    c.executemany("INSERT OR IGNORE INTO medications VALUES (?,?,?,?,?)", medications)

    careplans = [
        ("cp1", "p1", "Asthma management plan", "2022-01-01", "2023-01-01"),
    ]
    c.executemany("INSERT OR IGNORE INTO careplans VALUES (?,?,?,?,?)", careplans)

    allergies = [
        ("a1", "p2", "Penicillin", "2000-01-01", None),
    ]
    c.executemany("INSERT OR IGNORE INTO allergies VALUES (?,?,?,?,?)", allergies)

    devices = [
        ("d1", "p3", "Glucose monitor", "2021-06-01", None),
    ]
    c.executemany("INSERT OR IGNORE INTO devices VALUES (?,?,?,?,?)", devices)

    immunizations = [
        ("i1", "p3", "flu vaccine", "2023-10-10"),
    ]
    c.executemany("INSERT OR IGNORE INTO immunizations VALUES (?,?,?,?)", immunizations)

    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    seed_data(conn)
    conn.close()
    print(f"Created {DB_PATH} with sample data.")
