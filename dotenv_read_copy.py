import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GOOGLE_API_KEY")
# ALLOWED_IPS = os.getenv("ALLOWED_IPS")

# Читаємо як рядок і перетворюємо на множину
raw_ips = os.getenv("ALLOWED_IPS", "")
ALLOWED_IPS = set(ip.strip() for ip in raw_ips.split(",") if ip.strip())
