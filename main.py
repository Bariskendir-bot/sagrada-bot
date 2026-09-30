import time
import requests

# Kendi bilgileriniz
TELEGRAM_BOT_TOKEN = "8659750495:AAHGbqBjPzJWwe2pSITIsEa7hrMn-ZY0XJ0"
TELEGRAM_CHAT_ID = "5899841533"

URL = "https://sagradafamilia.org/en/tickets"
TARGET_DATES = ["2026-10-24", "2026-10-25"]

def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(api_url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram hatasi:", e)

def check_tickets():
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        content = response.text
        for date in TARGET_DATES:
            if date in content:
                msg = f"🚨 SAGRADA FAMILIA BILET ALARMI! {date} tarihi icin hareketlilik var! Hemen kontrol et: {URL}"
                send_telegram(msg)
                print(f"Bilet bulundu: {date}")
    except Exception as e:
        print("Sayfa kontrol hatasi:", e)

# Ilk calisma testi
send_telegram("🤖 Sagrada Familia Bilet Botu Render Üzerinde Aktif! 24-25 Ekim izleniyor.")

while True:
    check_tickets()
    time.sleep(180)
