"""Correctness checks for the seven CO2 assignment algorithms."""

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for folder in (
    "Q1_Sorting_Algorithms/Implementation_Code",
    "Q2_Sequential_Search/Implementation_Code",
    "Q3_Brute_Force_String_Matching/Implementation_Code",
    "Q4_Brute_Force_Closest_Pair/Implementation_Code",
    "Q5_Brute_Force_Convex_Hull/Implementation_Code",
    "Q6_Exhaustive_Search/Implementation_Code",
    "Q7_Day4_Design_Challenge/Implementation_Code",
):
    sys.path.insert(0, str(ROOT / folder))

from sorting_algorithms import selection_sort, bubble_sort, insertion_sort
from sequential_search import sequential_search, records_of_size
from brute_force_string_matching import brute_force_match
from brute_force_closest_pair import closest_pair
from brute_force_convex_hull import convex_hull
from exhaustive_knapsack import exhaustive_knapsack, sample_packages
from closest_pair_redesign import closest_pair_dc


class AssignmentTests(unittest.TestCase):
    def test_all_sorts_against_builtin(self):
        rng = random.Random(72)
        for algorithm in (selection_sort, bubble_sort, insertion_sort):
            for values in ([], [1], [2, 1], [3, 3, -1], rng.choices(range(20), k=40)):
                result, _ = algorithm(values)
                self.assertEqual(result, sorted(values))

    def test_sequential_search_positions_and_miss(self):
        records = records_of_size(7)
        self.assertEqual(sequential_search(records, "T-000000"), (0, 1))
        self.assertEqual(sequential_search(records, "T-000003"), (3, 4))
        self.assertEqual(sequential_search(records, "T-000006"), (6, 7))
        self.assertEqual(sequential_search(records, "missing"), (-1, 7))
        self.assertEqual(sequential_search([], "missing"), (-1, 0))

    def test_string_matching_overlaps_and_edges(self):
        self.assertEqual(brute_force_match("ABABABA", "ABA")[0], [0, 2, 4])
        self.assertEqual(brute_force_match("abc", "long")[0], [])
        self.assertEqual(brute_force_match("abc", "")[0], [0, 1, 2, 3])

    def test_brute_force_closest_pair(self):
        pair, distance, count, _ = closest_pair([(0, 0), (5, 5), (1, 1)])
        self.assertEqual(pair, (0, 2))
        self.assertAlmostEqual(distance, 2 ** 0.5)
        self.assertEqual(count, 3)

    def test_convex_hull_boundary_and_collinear(self):
        hull, _, _ = convex_hull([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)])
        self.assertEqual(set(hull), {(0, 0), (4, 0), (4, 4), (0, 4)})
        hull, _, _ = convex_hull([(0, 0), (1, 1), (3, 3), (2, 2)])
        self.assertEqual(set(hull), {(0, 0), (3, 3)})

    def test_convex_hull_matches_independent_reference(self):
        def reference(points):
            pts = sorted(set(tuple(p) for p in points))
            if len(pts) <= 1:
                return set(pts)

            def cross(a, b, c):
                return ((b[0] - a[0]) * (c[1] - a[1])
                        - (b[1] - a[1]) * (c[0] - a[0]))

            lower = []
            for point in pts:
                while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
                    lower.pop()
                lower.append(point)
            upper = []
            for point in reversed(pts):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
                    upper.pop()
                upper.append(point)
            return set(lower[:-1] + upper[:-1])

        rng = random.Random(6022)
        for _ in range(60):
            points = [(rng.randrange(-20, 21), rng.randrange(-20, 21))
                      for _ in range(rng.randrange(3, 25))]
            actual, _, _ = convex_hull(points)
            self.assertEqual(set(actual), reference(points))

    def test_exhaustive_knapsack_known_optimum(self):
        result = exhaustive_knapsack(sample_packages(), 15)
        self.assertEqual(result["selected"], ["A", "B"])
        self.assertEqual(result["value"], 100)
        self.assertEqual(result["candidate_subsets"], 16)

    def test_divide_conquer_closest_pair_matches_brute_force(self):
        rng = random.Random(932)
        for size in range(2, 42):
            points = [(rng.random() * 100, rng.random() * 100)
                      for _ in range(size)]
            brute = closest_pair(points)[1]
            divide = closest_pair_dc(points)[1]
            self.assertAlmostEqual(brute, divide, places=10)

    def test_divide_conquer_duplicate_coordinates(self):
        pair, distance, _, _ = closest_pair_dc([(0, 0), (4, 4), (0, 0)])
        self.assertEqual(distance, 0.0)
        self.assertEqual(pair, (0, 2))

    def test_closest_pair_small_inputs(self):
        self.assertEqual(closest_pair_dc([]), (None, None, 0, 0.0))
        self.assertEqual(closest_pair_dc([(3, 4)]), (None, None, 0, 0.0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
