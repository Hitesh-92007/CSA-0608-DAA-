"""Quadratic closest-pair baseline for CO2 Q4."""

from math import sqrt
from time import perf_counter


def closest_pair(points):
    if len(points) < 2:
        return None, None, 0, 0.0
    best_pair = None
    best_squared = float("inf")
    calculations = 0
    start = perf_counter()
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            squared = dx * dx + dy * dy
            calculations += 1
            if squared < best_squared:
                best_squared = squared
                best_pair = (i, j)
    elapsed = perf_counter() - start
    return best_pair, sqrt(best_squared), calculations, elapsed


def generate_points(n, seed=604):
    points = []
    for i in range(n):
        x = ((i * 7_919 + seed * 31) % 1_000_003) + i * 0.001
        y = ((i * 10_007 + seed * 17) % 1_000_033) + i * 0.002
        points.append((x, y))
    return points


def run():
    rows = []
    for n in (100, 300, 600, 1_000, 2_000):
        points = generate_points(n)
        pair, distance, calculations, elapsed = closest_pair(points)
        assert calculations == n * (n - 1) // 2
        rows.append((n, pair, distance, calculations, elapsed))
    return rows


if __name__ == "__main__":
    print("n      closest_pair_indices     distance       pair calculations       time")
    for n, pair, distance, calculations, elapsed in run():
        print(f"{n:<6} {str(pair):>12} {distance:>14.6f} "
              f"{calculations:>20} {elapsed:>10.6f}s")
