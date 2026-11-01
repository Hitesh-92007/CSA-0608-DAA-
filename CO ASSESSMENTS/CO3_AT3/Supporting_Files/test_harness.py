"""Deterministic tests for the four CO3 case-study algorithms."""

from __future__ import annotations

import random
import sys
import unittest
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
from quick_sort_baseline import QuickSortStats as BaselineStats, first_pivot_partition, quick_sort_first_pivot
from binary_search import SearchStats, first_order_at_timestamp
from strassen import MatrixStats, classical_multiply, strassen_multiply


class MergeSortTests(unittest.TestCase):
    def test_sample_sorted_and_stable(self):
        stats = SortStats()
        result = merge_sort(SAMPLE_ORDERS, key=lambda row: row[0], stats=stats)
        self.assertEqual(result, [(101, "O4"), (102, "O2"), (102, "O5"),
                                  (103, "O6"), (105, "O1"), (105, "O3")])
        self.assertLess(result.index((102, "O2")), result.index((102, "O5")))
        self.assertLess(result.index((105, "O1")), result.index((105, "O3")))
        self.assertGreater(stats.key_comparisons, 0)

    def test_empty_single_and_input_preserved(self):
        self.assertEqual(merge_sort([], key=lambda x: x), [])
        self.assertEqual(merge_sort([4], key=lambda x: x), [4])
        sample = [(2, "a"), (1, "b")]
        original = sample[:]
        merge_sort(sample, key=lambda row: row[0])
        self.assertEqual(sample, original)

    def test_randomized_against_builtin_stable_sort(self):
        rng = random.Random(3101)
        for _ in range(100):
            data = [(rng.randrange(8), index) for index in range(rng.randrange(40))]
            self.assertEqual(merge_sort(data, key=lambda row: row[0]),
                             sorted(data, key=lambda row: row[0]))


class QuickSortTests(unittest.TestCase):
    def test_first_pivot_sample_partition(self):
        stats = BaselineStats()
        partitioned, pivot_index = first_pivot_partition([42, 17, 63, 8, 55, 29], stats)
        self.assertEqual(partitioned, [29, 17, 8, 42, 55, 63])
        self.assertEqual(pivot_index, 3)
        self.assertEqual(stats.comparisons, 5)

    def test_baseline_and_optimized_sort(self):
        ordered = list(range(1000))
        baseline_stats = BaselineStats()
        self.assertEqual(quick_sort_first_pivot(ordered, baseline_stats), ordered)
        self.assertEqual(baseline_stats.comparisons, 1000 * 999 // 2)
        self.assertEqual(quick_sort([], stats=QuickSortStats()), [])
        self.assertEqual(quick_sort([3], stats=QuickSortStats()), [3])
        self.assertEqual(quick_sort([5, 5, 5, 2, 5, 1]), [1, 2, 5, 5, 5, 5])
        self.assertEqual(quick_sort(list(range(1000, -1, -1))), list(range(1001)))

    def test_optimized_randomized_against_builtin(self):
        rng = random.Random(3102)
        for _ in range(150):
            values = [rng.randrange(-20, 21) for _ in range(rng.randrange(100))]
            self.assertEqual(quick_sort(values), sorted(values))

    def test_heap_fallback_is_used_at_depth_limit(self):
        stats = QuickSortStats()
        self.assertEqual(quick_sort([8, 2, 6, 1, 4], cutoff=1,
                                    depth_limit=0, stats=stats), [1, 2, 4, 6, 8])
        self.assertEqual(stats.heap_fallbacks, 1)


class BinarySearchTests(unittest.TestCase):
    def setUp(self):
        self.orders = merge_sort(SAMPLE_ORDERS, key=lambda row: row[0])

    def test_first_duplicate_and_comparison_count(self):
        stats = SearchStats()
        self.assertEqual(first_order_at_timestamp(self.orders, 102, stats), 1)
        self.assertEqual(self.orders[1], (102, "O2"))
        self.assertGreater(stats.timestamp_comparisons, 0)

    def test_missing_and_boundaries(self):
        self.assertIsNone(first_order_at_timestamp(self.orders, 100))
        self.assertIsNone(first_order_at_timestamp(self.orders, 106))
        self.assertEqual(first_order_at_timestamp(self.orders, 101), 0)
        self.assertEqual(first_order_at_timestamp(self.orders, 105), 4)
        self.assertIsNone(first_order_at_timestamp([], 5))


class StrassenTests(unittest.TestCase):
    def test_given_matrices_and_operation_counts(self):
        a = [[1, 7], [3, 5]]
        b = [[1, 3], [7, 5]]
        expected = [[50, 38], [38, 34]]
        classical_stats = MatrixStats()
        strassen_stats = MatrixStats()
        self.assertEqual(classical_multiply(a, b, classical_stats), expected)
        self.assertEqual(strassen_multiply(a, b, cutoff=1, stats=strassen_stats), expected)
        self.assertEqual(classical_stats.scalar_multiplications, 8)
        self.assertEqual(strassen_stats.scalar_multiplications, 7)

    def test_padding_and_randomized_equivalence(self):
        rng = random.Random(3104)
        for n in range(1, 9):
            a = [[rng.randrange(-5, 6) for _ in range(n)] for _ in range(n)]
            b = [[rng.randrange(-5, 6) for _ in range(n)] for _ in range(n)]
            self.assertEqual(strassen_multiply(a, b, cutoff=2), classical_multiply(a, b))
        self.assertEqual(strassen_multiply([], []), [])

    def test_rejects_non_square(self):
        with self.assertRaises(ValueError):
            strassen_multiply([[1, 2]], [[3, 4]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
