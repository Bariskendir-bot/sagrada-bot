import os
import time
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Render'ın servisi kapatmasını önleyecek sahte web sunucusu
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot aktif sekilde calisiyor!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Web sunucusunu arka planda başlat
Thread(target=run_web_server, daemon=True).start()

# --- Telegram Bot Kodları ---
TELEGRAM_TOKEN = "8659750495:AAHGbqBjPzJWwe2pSITIsEa7hrMn-ZY0XJ0"
CHAT_ID = "5899841533"
URL = "https://sagradafamilia.org/"
TARGET_DATES = ["2026-10-24", "2026-10-25"]

def send_telegram_msg(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Telegram hatasi: {e}")

# İlk açılış test bildirimi
send_telegram_msg("🤖 *Sagrada Familia Bilet Botu Render Üzerinde Aktif!* 24-25 Ekim izleniyor.")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

while True:
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        if response.status_code == 200:
            content = response.text
            found_dates = [date for date in TARGET_DATES if date in content]
            if found_dates:
                msg = f"🚨 *SAGRADA FAMILIA BİLET ALARMI!*\n\nHedef tarihler için bilet bulundu:\n📅 Tarihler: {', '.join(found_dates)}\n🔗 {URL}"
                send_telegram_msg(msg)
            else:
                print("Bilet yok, taranıyor...")
    except Exception as e:
        print(f"Hata: {e}")
    
    time.sleep(180)
