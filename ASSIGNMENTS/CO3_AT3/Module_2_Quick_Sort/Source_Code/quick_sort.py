"""Robust in-place-style Quick Sort with median-of-three and heap fallback.

The function returns a new list. It uses median-of-three pivot selection,
Hoare partitioning, insertion sort for small ranges, and a depth limit with
heapsort fallback to guarantee O(n log n) worst-case time.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Sequence, TypeVar

T = TypeVar("T")


@dataclass
class QuickSortStats:
    comparisons: int = 0
    partitions: int = 0
    heap_fallbacks: int = 0


def _less(a: T, b: T, stats: QuickSortStats) -> bool:
    stats.comparisons += 1
    return a < b


def _median_of_three(a: T, b: T, c: T, stats: QuickSortStats) -> T:
    if _less(a, b, stats):
        if _less(b, c, stats):
            return b
        return c if _less(a, c, stats) else a
    if _less(a, c, stats):
        return a
    return c if _less(b, c, stats) else b


def _insertion_sort(items: list[T], low: int, high: int,
                    stats: QuickSortStats) -> None:
    for index in range(low + 1, high):
        value = items[index]
        cursor = index
        while cursor > low and _less(value, items[cursor - 1], stats):
            items[cursor] = items[cursor - 1]
            cursor -= 1
        items[cursor] = value


def _hoare_partition(items: list[T], low: int, high: int, pivot: T,
                     stats: QuickSortStats) -> int:
    """Split [low, high) around pivot and return a strict interior boundary."""
    left = low
    right = high - 1
    while True:
        while _less(items[left], pivot, stats):
            left += 1
        while _less(pivot, items[right], stats):
            right -= 1
        if left >= right:
            return right + 1
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


def _heap_sort_range(items: list[T], low: int, high: int,
                     stats: QuickSortStats) -> None:
    """Heapsort items[low:high] in place (high is exclusive)."""
    length = high - low

    def sift_down(root: int, end: int) -> None:
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and _less(items[low + child], items[low + child + 1], stats):
                child += 1
            if not _less(items[low + root], items[low + child], stats):
                return
            items[low + root], items[low + child] = items[low + child], items[low + root]
            root = child

    for root in range(length // 2 - 1, -1, -1):
        sift_down(root, length)
    for end in range(length - 1, 0, -1):
        items[low], items[low + end] = items[low + end], items[low]
        sift_down(0, end)


def _intro_sort(items: list[T], low: int, high: int, depth_limit: int,
                cutoff: int, stats: QuickSortStats) -> None:
    while high - low > cutoff:
        if depth_limit == 0:
            stats.heap_fallbacks += 1
            _heap_sort_range(items, low, high, stats)
            return

        depth_limit -= 1
        middle = low + (high - low) // 2
        pivot = _median_of_three(items[low], items[middle], items[high - 1], stats)
        split = _hoare_partition(items, low, high, pivot, stats)
        stats.partitions += 1

        # Recurse into the smaller side; iterate on the larger side to bound stack depth.
        left_size = split - low
        right_size = high - split
        if left_size < right_size:
            _intro_sort(items, low, split, depth_limit, cutoff, stats)
            low = split
        else:
            _intro_sort(items, split, high, depth_limit, cutoff, stats)
            high = split

    _insertion_sort(items, low, high, stats)


def quick_sort(values: Sequence[T], *, cutoff: int = 24,
               stats: QuickSortStats | None = None,
               depth_limit: int | None = None) -> list[T]:
    """Return values sorted ascending, with deterministic worst-case protection."""
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    items = list(values)
    if stats is None:
        stats = QuickSortStats()
    if len(items) > 1:
        if depth_limit is None:
            depth_limit = 2 * int(log2(len(items)))
        if depth_limit < 0:
            raise ValueError("depth_limit cannot be negative")
        _intro_sort(items, 0, len(items), depth_limit, cutoff, stats)
    return items


if __name__ == "__main__":
    sample = [42, 17, 63, 8, 55, 29]
    stats = QuickSortStats()
    print("Input:", sample)
    print("Sorted scores:", quick_sort(sample, stats=stats))
    print("Key comparisons:", stats.comparisons)
    print("Partitions:", stats.partitions)
    print("Heap fallbacks:", stats.heap_fallbacks)
