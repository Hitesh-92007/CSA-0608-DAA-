"""Q2: instrumented Merge Sort and last-element-pivot Lomuto Quick Sort."""
from __future__ import annotations

from typing import Iterable


def merge_sort(values: Iterable[int]) -> tuple[list[int], dict[str, int]]:
    data = list(values)
    stats = {"comparisons": 0, "max_depth": 0, "merges": 0}

    def sort(part: list[int], depth: int) -> list[int]:
        stats["max_depth"] = max(stats["max_depth"], depth)
        if len(part) <= 1:
            return part
        mid = len(part) // 2
        left, right = sort(part[:mid], depth + 1), sort(part[mid:], depth + 1)
        out: list[int] = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        out.extend(left[i:]); out.extend(right[j:])
        stats["merges"] += 1
        return out

    return sort(data, 1), stats


def quick_sort(values: Iterable[int]) -> tuple[list[int], dict[str, object]]:
    """Quicksort with Lomuto partition and the last element as pivot."""
    data = list(values)
    stats: dict[str, object] = {"comparisons": 0, "max_depth": 0, "partitions": []}

    def sort(lo: int, hi: int, depth: int) -> None:
        stats["max_depth"] = max(int(stats["max_depth"]), depth)
        if lo >= hi:
            return
        pivot = data[hi]
        i = lo
        for j in range(lo, hi):
            stats["comparisons"] = int(stats["comparisons"]) + 1
            if data[j] <= pivot:
                data[i], data[j] = data[j], data[i]
                i += 1
        data[i], data[hi] = data[hi], data[i]
        cast = stats["partitions"]
        assert isinstance(cast, list)
        cast.append((i - lo, hi - i, hi - lo + 1))
        sort(lo, i - 1, depth + 1)
        sort(i + 1, hi, depth + 1)

    sort(0, len(data) - 1, 1)
    return data, stats


def balanced_last_pivot_permutation(lo: int, hi: int) -> list[int]:
    """Build a permutation that gives median pivots after Lomuto's final swap."""
    if lo > hi:
        return []
    mid = (lo + hi) // 2
    left = balanced_last_pivot_permutation(lo, mid - 1)
    right = balanced_last_pivot_permutation(mid + 1, hi)
    # The pivot swap sends the first greater item to the end of the right
    # partition. Right-rotate the desired sequence to preserve its recursive order.
    if right:
        right = [right[-1]] + right[:-1]
    return left + right + [mid]


def demo() -> str:
    source = [23, 4, 16, 8, 42, 15, 9, 31, 2, 27, 11, 5, 19, 6, 33]
    sorted_merge, m = merge_sort(source)
    sorted_quick, q = quick_sort(source)
    balanced = balanced_last_pivot_permutation(0, 30)
    _, b = quick_sort(balanced)
    _, w = quick_sort(list(range(31)))
    return "\n".join([
        f"Merge Sort output: {sorted_merge}",
        f"Quick Sort output: {sorted_quick}",
        f"Merge comparisons={m['comparisons']}, recursion depth={m['max_depth']}",
        f"Quick comparisons={q['comparisons']}, recursion depth={q['max_depth']}",
        f"Last-pivot balanced case n=31: comparisons={b['comparisons']}, depth={b['max_depth']}",
        f"Last-pivot ascending case n=31: comparisons={w['comparisons']}, depth={w['max_depth']}",
        "Quick Sort pivot: last element; ascending distinct input creates n-1/0 partitions.",
    ])


if __name__ == "__main__":
    print(demo())
