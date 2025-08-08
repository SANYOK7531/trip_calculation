# def tsp_nearest_neighbor(matrix, start_index=0):
#     n = len(matrix)
#     visited = [False] * n
#     path = [start_index]
#     visited[start_index] = True
#     current = start_index

#     for _ in range(n - 1):
#         next_city = None
#         min_dist = float("inf")
#         for i in range(n):
#             if not visited[i] and matrix[current][i] < min_dist:
#                 min_dist = matrix[current][i]
#                 next_city = i

#         path.append(next_city)
#         visited[next_city] = True
#         current = next_city

#     path.append(start_index)
#     return path

def tsp_nearest_neighbor(matrix, start_index=0):
    n = len(matrix)
    visited = [False] * n
    path = [start_index]
    visited[start_index] = True
    current = start_index

    for _ in range(n - 1):
        _ , next_city = min(
            ((matrix[current][i], i) for i in range(n) if not visited[i]),
            default=(float("inf"), None)
        )
        if next_city is None:
            break

        path.append(next_city)
        visited[next_city] = True
        current = next_city

    path.append(start_index)

    return path

def extract_route_info(route, all_points, matrix):

    info = []

    start_point = all_points[route[0]]
    info.append((start_point[0], "Start", "Start"))

    for i in range(len(route) - 1):
        from_idx = route[i]
        to_idx = route[i + 1]

        name = all_points[to_idx][0]
        dist_m = matrix[from_idx][to_idx]
        dist_km = f"{dist_m / 1000:.1f} km" if dist_m != float("inf") else "—"
        dur_min = f"{round(dist_m / 800)} mins" if dist_m != float("inf") else "—"

        info.append((name, dist_km, dur_min))

    return info
