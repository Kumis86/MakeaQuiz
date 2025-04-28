# utils/otp_utils.py
import random
import smtplib
from email.message import EmailMessage

def send_otp(to_email, username):
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
    except Exception as e:
        print("Gagal mengirim email:", e)
        return None

    server.quit()
    return otp