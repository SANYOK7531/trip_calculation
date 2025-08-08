# from api_conncetions_copy import get_distance_matrix_osrm
from api_conncetions_copy import get_distance_matrix

def build_full_matrix_with_start(locations, start_point):
    # Всі точки: [START] + решта
    all_points = [start_point] + locations
    
    n = len(all_points)

    # Побудова матриці n x n
    matrix = [[0.0] * n for _ in range(n)]

    # return get_distance_matrix_osrm(all_points, matrix)
    return get_distance_matrix(all_points, matrix)