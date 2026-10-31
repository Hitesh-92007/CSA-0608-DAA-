"""Production-oriented SentinelOps algorithms after correctness fixes."""
from dataclasses import dataclass
import math
from typing import Optional, Sequence

Alert = tuple[str, int]
Point = tuple[float, float, int]
Pair = tuple[int, int]


@dataclass
class DistanceCounter:
    """Counts full squared-distance evaluations between candidate point pairs."""
    evaluations: int = 0


@dataclass
class MatchCounter:
    """Counts log-character versus pattern-character comparisons."""
    comparisons: int = 0


def sort_alerts(alerts: list[Alert]) -> list[Alert]:
    """Stable in-place sort by highest severity first using Python's Timsort."""
    alerts[:] = sorted(alerts, key=lambda alert: alert[1], reverse=True)
    return alerts


def build_blocklist_index(blocklist: Sequence[str]) -> frozenset[str]:
    """Build once and reuse for average O(1) membership checks."""
    return frozenset(blocklist)


def is_blocked(blocklist_index: frozenset[str] | set[str], ip: str) -> bool:
    """Return whether ip is present in a previously prepared blocklist index."""
    return ip in blocklist_index


def _build_lps(pattern: str) -> list[int]:
    """Build KMP's longest-prefix-suffix table in O(len(pattern)) time."""
    lps = [0] * len(pattern)
    prefix_len = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[prefix_len]:
            prefix_len += 1
            lps[i] = prefix_len
            i += 1
        elif prefix_len:
            prefix_len = lps[prefix_len - 1]
        else:
            i += 1
    return lps


def find_signature(log: str, pattern: str, counter: Optional[MatchCounter] = None) -> list[int]:
    """Find all occurrences, including overlaps, without rescanning matched prefixes."""
    if not pattern:
        return list(range(len(log) + 1))

    lps = _build_lps(pattern)
    hits = []
    i = j = 0
    while i < len(log):
        if counter is not None:
            counter.comparisons += 1
        if log[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                hits.append(i - j)
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return hits


def closest_logins_bruteforce(
    events: Sequence[tuple[float, float]], counter: Optional[DistanceCounter] = None
) -> tuple[Optional[Pair], float]:
    """Unpruned baseline: evaluate each unordered pair once, then take one square root."""
    n = len(events)
    if n < 2:
        return None, math.inf

    best_squared = math.inf
    best_pair: Optional[Pair] = None
    for i in range(n):
        x1, y1 = events[i]
        for j in range(i + 1, n):
            x2, y2 = events[j]
            if counter is not None:
                counter.evaluations += 1
            dx, dy = x1 - x2, y1 - y2
            squared = dx * dx + dy * dy
            pair = (i, j)
            if squared < best_squared or (squared == best_squared and pair < best_pair):
                best_squared, best_pair = squared, pair
    return best_pair, math.sqrt(best_squared)


def _prefer(candidate_squared: float, candidate_pair: Pair,
            best_squared: float, best_pair: Optional[Pair]) -> bool:
    return (candidate_squared < best_squared or
            (candidate_squared == best_squared and
             (best_pair is None or candidate_pair < best_pair)))


def closest_logins(
    events: Sequence[tuple[float, float]], counter: Optional[DistanceCounter] = None
) -> tuple[Optional[Pair], float]:
    """Divide-and-conquer closest pair with x/y pruning and one final square root.

    Returns the lexicographically first index pair when distances tie. For fewer than
    two events, returns (None, infinity).
    """
    n = len(events)
    if n < 2:
        return None, math.inf

    first_at_coordinate: dict[tuple[float, float], int] = {}
    zero_pair: Optional[Pair] = None
    for index, point in enumerate(events):
        coordinate = (point[0], point[1])
        if coordinate in first_at_coordinate:
            candidate = (first_at_coordinate[coordinate], index)
            if zero_pair is None or candidate < zero_pair:
                zero_pair = candidate
        else:
            first_at_coordinate[coordinate] = index
    if zero_pair is not None:
        return zero_pair, 0.0

    points: list[Point] = [(float(x), float(y), i) for i, (x, y) in enumerate(events)]
    points_x = sorted(points, key=lambda p: (p[0], p[1], p[2]))
    points_y = sorted(points, key=lambda p: (p[1], p[0], p[2]))

    def solve(px: list[Point], py: list[Point]) -> tuple[float, Pair]:
        size = len(px)
        if size <= 3:
            best_sq = math.inf
            best_pair: Optional[Pair] = None
            for a in range(size):
                for b in range(a + 1, size):
                    p, q = px[a], px[b]
                    if counter is not None:
                        counter.evaluations += 1
                    dx, dy = p[0] - q[0], p[1] - q[1]
                    squared = dx * dx + dy * dy
                    pair = (min(p[2], q[2]), max(p[2], q[2]))
                    if _prefer(squared, pair, best_sq, best_pair):
                        best_sq, best_pair = squared, pair
            assert best_pair is not None
            return best_sq, best_pair

        middle = size // 2
        left_x, right_x = px[:middle], px[middle:]
        left_ids = {point[2] for point in left_x}
        left_y, right_y = [], []
        for point in py:
            (left_y if point[2] in left_ids else right_y).append(point)

        left_sq, left_pair = solve(left_x, left_y)
        right_sq, right_pair = solve(right_x, right_y)
        if _prefer(right_sq, right_pair, left_sq, left_pair):
            best_sq, best_pair = right_sq, right_pair
        else:
            best_sq, best_pair = left_sq, left_pair

        split_x = right_x[0][0]
        strip = [point for point in py if (point[0] - split_x) ** 2 <= best_sq]
        for i, p in enumerate(strip):
            j = i + 1
            while j < len(strip):
                q = strip[j]
                dy = q[1] - p[1]
                if dy * dy > best_sq:
                    break
                if (p[2] in left_ids) != (q[2] in left_ids):
                    if counter is not None:
                        counter.evaluations += 1
                    dx = q[0] - p[0]
                    squared = dx * dx + dy * dy
                    pair = (min(p[2], q[2]), max(p[2], q[2]))
                    if _prefer(squared, pair, best_sq, best_pair):
                        best_sq, best_pair = squared, pair
                j += 1
        return best_sq, best_pair

    best_squared, best_pair = solve(points_x, points_y)
    return best_pair, math.sqrt(best_squared)
