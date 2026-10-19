import time
import requests
from bs4 import BeautifulSoup

# ================= НАСТРОЙКИ =================
TELEGRAM_BOT_TOKEN = "8623628157:AAGnBo3bxDR478Sjps19bL0Gj1Ud5Fg5gaQ"
TELEGRAM_CHAT_ID = "6993889912"

SITE_LOGIN_URL = "https://zaimis.by/app/login"
SITE_REQUESTS_URL = "https://zaimis.by/app/all-loans?tab=giveLoan"

LOGIN = "king211"
PASSWORD = "Kings6352410852"

CHECK_INTERVAL = 180
# =============================================

seen_requests = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

def run_parser():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    print("Авторизация на zaimis.by...")
    login_data = {"login": LOGIN, "password": PASSWORD}
    
    try:
        login_resp = session.post(SITE_LOGIN_URL, data=login_data)
        print("Вход выполнен. Статус:", login_resp.status_code)
    except Exception as e:
        print("Ошибка при авторизации:", e)
        return

    send_telegram("🚀 <b>Бот отслеживания заявок запущен!</b>\nОжидаю новые заявки по твоим фильтрам...")

    while True:
        try:
            response = session.get(SITE_REQUESTS_URL)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a", href=True)
                for link in links:
                    href = link['href']
                    if "/app/loan/" in href or "/app/request/" in href:
                        if href not in seen_requests:
                            seen_requests.add(href)
                            full_url = f"https://zaimis.by{href}" if href.startswith("/") else href
                            msg = f"🔥 <b>Новая заявка на Zaimis.by!</b>\n\n🔗 <a href='{full_url}'>Перейти к заявке</a>"
                            send_telegram(msg)
            else:
                print(f"Ошибка запроса страницы: {response.status_code}")
        except Exception as e:
            print(f"Ошибка во время мониторинга: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_parser()
