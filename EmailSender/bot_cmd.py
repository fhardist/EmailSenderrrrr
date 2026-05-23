import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ==================== KONFIGURASI UTAMA ====================
EMAIL_PENGIRIM = "your_email@gmail.com"
EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx" # 16 Digit App Password Lu
FILE_TEXT = "body.txt"
FILE_LAMPIRAN = "CV_Kamu.pdf" # Ubah sesuai nama file PDF lu, file pdf dalam folder yang lu masukin tadi
# ===========================================================

def kirim(tujuan, subjek):
    try:
        if not os.path.exists(FILE_TEXT) or not os.path.exists(FILE_LAMPIRAN):
            print("❌ Error: File body.txt atau PDF tidak ditemukan di folder lokal!")
            return

        print("⏳ Membaca file template dan berkas lampiran ...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_PENGIRIM
        msg['To'] = tujuan
        msg['Subject'] = subjek

        with open(FILE_TEXT, 'r', encoding='utf-8') as f:
            msg.attach(MIMEText(f.read(), 'plain'))

        with open(FILE_LAMPIRAN, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=\"{FILE_LAMPIRAN}\"")
            msg.attach(part)
        
        print("⏳ Menghubungkan ke server SMTP Gmail...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_PENGIRIM, EMAIL_PASSWORD)
        
        print(f"⏳ Mengirim email ke {tujuan}...")
        server.sendmail(EMAIL_PENGIRIM, tujuan, msg.as_string())
        server.quit()
        
        print(f"✅ SUKSES! Email berhasil terkirim ke: {tujuan}")
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan pada versi cmd: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Format Penggunaan cmd: python bot_cmd.py [email_tujuan] , [Subjek Bebas Tanpa Petik]")
    else:
        seluruh_argumen = " ".join(sys.argv[1:])
        if "," in seluruh_argumen:
            bagian_email, bagian_subjek = seluruh_argumen.split(",", 1)
            kirim(bagian_email.strip(), bagian_subjek.strip())
        else:
            email_input = sys.argv[1]
            subjek_input = " ".join(sys.argv[2:])
            kirim(email_input, subjek_input)
