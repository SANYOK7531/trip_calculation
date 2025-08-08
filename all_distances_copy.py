def format_full_distance_table(all_points, matrix):
    headers = [name for name, _, _ in all_points]
    lines = []

    # Заголовок
    max_width = max(len(name) for name, _, _ in all_points) + 1  # додаємо запас
    header_line = f"{'':<{max_width}}" + "| ".join([f"{h:<{max_width}}" for h in headers])
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Рядки
    for i, (from_name, _, _) in enumerate(all_points):
        row = f"{from_name:<{max_width}}"
        for j in range(len(all_points)):
            dist_m = matrix[i][j]
            dist_km = " | " f"{dist_m / 1000:.1f} km" if dist_m != float("inf") else "—"
            row += f"{dist_km:<{max_width}}"
        lines.append(row)

    return "\n".join(lines)