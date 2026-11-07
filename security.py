import hashlib

def generate_certificate_hash(cert_id, student_name, competition):
    raw = f"{cert_id}|{student_name}|{competition}"
    return hashlib.sha256(raw.encode()).hexdigest()
