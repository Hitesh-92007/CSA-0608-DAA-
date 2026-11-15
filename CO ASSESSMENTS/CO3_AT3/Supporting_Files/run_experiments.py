"""Reproduce scale experiments and production operation-count calculations."""

from __future__ import annotations

import csv
import random
import sys
import time
from math import ceil, log2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Supporting_Files" / "results"
DATASETS = ROOT / "Supporting_Files" / "datasets"
RESULTS.mkdir(parents=True, exist_ok=True)
DATASETS.mkdir(parents=True, exist_ok=True)
for module_dir in (
    "Module_1_Merge_Sort/Source_Code",
    "Module_2_Quick_Sort/Source_Code",
    "Module_3_Binary_Search/Source_Code",
    "Module_4_Strassen_Matrix_Multiplication/Source_Code",
):
    sys.path.insert(0, str(ROOT / module_dir))

from merge_sort import SortStats, merge_sort
from quick_sort import QuickSortStats, quick_sort
from quick_sort_baseline import QuickSortStats as BaselineStats, quick_sort_first_pivot
from strassen import MatrixStats, classical_multiply, strassen_multiply


def nearly_sorted_scores(n: int, swaps: int = 100) -> list[int]:
    values = list(range(n))
    if n < 2:
        return values
    actual_swaps = min(swaps, n - 1)
    for index in range(actual_swaps):
        position = ((index + 1) * (n - 1)) // (actual_swaps + 1)
        values[position], values[position + 1] = values[position + 1], values[position]
    return values


def timed(function):
    start = time.perf_counter()
    result = function()
    return result, (time.perf_counter() - start) * 1000


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def strassen_count(n: int, cutoff: int) -> tuple[int, int, int]:
    """Return (scalar multiplies, scalar adds/subtracts, leaf calls)."""
    if n <= cutoff:
        return n**3, n * n * (n - 1), 1
    sub_m, sub_a, sub_leaves = strassen_count(n // 2, cutoff)
    return 7 * sub_m, 7 * sub_a + 18 * (n // 2) ** 2, 7 * sub_leaves


def sorting_experiments() -> list[dict]:
    rng = random.Random(20261031)
    cases: list[tuple[str, list[int]]] = []
    for n in (1_000, 5_000, 20_000, 100_000):
        cases.append(("nearly_sorted_100_adjacent_swaps", nearly_sorted_scores(n, 100)))
    for n in (1_000, 5_000, 20_000):
        values = list(range(n))
        rng.shuffle(values)
        cases.append(("seeded_random", values))

    rows: list[dict] = []
    for distribution, values in cases:
        merge_stats = SortStats()
        quick_stats = QuickSortStats()
        expected = sorted(values)
        merge_result, merge_ms = timed(
            lambda: merge_sort(values, key=lambda value: value, stats=merge_stats))
        quick_result, quick_ms = timed(
            lambda: quick_sort(values, stats=quick_stats))
        if merge_result != expected or quick_result != expected:
            raise AssertionError(f"sort output mismatch for {distribution}, n={len(values)}")

        baseline_count = "not measured at this size"
        baseline_ms: str | float = ""
        # This upper-scale baseline is only run on a modest case; the 100,000
        # ordered-score count is derived from the exact recurrence below.
        if len(values) <= 5_000 and distribution.startswith("nearly_sorted"):
            baseline_stats = BaselineStats()
            baseline_result, baseline_ms = timed(
                lambda: quick_sort_first_pivot(values, baseline_stats))
            if baseline_result != expected:
                raise AssertionError("first-pivot baseline output mismatch")
            baseline_count = baseline_stats.comparisons

        rows.append({
            "n": len(values),
            "distribution": distribution,
            "merge_key_comparisons": merge_stats.key_comparisons,
            "merge_ms": f"{merge_ms:.3f}",
            "guarded_quick_comparisons": quick_stats.comparisons,
            "guarded_quick_ms": f"{quick_ms:.3f}",
            "guarded_partitions": quick_stats.partitions,
            "heap_fallbacks": quick_stats.heap_fallbacks,
            "first_pivot_measured_comparisons": baseline_count,
            "first_pivot_ms": f"{baseline_ms:.3f}" if baseline_ms != "" else "",
            "output_match": True,
        })
    write_csv(RESULTS / "sorting_experiments.csv", rows)

    near_100k = nearly_sorted_scores(100_000, 100)
    with (DATASETS / "nearly_sorted_seller_scores_100k.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["seller_position", "score"])
        writer.writerows(enumerate(near_100k))
    return rows


def matrix_experiments() -> list[dict]:
    rng = random.Random(20261032)
    rows = []
    for n in (16, 32, 64, 128):
        a = [[rng.randrange(10) for _ in range(n)] for _ in range(n)]
        b = [[rng.randrange(10) for _ in range(n)] for _ in range(n)]
        classical_stats = MatrixStats()
        strassen_stats = MatrixStats()
        classical, classical_ms = timed(lambda: classical_multiply(a, b, classical_stats))
        hybrid, hybrid_ms = timed(
            lambda: strassen_multiply(a, b, cutoff=32, stats=strassen_stats))
        if classical != hybrid:
            raise AssertionError(f"matrix output mismatch for n={n}")
        rows.append({
            "n": n,
            "cutoff": 32,
            "classical_multiplications": classical_stats.scalar_multiplications,
            "hybrid_strassen_multiplications": strassen_stats.scalar_multiplications,
            "hybrid_additions_subtractions": strassen_stats.scalar_additions,
            "multiplication_reduction_percent": f"{(1 - strassen_stats.scalar_multiplications / classical_stats.scalar_multiplications) * 100:.2f}",
            "classical_ms": f"{classical_ms:.3f}",
            "hybrid_strassen_ms": f"{hybrid_ms:.3f}",
            "outputs_match": True,
        })
    write_csv(RESULTS / "matrix_experiments.csv", rows)

    production_rows = []
    n = 1_024
    for cutoff, label in ((1, "pure_strassen"), (64, "hybrid_cutoff_64")):
        multiply_count, addition_count, leaves = strassen_count(n, cutoff)
        production_rows.append({
            "n": n,
            "method": label,
            "cutoff": cutoff,
            "scalar_multiplications": multiply_count,
            "scalar_additions_subtractions": addition_count,
            "classical_multiplications": n**3,
            "reduction_vs_classical_percent": f"{(1 - multiply_count / (n**3)) * 100:.4f}",
            "classical_leaf_calls": leaves,
        })
    write_csv(RESULTS / "matrix_production_counts.csv", production_rows)
    return rows


def main() -> None:
    sorting = sorting_experiments()
    matrix = matrix_experiments()
    n_orders = 10_000_000
    merge_worst = n_orders * ceil(log2(n_orders)) - 2 ** ceil(log2(n_orders)) + 1
    first_pivot_sorted = 100_000 * 99_999 // 2
    binary_probes = ceil(log2(n_orders + 1))
    with (RESULTS / "production_calculations.txt").open("w", encoding="utf-8") as stream:
        stream.write(f"merge_sort_n_log2_n_scale={n_orders * log2(n_orders):.0f}\n")
        stream.write(f"merge_sort_worst_comparisons={merge_worst}\n")
        stream.write(f"first_pivot_quick_sort_sorted_100k={first_pivot_sorted}\n")
        stream.write(f"balanced_quick_sort_n_log2_n_scale={100_000 * log2(100_000):.0f}\n")
        stream.write(f"binary_lower_bound_max_loop_probes={binary_probes}\n")
        stream.write(f"binary_max_key_comparisons_including_final_equality={binary_probes + 1}\n")
        stream.write(f"matrix_classical_1024_multiplies={1_024**3}\n")
        for row in sorting:
            stream.write(f"sorting_{row['n']}_{row['distribution']}_quick_comparisons={row['guarded_quick_comparisons']}\n")
        for row in matrix:
            stream.write(f"matrix_{row['n']}_hybrid_32_ms={row['hybrid_strassen_ms']}\n")
    print("Sorting and matrix experiments completed.")
    print(f"Near-sorted 100,000 seller data: {DATASETS / 'nearly_sorted_seller_scores_100k.csv'}")
    print(f"Production calculations: {RESULTS / 'production_calculations.txt'}")
    print(f"Sorting result rows: {len(sorting)}; matrix result rows: {len(matrix)}")


if __name__ == "__main__":
    main()
