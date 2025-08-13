from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
from full_matrix_creation_copy import build_full_matrix_with_start
from tsp_copy import tsp_nearest_neighbor, extract_route_info
from url_generation_copy import generate_maps_url
from all_distances_copy import format_full_distance_table
from parse_json import parse_json
from dotenv_read_copy import ALLOWED_IPS

app = FastAPI()

@app.middleware("http")
async def restrict_ip_access(request: Request, call_next):
    client_ip = request.client.host
    if client_ip in {"127.0.0.1"}:
        return await call_next(request)
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail=f"Access denied for IP: {client_ip}")
    return await call_next(request)

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

