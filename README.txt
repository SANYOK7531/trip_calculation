ІНСТРУКЦІЯ ДЛЯ WINDOWS:

1. Встанови Python 3.11+ з https://python.org
2. Відкрий командний рядок (cmd), зайди у цю теку:
   cd шлях_до_теки
3. Встанови залежності:
   pip install -r requirements.txt
4. Запусти сервер:
   uvicorn doc_analyzer:app --reload --host 127.0.0.1 --port 8000