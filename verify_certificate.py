import sqlite3
from security import generate_certificate_hash


def verify_certificate(cert_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM competition_certificates WHERE cert_id=?",
        (cert_id,)
    )
    data = cur.fetchone()
    conn.close()

    # ❌ Certificate not found
    if not data:
        return None

    stored_hash = data[6]

    recalculated_hash = generate_certificate_hash(
        data[0],  # cert_id
        data[1],  # student_name
        data[2]   # competition_name
    )

    # ❌ Data tampered
    if stored_hash != recalculated_hash:
        return "TAMPERED"

    # ⚠ Certificate revoked
    if data[7] != "ACTIVE":
        return "REVOKED"

    # ✅ Certificate valid
    return data
