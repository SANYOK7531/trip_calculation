# from fastapi import FastAPI
# from pydantic import BaseModel
# import spacy
# import re

# nlp = spacy.load("uk_core_news_sm")

# app = FastAPI()

# class AnalyzeRequest(BaseModel):
#     text: str

# @app.post("/analyze")
# def analyze(req: AnalyzeRequest):
#     text = req.text
#     doc = nlp(text)
    
#     number = None
    
#     # Тип і номер документа — через RegEx
#     #pattern = r"(н/н|накладна|договір|акт|рахунок|рах\.|дог\.|накл\.)\s*№?\s*([a-zа-яіїґєA-Z0-9\-/]+)"
#     #pattern = r"(?i)(?:\b(?:згідно\s+)?(?:накл\.?|ном(?:\.|ер)?|#|№)\b[\s]*)+(?:[a-zа-яіїґєA-ZА-ЯІЇҐЄ]+)?\s*-?\s*(\d{1,6)(?!\d)"
#     pattern = r"(?i)(?:\b(?:н\/н|н\.?|номер(?:[^\w\s]?|\b\s)|накладна(?:[^\w\s]?|\b\s)|накл(?:адною)?(?:[^\w\s]?|\b\s)|n(?:[^\w\s]?|\b\s))){1,2}[\s]*(?:[a-zа-яіїєґ]{1,4})?\s*-?\s*(\d{1,6})(?!\d)"
#     pattern = (
#     r"(?i)"  # нечутливість до регістру
#     #r"(?:\b(?:згідно|зг\.?|н\/н|н\.?|номер|накладна|накл\.?|накладною|накладноє|n|№)[^\w\d]?\s*){1,3}"  # ключові слова
#     r"(?:[a-zа-яіїєґ]{0,4})?"  # префікс (опціональний)
#     r"\s*?-?\s*?"  # дефіс та пробіли (опціональні)
#     r"(\d{1,6})(?!\d)"  # головна група — 1-6 цифр (без продовження цифрами)
#     )
#     matches = re.findall(pattern, text, re.IGNORECASE)

#     # Доповнюємо кожен номер нулями зліва до довжини 6
#     padded_numbers = [number.zfill(6) for number in matches]

#     return padded_numbers

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
from full_matrix_creation_copy import build_full_matrix_with_start
from tsp_copy import tsp_nearest_neighbor, extract_route_info
from url_generation_copy import generate_maps_url
from all_distances_copy import format_full_distance_table
from parse_json import parse_json
# from dotenv import load_dotenv
# import os

# load_dotenv(override=True)

# ALLOWED_IPS = os.getenv("ALLOWED_IPS")

app = FastAPI()

# @app.middleware("http")
# async def restrict_ip_access(request: Request, call_next):
#     client_ip = request.client.host
#     if client_ip not in ALLOWED_IPS:
#         raise HTTPException(status_code=403, detail="Access denied")
#     return await call_next(request)

class Point(BaseModel):
    name: str
    lat: float
    lon: float

class RequestBody(BaseModel):
    points: List[Point]

@app.post("/calculate")
def calculate_routes(data: dict):
    try:

        routes = parse_json(data)
        # 📍 Отримання delivery_points
        for route_id, start_point, delivery_points in routes:  #[(p.name, p.lat, p.lon) for p in data.points]
        
            all_points, matrix = build_full_matrix_with_start(delivery_points, start_point)
            route = tsp_nearest_neighbor(matrix)
            route_info = extract_route_info(route, all_points, matrix)
            maps_url = generate_maps_url(route, all_points)
            full_table = format_full_distance_table(all_points, matrix)

            return {
                "message": f"🗺️ Розрахунок успішний для {len(delivery_points)} точок",
                "matrix_table": full_table,
                "route": [
                    {
                        "route_id": route_id,
                        "point": name,
                        "distance": distance,
                        "duration": duration
                    } for name, distance, duration in route_info
                ],
                "maps_url": maps_url
            }

    except Exception as e:
        return {"error": str(e)}

