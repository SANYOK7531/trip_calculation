def generate_maps_url(route, all_points):
    coords = []

    for idx in route:
        lat = all_points[idx][1]
        lon = all_points[idx][2]
        coords.append(f"{lat},{lon}")

    # 🧭 Перевіряємо: чи маршрут вже закінчується на START?
    if route[-1] != 0:
        coords.append(f"{all_points[0][1]},{all_points[0][2]}")

    url = "https://www.google.com/maps/dir/" + "/".join(coords)
    return url
