"""Stable merge sort for KartIQ order records (timestamp, order_id)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")
K = TypeVar("K")


@dataclass
class SortStats:
    key_comparisons: int = 0


def merge_sort(values: Sequence[T], key: Callable[[T], K],
               stats: SortStats | None = None) -> list[T]:
    """Return a stable ascending sort without changing the input sequence."""
    n = len(values)
    if n <= 1:
        return list(values)

    middle = n // 2
    left = merge_sort(values[:middle], key, stats)
    right = merge_sort(values[middle:], key, stats)
    result: list[T] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if stats is not None:
            stats.key_comparisons += 1
        # Choosing the left item on equality preserves original arrival order.
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


SAMPLE_ORDERS = [(105, "O1"), (102, "O2"), (105, "O3"),
                 (101, "O4"), (102, "O5"), (103, "O6")]


if __name__ == "__main__":
    stats = SortStats()
    print("Input:", SAMPLE_ORDERS)
    print("Stable timestamp order:", merge_sort(SAMPLE_ORDERS, key=lambda row: row[0], stats=stats))
    print("Timestamp comparisons:", stats.key_comparisons)
