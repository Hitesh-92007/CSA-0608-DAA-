"""Deterministic selection using groups of five."""
from __future__ import annotations


def _insertion_sort(values: list[int], stats: dict[str, int]) -> list[int]:
    out = values[:]
    for i in range(1, len(out)):
        value = out[i]; j = i - 1
        while j >= 0:
            stats["comparisons"] += 1
            if out[j] <= value:
                break
            out[j + 1] = out[j]; j -= 1
        out[j + 1] = value
    return out


def median_of_medians(values: list[int], k: int, stats: dict[str, int] | None = None) -> int:
    """Return the zero-based k-th smallest item with a deterministic pivot."""
    if not 0 <= k < len(values):
        raise IndexError("k must be a valid zero-based index")
    count = stats if stats is not None else {"comparisons": 0, "partitions": 0, "max_depth": 0}

    def select(data: list[int], rank: int, depth: int) -> int:
        count["max_depth"] = max(count["max_depth"], depth)
        if len(data) <= 5:
            return _insertion_sort(data, count)[rank]
        medians = []
        for start in range(0, len(data), 5):
            group = _insertion_sort(data[start:start + 5], count)
            medians.append(group[len(group) // 2])
        pivot = select(medians, len(medians) // 2, depth + 1)
        low: list[int] = []; equal: list[int] = []; high: list[int] = []
        for item in data:
            count["comparisons"] += 1
            if item < pivot:
                low.append(item)
            else:
                count["comparisons"] += 1
                if item > pivot:
                    high.append(item)
                else:
                    equal.append(item)
        count["partitions"] += 1
        if rank < len(low):
            return select(low, rank, depth + 1)
        if rank < len(low) + len(equal):
            return pivot
        return select(high, rank - len(low) - len(equal), depth + 1)

    return select(list(values), k, 1)
