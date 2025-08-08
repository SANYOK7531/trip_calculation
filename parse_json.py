from typing import List, Tuple, Dict
from pydantic import BaseModel

class Point(BaseModel):
    name: str
    lat: float
    lon: float

def parse_json(data: Dict) -> List[Tuple[str, Tuple[str, float, float], List[Tuple[str, float, float]]]]:

    results = []

    try:
        routes = data.get("Routes", [])
        for route in routes:
            route_id = route.get("RouteID", "undefined")
            addresses = route.get("Adresses", [])

            # Пропуск, якщо список порожній
            if not addresses:
                continue

            # Фільтруємо точки з координатами ≠ 0
            valid_points = [
                Point(name=addr["ClientID"], lat=addr["Latitude"], lon=addr["Longitude"])
                for addr in addresses
                if addr.get("Latitude") not in [0.0, "", None] and addr.get("Longitude") not in [0.0, "", None]
            ]

            if not valid_points:
                continue  # нічого валідного — пропускаємо маршрут

            start_point = (valid_points[0].name, valid_points[0].lat, valid_points[0].lon)
            delivery_points = [(p.name, p.lat, p.lon) for p in valid_points[1:]]

            results.append((route_id, start_point, delivery_points))

        return results

    except Exception as e:
        raise ValueError(f"⛔ Помилка при парсингу JSON: {e}")
    