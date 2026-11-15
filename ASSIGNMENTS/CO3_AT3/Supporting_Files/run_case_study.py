"""Run the supplied sample datasets through the four algorithms."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for module_dir in (
    "Module_1_Merge_Sort/Source_Code",
    "Module_2_Quick_Sort/Source_Code",
    "Module_3_Binary_Search/Source_Code",
    "Module_4_Strassen_Matrix_Multiplication/Source_Code",
):
    sys.path.insert(0, str(ROOT / module_dir))

from merge_sort import SAMPLE_ORDERS, SortStats, merge_sort
from quick_sort import QuickSortStats, quick_sort
from quick_sort_baseline import QuickSortStats as BaselineStats, first_pivot_partition
from binary_search import SearchStats, first_order_at_timestamp
from strassen import MatrixStats, classical_multiply, strassen_multiply


def main() -> None:
    print("PART (b) - MODULE 1: MERGE SORT")
    merge_stats = SortStats()
    sorted_orders = merge_sort(SAMPLE_ORDERS, key=lambda row: row[0], stats=merge_stats)
    print("Input:", SAMPLE_ORDERS)
    print("Sorted output:", sorted_orders)
    print("Timestamp comparisons:", merge_stats.key_comparisons)
    print("Equal timestamp 102 order IDs:", [row[1] for row in sorted_orders if row[0] == 102])
    print("Equal timestamp 105 order IDs:", [row[1] for row in sorted_orders if row[0] == 105])
    print()

    print("PART (c) - MODULE 2: QUICK SORT")
    sample_scores = [42, 17, 63, 8, 55, 29]
    baseline_stats = BaselineStats()
    partitioned, pivot_index = first_pivot_partition(sample_scores, baseline_stats)
    optimized_stats = QuickSortStats()
    print("Sample scores:", sample_scores)
    print("After first-pivot partition:", partitioned, "pivot index:", pivot_index)
    print("Partition comparisons:", baseline_stats.comparisons)
    print("Optimized sorted scores:", quick_sort(sample_scores, stats=optimized_stats))
    print("Optimized comparisons:", optimized_stats.comparisons,
          "partitions:", optimized_stats.partitions,
          "heap fallbacks:", optimized_stats.heap_fallbacks)
    print()

    print("PART (d) - MODULE 3: FIRST MATCHING ORDER")
    search_stats = SearchStats()
    first = first_order_at_timestamp(sorted_orders, 102, search_stats)
    print("Consolidated orders:", sorted_orders)
    print("Timestamp 102 first index:", first, "record:", sorted_orders[first] if first is not None else None)
    print("Timestamp comparisons including final equality check:", search_stats.timestamp_comparisons)
    print()

    print("PART (e) - MODULE 4: STRASSEN MULTIPLICATION")
    a = [[1, 7], [3, 5]]
    b = [[1, 3], [7, 5]]
    classical_stats = MatrixStats()
    strassen_stats = MatrixStats()
    print("A:", a)
    print("B:", b)
    print("Classical result:", classical_multiply(a, b, classical_stats))
    print("Strassen result:", strassen_multiply(a, b, cutoff=1, stats=strassen_stats))
    print("Classical scalar multiplications:", classical_stats.scalar_multiplications)
    print("Strassen scalar multiplications:", strassen_stats.scalar_multiplications)
    print("Strassen scalar additions/subtractions:", strassen_stats.scalar_additions)


if __name__ == "__main__":
    main()
