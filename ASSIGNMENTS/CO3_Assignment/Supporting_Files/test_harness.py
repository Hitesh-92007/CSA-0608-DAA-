"""Deterministic correctness tests for Q1-Q7."""
from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


q1 = load("q1", "Q1_MaxMin_Binary_Search/Implementation_Code/max_min_binary_search.py")
q2 = load("q2", "Q2_MergeSort_QuickSort/Implementation_Code/sorting_comparison.py")
q3 = load("q3", "Q3_Karatsuba_Multiplication/Implementation_Code/karatsuba_multiplication.py")
q4 = load("q4", "Q4_Strassen_Matrix_Multiplication/Implementation_Code/strassen_comparison.py")
q5 = load("q5", "Q5_Divide_Conquer_Closest_Pair/Implementation_Code/closest_pair_comparison.py")
sys.path.insert(0, str(ROOT / "Q6_Advanced_Divide_Conquer/Median_of_Medians"))
sys.path.insert(0, str(ROOT / "Q6_Advanced_Divide_Conquer/Meet_in_the_Middle"))
from median_of_medians import median_of_medians
from meet_in_the_middle import exhaustive_subset_sum, meet_in_middle
q6 = load("q6", "Q6_Advanced_Divide_Conquer/Implementation_Code/q6_advanced.py")
q7 = load("q7", "Q7_Day4_Design_Challenge/Implementation_Code/day4_challenge.py")


def run() -> list[str]:
    checks: list[str] = []
    rng = random.Random(2026)
    for n in range(1, 51):
        a = [rng.randint(-1000, 1000) for _ in range(n)]
        low, high, comparisons = q1.max_min_divide_conquer(a)
        assert (low, high) == (min(a), max(a)) and comparisons >= 0
        if n == 1: checks.append("Q1 max/min matches Python reference for n=1..50")
        ordered = sorted(a)
        for target in (ordered[0], ordered[-1], 10**6):
            ix, _ = q1.binary_search(ordered, target)
            assert (ix >= 0) == (target in ordered)
        if n == 1: checks.append("Q1 binary search finds endpoints and rejects a missing key")
        ms, _ = q2.merge_sort(a); qs, _ = q2.quick_sort(a)
        assert ms == qs == ordered
        if n == 1: checks.append("Q2 Merge Sort and Quick Sort match sorted reference for n=1..50")
        x = rng.randint(-10**30, 10**30); y = rng.randint(-10**30, 10**30)
        assert q3.karatsuba_multiply(x, y, threshold_digits=4) == x * y == q3.schoolbook_multiply(x, y)
        if n == 1: checks.append("Q3 both multiplication methods match integer product on signed values")
        matrix_size = rng.randint(1, 6)
        ma = [[rng.randint(-5, 5) for _ in range(matrix_size)] for _ in range(matrix_size)]
        mb = [[rng.randint(-5, 5) for _ in range(matrix_size)] for _ in range(matrix_size)]
        assert q4.strassen(ma, mb, cutoff=1) == q4.conventional(ma, mb)
        if n == 1: checks.append("Q4 padded Strassen matches conventional multiplication for sizes 1..6")
        points = [(rng.randint(-10, 10), rng.randint(-10, 10)) for _ in range(max(2, n % 16 + 2))]
        d1, _, _ = q5.brute_force(points); d2, _, _ = q5.divide_conquer(points)
        assert abs(d1 - d2) < 1e-12
        if n == 1: checks.append("Q5 closest-pair divide-and-conquer matches brute force on repeated-coordinate data")
        size = rng.randint(1, 80); values = [rng.randint(-100, 100) for _ in range(size)]; k = rng.randrange(size)
        assert median_of_medians(values, k) == sorted(values)[k]
        assert q6.quickselect(values, k, seed=n) == sorted(values)[k]
        if n == 1: checks.append("Q6 selection methods return the requested order statistic")
        subset_values = [rng.randint(-8, 12) for _ in range(8)]; target = rng.randint(-10, 25)
        a1, _ = meet_in_middle(subset_values, target); a2, _ = exhaustive_subset_sum(subset_values, target)
        assert (a1 is None) == (a2 is None)
        if a1 is not None:
            assert sum(a1) == target
        if n == 1: checks.append("Q6 Meet-in-the-Middle agrees with exhaustive subset-sum feasibility")
        arr = [rng.randint(-20, 20) for _ in range(size)]
        r1 = q7.maximum_subarray_divide_conquer(arr); r2 = q7.maximum_subarray_brute_force(arr)
        assert r1[:3] == r2[:3]
        if n == 1: checks.append("Q7 divide-and-conquer maximum subarray matches brute force")
    # explicit edge cases
    assert q1.max_min_divide_conquer([-4])[:2] == (-4, -4)
    assert q5.divide_conquer([(1, 1), (1, 1)])[0] == 0
    assert q7.maximum_subarray_divide_conquer([-5, -2, -8])[:3] == (-2, 1, 1)
    checks.append("Edge cases: singleton, identical points, and all-negative subarray")
    print(f"{len(checks)} checks passed")
    for item in checks:
        print("[PASS] " + item)
    return checks


if __name__ == "__main__":
    run()
