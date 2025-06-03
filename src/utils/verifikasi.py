# utils/otp_utils.py
import random
import smtplib
import time
from email.message import EmailMessage
from pathlib import Path

OTP_LOG_PATH = Path('database/otp_request.txt')
OTP_LIMIT = 3  # Limit permintaan OTP per user
OTP_WINDOW = 600  # Waktu tunggu (cooldown) dalam detik

def load_otp_log():
    if not OTP_LOG_PATH.exists():
        return []
    with open(OTP_LOG_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_otp_log(email):
    now = int(time.time())
    with open(OTP_LOG_PATH, "a") as f:
        f.write(f"{email},{now}\n")

def can_send_otp(email):
    logs = load_otp_log()
    now = int(time.time())
    count = 0

    for log in logs:
        try:
            log_email, ts = log.split(",")
            ts = int(ts)
            if log_email == email and now - ts < OTP_WINDOW:
                count += 1
        except ValueError:
            continue

    return count < OTP_LIMIT

def send_otp(to_email, username):
    if not can_send_otp(to_email):
        print("Batas OTP tercapai. Coba lagi nanti.")
        return None
    
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    from_email = 'makeaquiz.official@gmail.com'
    server.login(from_email, 'esyv bohl izcg oddd')
    
    msg = EmailMessage()
    msg['Subject'] = 'Verifikasi OTP'
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(f"""Halo {username},

Berikut adalah kode verifikasi (OTP) Anda:

🔐 Kode OTP: {otp}

Kode ini berlaku selama 5 menit. Jangan berikan kode ini kepada siapa pun, termasuk pihak yang mengaku dari MakeaQuiz.

Jika Anda tidak meminta kode ini, abaikan email ini atau hubungi tim dukungan kami.

Terima kasih,
Tim MakeaQuiz""")

    try:
        server.send_message(msg)
        print("OTP berhasil dikirim ke", to_email)
        save_otp_log(to_email)
    except Exception as e:
        print("Gagal mengirim email:", e)
        return None

    server.quit()
    return otp