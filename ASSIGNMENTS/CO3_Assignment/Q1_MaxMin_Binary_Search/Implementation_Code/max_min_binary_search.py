"""Q1: tournament-style max/min and iterative binary search."""
from __future__ import annotations

from typing import Iterable


def max_min_divide_conquer(values: Iterable[int]) -> tuple[int, int, int]:
    """Return (minimum, maximum, comparisons); reject an empty input."""
    data = list(values)
    if not data:
        raise ValueError("values must not be empty")

    def solve(lo: int, hi: int) -> tuple[int, int, int]:
        size = hi - lo
        if size == 1:
            return data[lo], data[lo], 0
        if size == 2:
            a, b = data[lo], data[lo + 1]
            return (a, b, 1) if a <= b else (b, a, 1)
        mid = lo + size // 2
        min_l, max_l, c_l = solve(lo, mid)
        min_r, max_r, c_r = solve(mid, hi)
        return min(min_l, min_r), max(max_l, max_r), c_l + c_r + 2

    return solve(0, len(data))


def max_min_independent(values: Iterable[int]) -> tuple[int, int, int]:
    data = list(values)
    if not data:
        raise ValueError("values must not be empty")
    low = high = data[0]
    comparisons = 0
    for value in data[1:]:
        comparisons += 1
        if value < low:
            low = value
        comparisons += 1
        if value > high:
            high = value
    return low, high, comparisons


def binary_search(sorted_values: list[int], target: int) -> tuple[int, int]:
    """Return (index or -1, key comparisons). Input must be sorted ascending."""
    left, right, comparisons = 0, len(sorted_values) - 1, 0
    while left <= right:
        mid = left + (right - left) // 2
        comparisons += 1
        if sorted_values[mid] == target:
            return mid, comparisons
        comparisons += 1
        if sorted_values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons


def demo() -> str:
    values = [19, 4, 27, 8, 11, 2, 31, 6]
    dc = max_min_divide_conquer(values)
    naive = max_min_independent(values)
    ordered = sorted(values)
    lines = [f"Input: {values}", f"Divide-and-conquer min/max: {dc[0]}/{dc[1]} ({dc[2]} comparisons)",
             f"Independent scans min/max: {naive[0]}/{naive[1]} ({naive[2]} comparisons)",
             f"Sorted for binary search: {ordered}"]
    for target in (2, 19, 31, 10):
        index, count = binary_search(ordered, target)
        lines.append(f"Binary search {target}: index={index}, comparisons={count}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(demo())
