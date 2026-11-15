"""Supporting-line brute-force convex hull for CO2 Q5."""

from collections import defaultdict


def orientation(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def convex_hull(points):
    pts = sorted(set(tuple(p) for p in points))
    n = len(pts)
    if n <= 2:
        return pts, 0, 0
    edges = set()
    orientation_tests = pair_candidates = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            pair_candidates += 1
            a, b = pts[i], pts[j]
            positive = negative = False
            collinear = []
            for k, p in enumerate(pts):
                if k == i or k == j:
                    continue
                value = orientation(a, b, p)
                orientation_tests += 1
                if value > 0:
                    positive = True
                elif value < 0:
                    negative = True
                else:
                    collinear.append(p)
                if positive and negative:
                    break
            if positive and negative:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            length_squared = dx * dx + dy * dy
            outside = False
            for p in collinear:
                projection = (p[0] - a[0]) * dx + (p[1] - a[1]) * dy
                if projection < 0 or projection > length_squared:
                    outside = True
                    break
            if not outside:
                edges.add((a, b))
    adjacency = defaultdict(list)
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    if not adjacency:
        return pts[:1], orientation_tests, pair_candidates
    start = min(adjacency)
    hull = [start]
    previous = None
    current = start
    for _ in range(n + 1):
        options = sorted(p for p in adjacency[current] if p != previous)
        if not options:
            break
        nxt = options[0]
        if nxt == start:
            break
        hull.append(nxt)
        previous, current = current, nxt
    return hull, orientation_tests, pair_candidates


def run():
    cases = {
        "square_with_interior": [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 2)],
        "collinear_edges_and_duplicate": [
            (0, 0), (2, 0), (4, 0), (4, 3), (0, 3), (2, 1), (0, 0)
        ],
        "all_collinear": [(0, 0), (1, 1), (2, 2), (4, 4), (3, 3)],
    }
    return [(name, points, *convex_hull(points)) for name, points in cases.items()]


if __name__ == "__main__":
    for name, points, hull, orientations, pairs in run():
        print(f"{name}: input={len(points)} hull={hull}")
        print(f"  candidate pairs={pairs} orientation tests={orientations}")
