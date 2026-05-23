<div align="center">
  <h1>📧 AUTOMATED EMAIL & CV SENDER CLI</h1>
  <p><b>Kirim lamaran kerja dan CV secara instan langsung lewat Terminal Termux (HP) atau Command Line (Laptop/PC)</b></p>
  <hr>
</div>

## 📌 Daftar Isi
1. <a href="#1-cara-mendapatkan-app-password-gmail-16-digit">Cara Mendapatkan App Password Gmail</a>
2. <a href="#2-struktur-file-di-dalam-project">Struktur File Project</a>
3. <a href="#3-panduan-versi-hp-termux">Panduan Versi HP (Termux)</a>
4. <a href="#4-panduan-versi-laptop--pc-windows-linux-macos">Panduan Versi Laptop / PC</a>
5. <a href="#5-cara-konfigurasi-email--app-password">Cara Konfigurasi Email & Password</a>

---

## 🔑 1. Cara Mendapatkan App Password Gmail (16 Digit)
Google melarang login menggunakan password utama demi keamanan. Kamu **wajib** membuat 16 digit App Password terlebih dahulu:

1. Masuk ke halaman <a href="https://myaccount.google.com/security" target="_blank">Google Account Security</a>.
2. Aktifkan **Verifikasi 2 Langkah (2-Step Verification)** jika belum aktif.
3. Di kolom pencarian atas halaman tersebut, ketik **"Sandi Aplikasi"** atau **"App Passwords"**.
4. Masukkan nama bebas (Contoh: `Bot Kirim CV`), lalu klik **Buat (Create)**.
5. Salin **16 digit huruf acak** yang muncul (Contoh: `abcd efgh ijkl mnop`). Simpan kode ini ke Notepad!

---

## 📁 2. Struktur File di Dalam Project
Pastikan susunan file di lokal penyimpanan kamu mengikuti struktur berikut:
*   `bot.py` -> Script utama untuk versi HP (Termux).
*   `bot_laptop.py` -> Script utama untuk versi Laptop/PC.
*   `body.txt` -> File teks berisi isi pesan/surat lamaran email kamu.
*   `CV_Kamu.pdf` -> File PDF CV kamu yang akan otomatis terlampir.

---

## 📲 3. Panduan Versi HP (Termux)
Pilih salah satu metode instalasi di bawah ini yang menurutmu paling mudah:

### 🛠️ Jalur A: Instalasi Instan (Rekomendasi via Git Clone)
Dapatkan seluruh file project langsung dari GitHub dengan mengetik tabel perintah di bawah ini satu per satu:

| No | Langkah Eksekusi Perintah Termux | Keterangan |
| :--- | :--- | :--- |
| 1 | `pkg update && pkg upgrade -y` | Update system Termux |
| 2 | `pkg install python git -y` | Install Python & Git |
| 3 | `termux-setup-storage` | Beri izin akses memori internal HP |
| 4 | `git clone https://github.com/USERNAME_LU/EmailSender.git` | Download repositori dari GitHub lu |
| 5 | `cd EmailSender` | Masuk ke folder project |

> ⚠️ **PENTING Setelah Clone:** Jangan lupa masukkan file CV PDF kamu ke folder Download HP, lalu ganti nama file PDF di dalam kode `bot.py` sesuai nama CV asli kamu.

---

### 📝 Jalur B: Jalur Manual (Bikin Baru Tanpa Git)
Jika kamu tidak ingin melakukan clone, jalankan perintah otomatis di bawah ini untuk membuat file dan mengonfigurasi interseptor shortcut terminal secara instan:

<table>
  <tr>
    <th>Langkah</th>
    <th>Salin & Tempel Perintah Ini ke Termux</th>
  </tr>
  <tr>
    <td><b>1. Buat File Teks Isi Email</b></td>
    <td><pre>mkdir ~/EmailSender && cd ~/EmailSender && nano body.txt</pre><i>(Ketik isi email surat lamaran lu, lalu simpan dengan ketik Ctrl+O, Enter, Ctrl+X)</i></td>
  </tr>
  <tr>
    <td><b>2. Setup Script & System (Otomatis)</b></td>
    <td>
      <pre>
cat << 'EOF' > /data/data/com.termux/files/home/EmailSender/bot.py
import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ==================== KONFIGURASI UTAMA ====================
EMAIL_PENGIRIM = "your_email@gmail.com"
EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx" # 16 Digit App Password Lu
FILE_TEXT = "body.txt"
FILE_LAMPIRAN = "CV_Kamu.pdf" # Ubah sesuai nama file PDF lu
# ===========================================================

def kirim(tujuan, subjek):
    try:
        folder_path = "/data/data/com.termux/files/home/EmailSender"
        full_text_path = os.path.join(folder_path, FILE_TEXT)
        full_pdf_path = os.path.join(folder_path, FILE_LAMPIRAN)
        if not os.path.exists(full_text_path) or not os.path.exists(full_pdf_path):
            print("❌ Error: Berkas body.txt atau PDF belum lengkap di folder!"); return
        print("⏳ Membaca berkas dan bersiap mengirim...")
        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = EMAIL_PENGIRIM, tujuan, subjek
        with open(full_text_path, 'r', encoding='utf-8') as f: msg.attach(MIMEText(f.read(), 'plain'))
        with open(full_pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read()); encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=\"{FILE_LAMPIRAN}\"")
            msg.attach(part)
        server = smtplib.SMTP("smtp.gmail.com", 587); server.starttls()
        server.login(EMAIL_PENGIRIM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_PENGIRIM, tujuan, msg.as_string()); server.quit()
        print(f"✅ SUKSES! CV terkirim ke: {tujuan}")
    except Exception as e: print(f"❌ Gagal: {e}")

if __name__ == "__main__":
    seluruh_argumen = " ".join(sys.argv[1:])
    if "," in seluruh_argumen:
        bagian_email, bagian_subjek = seluruh_argumen.split(",", 1)
        kirim(bagian_email.strip(), bagian_subjek.strip())
    else:
        if len(sys.argv) >= 3: kirim(sys.argv[1], " ".join(sys.argv[2:]))
EOF
      </pre>
    </td>
  </tr>
  <tr>
    <td><b>3. Pasang Shortcut Global Terminal</b></td>
    <td>
      <pre>
rm -f ~/.bashrc && touch ~/.bashrc
cat << 'EOF' >> ~/.bashrc
command_not_found_handle() {
    if [[ "$1" == *"*"* ]]; then return 127
    elif [[ "$1" == *"@"* ]]; then
        python /data/data/com.termux/files/home/EmailSender/bot.py "$@"
    else
        if [[ "$1" == "help" || "$1" == "bot" ]]; then
            echo "Format: email_tujuan , Subjek Tanpa Petik"; return 0
        fi
        print "bash: $1: command not found"; return 127
    fi
}
EOF
source ~/.bashrc
      </pre>
    </td>
  </tr>
</table>

### 🚀 Cara Menjalankan di Termux (Format Gaya Bebas)
Setelah konfigurasi di atas selesai, kamu bisa langsung mengirim email kapan pun tanpa perlu mengetik kata perintah pembuka. Cukup gunakan struktur berikut:

```bash
hrd_tujuan@gmail.com , Lamaran Pekerjaan IT Support Berkas Final Tanpa Petik
