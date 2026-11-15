"""Divide-and-conquer redesign for closest pair, with distance counters."""

from math import sqrt
from time import perf_counter


def closest_pair_dc(points):
    if len(points) < 2:
        return None, None, 0, 0.0
    indexed = [(float(x), float(y), i) for i, (x, y) in enumerate(points)]
    by_coordinate = {}
    for x, y, index in indexed:
        by_coordinate.setdefault((x, y), []).append(index)
    duplicate_pairs = [
        tuple(sorted(ids[:2])) for ids in by_coordinate.values() if len(ids) > 1
    ]
    if duplicate_pairs:
        pair = min(duplicate_pairs)
        return pair, 0.0, 0, 0.0

    px = sorted(indexed, key=lambda p: (p[0], p[1], p[2]))
    py = sorted(indexed, key=lambda p: (p[1], p[0], p[2]))
    distance_calculations = 0
    start = perf_counter()

    def squared_distance(a, b):
        nonlocal distance_calculations
        distance_calculations += 1
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def pair_key(a, b):
        return tuple(sorted((a[2], b[2])))

    def better(left, right):
        if left[0] < right[0]:
            return left
        if right[0] < left[0]:
            return right
        return left if left[1] <= right[1] else right

    def recurse(x_points, y_points):
        size = len(x_points)
        if size <= 3:
            best = (float("inf"), (None, None))
            for i in range(size - 1):
                for j in range(i + 1, size):
                    candidate = (squared_distance(x_points[i], x_points[j]),
                                 pair_key(x_points[i], x_points[j]))
                    best = better(best, candidate)
            return best
        middle = size // 2
        left_x, right_x = x_points[:middle], x_points[middle:]
        left_ids = {p[2] for p in left_x}
        left_y, right_y = [], []
        for point in y_points:
            (left_y if point[2] in left_ids else right_y).append(point)
        best = better(recurse(left_x, left_y), recurse(right_x, right_y))
        split_x = (left_x[-1][0] + right_x[0][0]) / 2.0
        strip = [p for p in y_points if (p[0] - split_x) ** 2 < best[0]]
        for i, point in enumerate(strip):
            j = i + 1
            while j < len(strip) and (strip[j][1] - point[1]) ** 2 < best[0]:
                candidate = (squared_distance(point, strip[j]),
                             pair_key(point, strip[j]))
                best = better(best, candidate)
                j += 1
        return best

    best_squared, pair = recurse(px, py)
    elapsed = perf_counter() - start
    return pair, sqrt(best_squared), distance_calculations, elapsed


if __name__ == "__main__":
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2] /
                        "Q4_Brute_Force_Closest_Pair" /
                        "Implementation_Code"))
    from brute_force_closest_pair import generate_points, closest_pair

    print("n      brute distances     D&C distances     reduction       distance equal")
    for n in (100, 300, 600, 1_000, 2_000):
        points = generate_points(n)
        brute_pair, brute_distance, brute_count, _ = closest_pair(points)
        dc_pair, dc_distance, dc_count, _ = closest_pair_dc(points)
        print(f"{n:<6} {brute_count:>15} {dc_count:>17} "
              f"{(1-dc_count/brute_count)*100:>11.2f}% "
              f"{abs(brute_distance-dc_distance) < 1e-9}")
