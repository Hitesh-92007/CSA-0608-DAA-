"""Lower-bound binary search for the first order with a timestamp."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, TypeAlias

Order: TypeAlias = tuple[int, str]


@dataclass
class SearchStats:
    timestamp_comparisons: int = 0


def first_order_at_timestamp(orders: Sequence[Order], timestamp: int,
                             stats: SearchStats | None = None) -> int | None:
    """Return the first matching index, or None if the timestamp is absent.

    Precondition: orders are sorted in non-decreasing timestamp order.
    """
    if stats is None:
        stats = SearchStats()
    low, high = 0, len(orders)  # Search the half-open interval [low, high).
    while low < high:
        middle = low + (high - low) // 2
        stats.timestamp_comparisons += 1
        if orders[middle][0] < timestamp:
            low = middle + 1
        else:
            high = middle

    if low < len(orders):
        stats.timestamp_comparisons += 1
        if orders[low][0] == timestamp:
            return low
    return None


if __name__ == "__main__":
    ordered = [(101, "O4"), (102, "O2"), (102, "O5"),
               (103, "O6"), (105, "O1"), (105, "O3")]
    stats = SearchStats()
    result = first_order_at_timestamp(ordered, 102, stats)
    print("Consolidated orders:", ordered)
    print("First order at timestamp 102:", result, ordered[result] if result is not None else None)
    print("Timestamp comparisons, including final equality check:", stats.timestamp_comparisons)
