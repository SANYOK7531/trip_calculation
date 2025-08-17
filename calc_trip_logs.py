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
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)  # ← оновлено
client = gspread.authorize(creds)

# 📄 Відкриваємо таблицю
sheet = client.open("Trip Calculation Logs").worksheet("Logs")

def log_request(client_name, ip, points_count, duration_ms, status="OK"):
    timestamp = datetime.utcnow().isoformat()
    row = [ip, client_name, points_count, duration_ms, timestamp, status]
    try:
        sheet.append_row(row)
        print(f"✅ Лог записано: {row}")
    except Exception as e:
        print(f"❌ Не вдалося записати лог у Sheets: {str(e)}")
