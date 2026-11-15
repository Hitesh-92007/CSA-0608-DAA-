"""Q5: brute-force baseline and divide-and-conquer closest pair."""
from __future__ import annotations

from math import sqrt
from typing import Iterable

Point = tuple[float, float]


def brute_force(points: Iterable[Point]) -> tuple[float, tuple[Point, Point] | None, int]:
    data = list(points)
    if len(data) < 2:
        return float("inf"), None, 0
    best2 = float("inf"); best_pair = None; count = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            dx, dy = data[i][0] - data[j][0], data[i][1] - data[j][1]
            d2 = dx * dx + dy * dy; count += 1
            if d2 < best2:
                best2, best_pair = d2, (data[i], data[j])
    return sqrt(best2), best_pair, count


def divide_conquer(points: Iterable[Point]) -> tuple[float, tuple[Point, Point] | None, int]:
    data = list(points)
    if len(data) < 2:
        return float("inf"), None, 0
    # IDs preserve duplicate points and make equal-x partitioning unambiguous.
    px = sorted(((p[0], p[1], i) for i, p in enumerate(data)))
    py = sorted(((p[0], p[1], i) for i, p in enumerate(data)), key=lambda p: (p[1], p[0], p[2]))
    comparisons = 0

    def rec(xs: list[tuple[float, float, int]], ys: list[tuple[float, float, int]]):
        nonlocal comparisons
        n = len(xs)
        if n <= 3:
            best2 = float("inf"); best = None
            for i in range(n):
                for j in range(i + 1, n):
                    dx, dy = xs[i][0] - xs[j][0], xs[i][1] - xs[j][1]
                    d2 = dx * dx + dy * dy; comparisons += 1
                    if d2 < best2:
                        best2, best = d2, (xs[i][2], xs[j][2])
            return best2, best
        mid = n // 2
        left_x, right_x = xs[:mid], xs[mid:]
        left_ids = {p[2] for p in left_x}
        left_y = [p for p in ys if p[2] in left_ids]
        right_y = [p for p in ys if p[2] not in left_ids]
        d_left, pair_left = rec(left_x, left_y)
        d_right, pair_right = rec(right_x, right_y)
        best2, best = (d_left, pair_left) if d_left <= d_right else (d_right, pair_right)
        mid_x = right_x[0][0]
        strip = [p for p in ys if (p[0] - mid_x) ** 2 < best2]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                if (strip[j][1] - strip[i][1]) ** 2 >= best2:
                    break
                dx, dy = strip[i][0] - strip[j][0], strip[i][1] - strip[j][1]
                d2 = dx * dx + dy * dy; comparisons += 1
                if d2 < best2:
                    best2, best = d2, (strip[i][2], strip[j][2])
        return best2, best

    best2, pair = rec(px, py)
    if pair is None:
        return float("inf"), None, comparisons
    return sqrt(best2), (data[pair[0]], data[pair[1]]), comparisons


def demo() -> str:
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (5, 1)]
    brute = brute_force(points); dc = divide_conquer(points)
    return "\n".join([
        f"Points: {points}", f"Brute-force closest distance: {brute[0]:.6f}, pair={brute[1]}, distance calculations={brute[2]}",
        f"Divide-and-conquer closest distance: {dc[0]:.6f}, pair={dc[1]}, distance calculations={dc[2]}",
        f"Distances agree: {abs(brute[0] - dc[0]) < 1e-12}",
    ])


if __name__ == "__main__":
    print(demo())
