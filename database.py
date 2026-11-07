import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# =========================
# ADMIN TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS admins (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

# Default admin (login credentials)
cur.execute("""
INSERT OR IGNORE INTO admins (username, password)
VALUES (?, ?)
""", ("admin", "admin123"))

# =========================
# CERTIFICATE TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS competition_certificates (
    cert_id TEXT PRIMARY KEY,
    student_name TEXT,
    competition_name TEXT,
    position TEXT,
    organizer TEXT,
    year TEXT,
    cert_hash TEXT,
    status TEXT DEFAULT 'ACTIVE',
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized with admin & certificate tables")
