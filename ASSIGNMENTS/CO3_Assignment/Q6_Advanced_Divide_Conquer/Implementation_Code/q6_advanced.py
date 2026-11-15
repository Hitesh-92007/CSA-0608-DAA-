"""Q6 demonstrations for deterministic selection and subset sum."""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Median_of_Medians"))
sys.path.insert(0, str(ROOT / "Meet_in_the_Middle"))
from median_of_medians import median_of_medians
from meet_in_the_middle import exhaustive_subset_sum, meet_in_middle


def quickselect(values: list[int], k: int, *, poor_first: bool = False,
                seed: int = 7, stats: dict[str, int] | None = None) -> int:
    if not 0 <= k < len(values):
        raise IndexError("k must be a valid zero-based index")
    rng = random.Random(seed)
    count = stats if stats is not None else {"comparisons": 0, "partitions": 0, "max_depth": 0}
    data = list(values); lo = 0; hi = len(data) - 1; depth = 0
    while lo <= hi:
        depth += 1; count["max_depth"] = max(count["max_depth"], depth)
        pivot = data[lo] if poor_first else data[rng.randrange(lo, hi + 1)]
        less: list[int] = []; equal: list[int] = []; greater: list[int] = []
        for item in data[lo:hi + 1]:
            count["comparisons"] += 1
            if item < pivot:
                less.append(item)
            else:
                count["comparisons"] += 1
                if item > pivot:
                    greater.append(item)
                else:
                    equal.append(item)
        count["partitions"] += 1
        data[lo:hi + 1] = less + equal + greater
        equal_start = lo + len(less)
        equal_end = equal_start + len(equal) - 1
        if k < equal_start:
            hi = equal_start - 1
        elif k <= equal_end:
            return pivot
        else:
            lo = equal_end + 1
    raise AssertionError("selection failed")


def demo() -> str:
    values = [31, 4, 18, 7, 22, 4, 10, 2, 15, 29, 11, 6, 40, 1, 17, 9, 13, 20, 5, 27, 8]
    k = len(values) // 2
    med_stats = {"comparisons": 0, "partitions": 0, "max_depth": 0}
    poor_stats = {"comparisons": 0, "partitions": 0, "max_depth": 0}
    med = median_of_medians(values, k, med_stats)
    poor = quickselect(sorted(values), k, poor_first=True, stats=poor_stats)
    items, mid_stats = meet_in_middle([3, 34, 4, 12, 5, 2], 9)
    brute, checks = exhaustive_subset_sum([3, 34, 4, 12, 5, 2], 9)
    return "\n".join([
        f"Input selection values: {values}", f"k={k} (zero-based)",
        f"Median of Medians: {med}, comparisons={med_stats['comparisons']}, depth={med_stats['max_depth']}",
        f"First-pivot QuickSelect on sorted data: {poor}, comparisons={poor_stats['comparisons']}, partitions={poor_stats['partitions']}",
        f"Subset sum values=[3, 34, 4, 12, 5, 2], target=9", f"Meet-in-the-Middle solution={items}, halves={mid_stats['left_subsets']}+{mid_stats['right_subsets']}",
        f"Exhaustive solution={brute}, subsets examined={checks}",
    ])


if __name__ == "__main__":
    print(demo())
