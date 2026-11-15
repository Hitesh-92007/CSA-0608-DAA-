"""Q7 working challenge: maximum contiguous subarray by divide and conquer."""
from __future__ import annotations

from typing import Iterable


def maximum_subarray_divide_conquer(values: Iterable[int]) -> tuple[int, int, int, int]:
    data = list(values)
    if not data:
        raise ValueError("maximum subarray requires a non-empty input")
    additions = 0

    def solve(lo: int, hi: int) -> tuple[int, int, int]:
        nonlocal additions
        if lo == hi:
            return data[lo], lo, hi
        mid = (lo + hi) // 2
        left = solve(lo, mid); right = solve(mid + 1, hi)
        total = 0; best_left = float("-inf"); best_start = mid
        for i in range(mid, lo - 1, -1):
            total += data[i]; additions += 1
            if total > best_left or (total == best_left and i < best_start):
                best_left, best_start = total, i
        total = 0; best_right = float("-inf"); best_end = mid + 1
        for j in range(mid + 1, hi + 1):
            total += data[j]; additions += 1
            if total > best_right:
                best_right, best_end = total, j
        cross = (int(best_left + best_right), best_start, best_end)
        # Stable tie rule: prefer earlier start, then earlier end.
        return max((left, right, cross), key=lambda x: (x[0], -x[1], -x[2]))

    best = solve(0, len(data) - 1)
    return best[0], best[1], best[2], additions


def maximum_subarray_brute_force(values: Iterable[int]) -> tuple[int, int, int, int]:
    data = list(values)
    if not data:
        raise ValueError("maximum subarray requires a non-empty input")
    best_sum = data[0]; best_start = best_end = 0; additions = 0
    for i in range(len(data)):
        total = 0
        for j in range(i, len(data)):
            total += data[j]; additions += 1
            if (total, -i, -j) > (best_sum, -best_start, -best_end):
                best_sum, best_start, best_end = total, i, j
    return best_sum, best_start, best_end, additions


def demo() -> str:
    values = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    dc = maximum_subarray_divide_conquer(values)
    brute = maximum_subarray_brute_force(values)
    return "\n".join([
        f"Input: {values}",
        f"D&C maximum segment: sum={dc[0]}, indices={dc[1]}..{dc[2]}, segment={values[dc[1]:dc[2]+1]}, boundary additions={dc[3]}",
        f"Brute-force maximum segment: sum={brute[0]}, indices={brute[1]}..{brute[2]}, segment={values[brute[1]:brute[2]+1]}, additions={brute[3]}",
        f"Results agree: {dc[:3] == brute[:3]}",
    ])


if __name__ == "__main__":
    print(demo())
