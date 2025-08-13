# import requests
# from dotenv_read_copy import API_KEY

# def get_distance_matrix(all_points, matrix):
#     n = len(all_points)
#     request_count = 0  # 🔢 Лічильник запитів

#     for i in range(n):
#         origin_coord = f"{all_points[i][1]},{all_points[i][2]}"
#         destination_coords = [f"{point[1]},{point[2]}" for point in all_points]

#         url = "https://maps.googleapis.com/maps/api/distancematrix/json"
#         params = {
#             "origins": origin_coord,
#             "destinations": "|".join(destination_coords),
#             "key": API_KEY,
#             "units": "metric",
#             "mode": "driving",
#         }

#         response = requests.get(url, params=params)
#         request_count += 1
#         print(f"📡 Запит #{request_count} — Origin {i + 1}/{n}")

#         data = response.json()

#         if data["status"] != "OK":
#             print(f"❌ Запит API не спрацював для точки {all_points[i][0]}")
#             continue

#         elements = data["rows"][0]["elements"]
#         for j in range(n):
#             element = elements[j]
#             if element["status"] == "OK":
#                 matrix[i][j] = element["distance"]["value"]  # у метрах
#             else:
#                 matrix[i][j] = float("inf")  # недоступна точка

#     print(f"✅ Усього запитів виконано: {request_count}")
#     return all_points, matrix

import requests
from dotenv_read_copy import API_KEY

def get_distance_matrix(all_points, matrix):
    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters"
    }

    n = len(all_points)
    request_count = 0  # 🔢 Лічильник запитів

    for i in range(n):
        origin = {
            "waypoint": {
                "location": {
                    "latLng": {
                        "latitude": all_points[i][1],
                        "longitude": all_points[i][2]
                    }
                }
            }
        }

        destinations = [
            {
                "waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": p[1],
                            "longitude": p[2]
                        }
                    }
                }
            } for p in all_points
        ]

        body = {
            "origins": [origin],
            "destinations": destinations,
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_UNAWARE"
        }

        response = requests.post(url, headers=headers, json=body)
        request_count += 1
        print(f"📡 Запит #{request_count} — Origin {i + 1}/{n}")

        if response.status_code != 200:
            print(f"❌ Помилка запиту: {response.status_code}")
            print(response.text)
            continue

        results = response.json()

        for row in results:
            j = row["destinationIndex"]
            if "distanceMeters" in row:
                matrix[i][j] = row["distanceMeters"]
            else:
                matrix[i][j] = float("inf")

    print(f"📊 Усього запитів виконано: {request_count}")
    return all_points, matrix
