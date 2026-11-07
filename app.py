from flask import (
    Flask, render_template, request,
    redirect, session, send_from_directory
)
import sqlite3
from datetime import datetime
import os

# Security & Verification
from security import generate_certificate_hash
from verify_certificate import verify_certificate

# QR Scanner
from qr_scanner import scan_qr

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "database.db"
CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)


def get_db():
    return sqlite3.connect(DB_NAME)


# =========================
# AUTH HELPER (IMPORTANT)
# =========================
def admin_required():
    return "admin" in session


# =========================
# PUBLIC VERIFICATION
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cert_id = request.form["cert_id"]
        result = verify_certificate(cert_id)
        return render_template("result.html", result=result)
    return render_template("index.html")


# =========================
# QR SCAN (CAMERA)
# =========================
@app.route("/scan")
def scan():
    qr_data = scan_qr()
    if not qr_data:
        return "❌ No QR detected"

    cert_id = qr_data.split("|")[0]
    result = verify_certificate(cert_id)
    return render_template("result.html", result=result)


# =========================
# CERTIFICATE VIEW
# =========================
@app.route("/certificate/<cert_id>")
def view_certificate(cert_id):
    data = verify_certificate(cert_id)

    if not data or data in ["TAMPERED", "REVOKED"]:
        return "❌ Invalid Certificate"

    return render_template(
        "certificate.html",
        cert_id=data[0],
        student_name=data[1],
        competition=data[2],
        position=data[3],
        organizer=data[4],
        year=data[5]
    )


# =========================
# CERTIFICATE PDF DOWNLOAD
# =========================
@app.route("/certificate/pdf/<cert_id>")
def certificate_pdf(cert_id):
    data = verify_certificate(cert_id)
    if not data or data in ["TAMPERED", "REVOKED"]:
        return "❌ Invalid Certificate"

    filename = f"{cert_id}.pdf"
    path = os.path.join(CERT_DIR, filename)

    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(300, 750, "Certificate of Achievement")

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 700, "This is to certify that")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 660, data[1])

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 620, f"has excelled in {data[2]}")
    c.drawCentredString(300, 580, f"Position: {data[3]}")
    c.drawCentredString(300, 540, f"Organizer: {data[4]}")
    c.drawCentredString(300, 500, f"Year: {data[5]}")
    c.drawCentredString(300, 460, f"Certificate ID: {data[0]}")

    c.save()
    return send_from_directory(CERT_DIR, filename, as_attachment=True)


# =========================
# ADMIN ENTRY (SYSTEMATIC)
# =========================
@app.route("/admin")
def admin_entry():
    if admin_required():
        return redirect("/admin/dashboard")
    return redirect("/admin/login")


# =========================
# ADMIN LOGIN
# =========================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (user, pwd)
        )
        admin = cur.fetchone()
        conn.close()

        if admin:
            session["admin"] = user
            return redirect("/admin/dashboard")
        else:
            return "❌ Invalid Admin Credentials"

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not admin_required():
        return redirect("/admin/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM competition_certificates")
    data = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", certificates=data)


# =========================
# ADD CERTIFICATE (ADMIN)
# =========================
@app.route("/admin/add", methods=["GET", "POST"])
def add_certificate():
    if not admin_required():
        return redirect("/admin/login")

    if request.method == "POST":
        cert_id = request.form["cert_id"]
        student = request.form["student_name"]
        competition = request.form["competition"]

        cert_hash = generate_certificate_hash(cert_id, student, competition)

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO competition_certificates
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            cert_id,
            student,
            competition,
            request.form["position"],
            request.form["organizer"],
            request.form["year"],
            cert_hash,
            "ACTIVE",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        return redirect("/admin/dashboard")

    return render_template("admin_add.html")


# =========================
# REVOKE / ACTIVATE
# =========================
@app.route("/admin/toggle/<cert_id>")
def toggle_certificate(cert_id):
    if not admin_required():
        return redirect("/admin/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM competition_certificates WHERE cert_id=?",
        (cert_id,)
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return redirect("/admin/dashboard")

    new_status = "REVOKED" if row[0] == "ACTIVE" else "ACTIVE"

    cur.execute(
        "UPDATE competition_certificates SET status=? WHERE cert_id=?",
        (new_status, cert_id)
    )
    conn.commit()
    conn.close()

    return redirect("/admin/dashboard")


# =========================
# LOGOUT
# =========================
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/")


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
