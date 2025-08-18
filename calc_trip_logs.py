import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

# 🔐 Шлях до секрету
key_path = "/secrets/sheets_key/sheets_key"  # ← оновлено

# 📥 Зчитуємо JSON-файл
with open(key_path, "r") as f:
    creds_dict = json.load(f)

# ✅ Авторизація через словник, не через шлях
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("sheets_key.json", scope)  # ← оновлено
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 📄 Відкриваємо таблицю
sheet = client.open("Trip Calculation Logs").worksheet("Logs")

def log_request(client_name, ip, points_count, duration_sec, status="OK"):
    now = datetime.utcnow()
    time_str = now.strftime("%H:%M:%S")      # 🕒 час
    day_str = now.strftime("%d")             # 📅 день
    month_str = now.strftime("%m")           # 📆 місяць
    timestamp = now.isoformat()              # 🧭 повний UTC timestamp (можеш прибрати, якщо не треба)

    row = [ip, client_name, points_count, duration_sec, time_str, day_str, month_str, timestamp, status]
    try:
        sheet.append_row(row)
        print(f"✅ Лог записано: {row}")
    except Exception as e:
        print(f"❌ Не вдалося записати лог у Sheets: {str(e)}")

