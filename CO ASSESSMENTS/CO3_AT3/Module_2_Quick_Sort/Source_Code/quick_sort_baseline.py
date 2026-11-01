"""First-element-pivot Quick Sort used to reproduce the case-study issue."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, TypeVar

T = TypeVar("T")


@dataclass
class QuickSortStats:
    comparisons: int = 0
    partitions: int = 0


def first_pivot_partition(values: Sequence[T], stats: QuickSortStats | None = None
                          ) -> tuple[list[T], int]:
    """Partition once with the first item as pivot; values smaller go left."""
    items = list(values)
    if not items:
        return items, -1
    if stats is None:
        stats = QuickSortStats()

    pivot = items[0]
    boundary = 0
    for scan in range(1, len(items)):
        stats.comparisons += 1
        if items[scan] < pivot:
            boundary += 1
            items[boundary], items[scan] = items[scan], items[boundary]
    items[0], items[boundary] = items[boundary], items[0]
    stats.partitions += 1
    return items, boundary


def quick_sort_first_pivot(values: Sequence[T], stats: QuickSortStats | None = None) -> list[T]:
    """Sort with an explicit range stack, avoiding Python recursion overflow.

    The explicit stack does not fix the quadratic comparison count for ordered
    inputs; it only makes the demonstration safe to run at a larger size.
    """
    items = list(values)
    if stats is None:
        stats = QuickSortStats()
    if len(items) < 2:
        return items

    pending = [(0, len(items) - 1)]
    while pending:
        low, high = pending.pop()
        if low >= high:
            continue
        pivot = items[low]
        boundary = low
        for scan in range(low + 1, high + 1):
            stats.comparisons += 1
            if items[scan] < pivot:
                boundary += 1
                items[boundary], items[scan] = items[scan], items[boundary]
        items[low], items[boundary] = items[boundary], items[low]
        stats.partitions += 1
        if boundary + 1 < high:
            pending.append((boundary + 1, high))
        if low < boundary - 1:
            pending.append((low, boundary - 1))
    return items


if __name__ == "__main__":
    sample = [42, 17, 63, 8, 55, 29]
    trace_stats = QuickSortStats()
    partitioned, pivot_index = first_pivot_partition(sample, trace_stats)
    print("Sample:", sample)
    print("After first-element partition:", partitioned)
    print("Pivot 42 final index:", pivot_index)
    print("Partition comparisons:", trace_stats.comparisons)
    full_stats = QuickSortStats()
    print("Fully sorted sample:", quick_sort_first_pivot(sorted(sample), full_stats))
    print("Total baseline comparisons:", full_stats.comparisons)
