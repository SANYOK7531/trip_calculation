# Базовий образ Python
FROM python:3.11-slim

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /doc_analyzer_windows

# Копіюємо файли проєкту
COPY . .

# Оновлюємо pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Встановлюємо залежності з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Оновлюємо spaCy та завантажуємо моделі
RUN pip install --upgrade spacy \
    && python -m spacy download en_core_web_sm \
    && python -m spacy download uk_core_news_sm \
    && python -m spacy validate

COPY .env_copy .env

# Відкриваємо порт
EXPOSE 8000

# Запускаємо FastAPI через Uvicorn
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
