# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime
# import json

# # 🔐 Зчитуємо секрет-файл
# key_path = "/secrets/sheets_key"  # Це шлях до змонтованого секрету

# with open(key_path, "r") as f:
#     creds_dict = json.load(f)

# # Авторизація
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("creds_dict", scope)
# client = gspread.authorize(creds)

# # Відкриваємо таблицю
# sheet = client.open("Trip Calculation Logs").worksheet("Logs")

# def log_request(client_name, ip, points_count, duration_ms, status="OK"):
#     timestamp = datetime.utcnow().isoformat()
#     row = [ip, client_name, points_count, duration_ms, timestamp, status]
#     try:
#         sheet.append_row(row)
#         print(f"✅ Лог записано: {row}")
#     except Exception as e:
#         print(f"❌ Не вдалося записати лог у Sheets: {str(e)}")
