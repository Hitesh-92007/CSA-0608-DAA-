"""Meet-in-the-Middle exact subset-sum solver."""
from __future__ import annotations

from typing import Iterable


def _subset_sums(values: list[int]) -> list[tuple[int, int]]:
    sums = [(0, 0)]
    for i, value in enumerate(values):
        bit = 1 << i
        sums += [(total + value, mask | bit) for total, mask in sums]
    return sums


def meet_in_middle(values: Iterable[int], target: int) -> tuple[list[int] | None, dict[str, int]]:
    data = list(values)
    mid = len(data) // 2
    left = _subset_sums(data[:mid])
    right = sorted(_subset_sums(data[mid:]), key=lambda x: x[0])
    right_values = [total for total, _ in right]
    stats = {"left_subsets": len(left), "right_subsets": len(right), "binary_search_comparisons": 0}
    for left_sum, left_mask in left:
        wanted = target - left_sum
        lo, hi = 0, len(right_values)
        while lo < hi:
            stats["binary_search_comparisons"] += 1
            m = (lo + hi) // 2
            if right_values[m] < wanted:
                lo = m + 1
            else:
                hi = m
        if lo < len(right_values) and right_values[lo] == wanted:
            right_mask = right[lo][1]
            chosen = [data[i] for i in range(mid) if left_mask & (1 << i)]
            chosen.extend(data[mid + j] for j in range(len(data) - mid) if right_mask & (1 << j))
            return chosen, stats
    return None, stats


def exhaustive_subset_sum(values: Iterable[int], target: int) -> tuple[list[int] | None, int]:
    data = list(values)
    previous = 0; total = 0
    for index in range(1 << len(data)):
        mask = index ^ (index >> 1)
        if index:
            changed = mask ^ previous
            bit = changed.bit_length() - 1
            total += data[bit] if mask & changed else -data[bit]
        if total == target:
            return [data[i] for i in range(len(data)) if mask & (1 << i)], index + 1
        previous = mask
    return None, 1 << len(data)
