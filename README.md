
# 🏆 Competition Certificate Verification System 

A **secure, end-to-end certificate verification platform** built using **Python & Flask** that helps colleges and institutions verify **competition certificates** and detect **fake, tampered, or revoked certificates** using **cryptographic hashing, QR codes, and admin control**. 

This project is designed **from scratch to professional level**, suitable for:
- 🎓 Final-year / college projects
- 🧪 Internal college verification systems
- 💼 Internship & placement demonstrations
- 🚀 Real-world backend + security learning 

---

## 📌 Problem Statement 

Fake and duplicate certificates are commonly used in colleges and job applications.  
Manual verification is slow, unreliable, and error-prone.

### ❌ Traditional Problems
- Certificates can be easily edited
- No centralized verification
- Manual checking required
- No revocation control

---

## ✅ Solution Overview

This system provides:
- 🔐 **Cryptographic certificate validation**
- 📷 **QR-based instant verification**
- 👨‍💼 **Admin-controlled issuance & revocation**
- 📄 **Downloadable PDF certificates**
- 🧾 **Professional certificate UI**

---

## 🚀 Features (From Basic to Pro)

### 🔓 Public Features
- Verify certificate using **Certificate ID**
- Verify certificate using **QR code scanning**
- View professional digital certificate
- Download certificate as **PDF**

### 🔐 Security Features
- SHA-256 hash-based integrity check
- Tamper detection
- Fake certificate detection
- Revoked certificate blocking

### 👨‍💼 Admin Features
- Secure admin login
- Add new certificates
- View all certificates
- Revoke / Activate certificates
- Logout & session control

### 🧾 Certificate Features
- Premium certificate UI
- QR code embedded
- Digital watermark
- PDF export (print-ready)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Language | Python 3 |
| Backend | Flask |
| Database | SQLite |
| Security | SHA-256 hashing |
| QR Generation | qrcode + Pillow |
| QR Scanning | OpenCV + pyzbar |
| PDF | ReportLab |
| Frontend | HTML5 + CSS3 |

---

## 📂 Project Structure

```

competition_certificate_verification/
│
├── app.py                     # Main Flask app
├── database.py                # Database initialization
├── database.db                # SQLite database
├── generate_certificate.py    # Random certificate generator
├── verify_certificate.py      # Certificate verification logic
├── security.py                # Hash generation logic
├── qr_scanner.py              # Camera-based QR scanning
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── certificate.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── admin_add.html
│
├── static/
│   ├── style.css
│   └── certificate.css
│
├── certificates/
│   └── *.png / *.pdf
│
├── venv/
├── requirements.txt
├── .gitignore
└── README.md

```

---

## ⚙️ Installation (Easy & Clean)

### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd competition_certificate_verification
````

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Linux users (for QR scanning):

```bash
sudo pacman -S zbar v4l-utils
```

---

## 🗃️ Database Setup (IMPORTANT)

### 4️⃣ Initialize Database

```bash
python database.py
```

Expected output:

```
✅ Database initialized with admin & certificate tables
```

This creates:

* `admins` table
* `competition_certificates` table
* Default admin user

---

## 🔐 Admin Login Details

```
Username: admin
Password: admin123
```

(Admin credentials are stored locally for project simplicity.)

---

## ▶️ Running the Application

### 5️⃣ Start Flask Server

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🌐 Application Routes

| URL                          | Purpose                         |
| ---------------------------- | ------------------------------- |
| `/`                          | Public certificate verification |
| `/scan`                      | Camera-based QR scan            |
| `/certificate/<cert_id>`     | View certificate                |
| `/certificate/pdf/<cert_id>` | Download PDF                    |
| `/admin`                     | Admin entry point               |
| `/admin/login`               | Admin login                     |
| `/admin/dashboard`           | Admin panel                     |
| `/admin/add`                 | Add certificate                 |

---

## 🧪 Generate Random Certificates

To generate a secure, random certificate:

```bash
python generate_certificate.py
```

This will:

* Generate unique Certificate ID
* Insert data into database
* Create QR code in `certificates/`
* Make certificate ready for verification

---

## 🔍 Verification Flow

1. User enters Certificate ID OR scans QR
2. System fetches certificate from DB
3. Hash is recomputed
4. Comparison happens:

   * ✅ VERIFIED
   * ❌ FAKE
   * ❌ TAMPERED
   * ⚠ REVOKED

---

## 🎨 Frontend Design

* Clean & responsive UI
* Premium certificate layout
* Digital watermark
* QR embedded verification
* Print-ready PDF

---


## 📈 Future Enhancements

* Password hashing (bcrypt)
* Verification audit logs
* Role-based users
* Cloud deployment
* Blockchain verification

---

## 🧑‍💻 Author

**Pratik Khumkar**  
Backend & Security Enthusiast  
Python | Flask | Web Security  

---

## 📜 License

This project is for **educational and demonstration purposes**.
Free to use and extend with attribution.

---


