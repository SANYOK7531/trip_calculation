import requests
from dotenv_read_copy import API_KEY

def get_distance_matrix(all_points, matrix):

    n = len(all_points)
    
    for i in range(n):
        origin_coord = f"{all_points[i][1]},{all_points[i][2]}"
        destination_coords = [f"{point[1]},{point[2]}" for point in all_points]

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin_coord,
            "destinations": "|".join(destination_coords),
            "key": API_KEY,
            "units": "metric",
            "mode": "driving",
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            print(f"❌ Запит API не спрацював для точки {all_points[i][0]}")
            print(f"❌ Помилка для пари: {origin_coord} → {destination_coords[j]}")
            continue

        elements = data["rows"][0]["elements"]
        for j in range(n):
            element = elements[j]
            if element["status"] == "OK":
                matrix[i][j] = element["distance"]["value"]  # у метрах
            else:
                matrix[i][j] = float("inf")  # недоступна точка

    return all_points, matrix

# import requests

# def get_distance_matrix_osrm(all_points, matrix):
#     n = len(all_points)

#     # Формуємо рядок координат через ;
#     coord_string = ";".join(f"{point[1]},{point[2]}" for point in all_points)

#     # Виконуємо запит до OSRM
#     url = f"http://router.project-osrm.org/table/v1/driving/{coord_string}"
#     params = {
#         "annotations": "distance"  # можна також додати "duration"
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     if "distances" not in data:
#         print("❌ OSRM не повернув 'distances'")
#         return all_points, matrix

#     # Записуємо матрицю
#     for i in range(n):
#         for j in range(n):
#             dist = data["distances"][i][j]
#             matrix[i][j] = dist if dist is not None else float("inf")

#     return all_points, matrix
