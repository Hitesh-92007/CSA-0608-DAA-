"""Repeatable distance and insertion-sort comparison-count experiments."""
import csv
import random
import time
from pathlib import Path

import corrected_module
import optimized_module
from optimized_module import DistanceCounter


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "Supporting_Files"
SUPPORT.mkdir(exist_ok=True)


def insertion_sort_count(records):
    """Run corrected insertion sort and count severity-key comparisons."""
    data = records.copy()
    comparisons = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if data[j][1] < key[1]:
                data[j + 1] = data[j]
                j -= 1
            else:
                break
        data[j + 1] = key
    return data, comparisons


def timed(callable_):
    start = time.perf_counter()
    result = callable_()
    return result, (time.perf_counter() - start) * 1000


def main():
    seed = 20261026
    rng = random.Random(seed)
    events_all = [(rng.random() * 10000, rng.random() * 10000) for _ in range(8000)]
    with (SUPPORT / "closest_pair_points.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(("index", "x_km", "y_km"))
        writer.writerows((i, f"{x:.12f}", f"{y:.12f}") for i, (x, y) in enumerate(events_all))
    distance_rows = []
    for size in (1000, 4000, 8000):
        events = events_all[:size]
        brute_counter = DistanceCounter()
        (brute_result, brute_ms) = timed(lambda: optimized_module.closest_logins_bruteforce(events, brute_counter))
        fast_counter = DistanceCounter()
        (fast_result, fast_ms) = timed(lambda: optimized_module.closest_logins(events, fast_counter))
        assert brute_result[0] == fast_result[0]
        assert abs(brute_result[1] - fast_result[1]) < 1e-9
        distance_rows.append({
            "events": size,
            "bruteforce_distance_evaluations": brute_counter.evaluations,
            "optimized_distance_evaluations": fast_counter.evaluations,
            "reduction_percent": round(100 * (1 - fast_counter.evaluations / brute_counter.evaluations), 4),
            "bruteforce_milliseconds": round(brute_ms, 3),
            "optimized_milliseconds": round(fast_ms, 3),
            "matching_pair": str(fast_result[0]),
            "distance": f"{fast_result[1]:.9f}",
        })

    n = 5000
    nearly = [(f"N{i}", n - i) for i in range(n)]
    # Insert 100 adjacent inversions: still mostly descending, but not perfectly sorted.
    for i in range(25, n - 1, 50):
        nearly[i], nearly[i + 1] = nearly[i + 1], nearly[i]
    random_severities = list(range(n))
    rng.shuffle(random_severities)
    random_alerts = [(f"R{i}", value) for i, value in enumerate(random_severities)]

    sort_rows = []
    for label, records in (("nearly_sorted", nearly), ("random", random_alerts)):
        insertion_result, insertion_comparisons = insertion_sort_count(records)
        (_, insertion_ms) = timed(lambda: corrected_module.sort_alerts(records.copy()))
        timsort_result, timsort_ms = timed(lambda: optimized_module.sort_alerts(records.copy()))
        assert insertion_result == timsort_result
        sort_rows.append({
            "dataset": label,
            "alerts": n,
            "insertion_key_comparisons": insertion_comparisons,
            "insertion_milliseconds": round(insertion_ms, 3),
            "timsort_milliseconds": round(timsort_ms, 3),
            "outputs_match": True,
        })

    with (SUPPORT / "distance_experiments.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(distance_rows[0]))
        writer.writeheader()
        writer.writerows(distance_rows)
    with (SUPPORT / "sort_experiments.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sort_rows[0]))
        writer.writeheader()
        writer.writerows(sort_rows)

    print(f"Python random seed: {seed}")
    print("Closest-pair experiment: one measured run per version and size")
    print("events | brute evals | optimized evals | reduction | brute ms | optimized ms | pair | distance")
    for row in distance_rows:
        print(f"{row['events']:>6} | {row['bruteforce_distance_evaluations']:>11} | "
              f"{row['optimized_distance_evaluations']:>15} | {row['reduction_percent']:>9.4f}% | "
              f"{row['bruteforce_milliseconds']:>8.3f} | {row['optimized_milliseconds']:>12.3f} | "
              f"{row['matching_pair']:>13} | {row['distance']}")
    print("Insertion sort comparison test: n=5000")
    print("input         | insertion comps | insertion ms | Timsort ms | same output")
    for row in sort_rows:
        print(f"{row['dataset']:<13} | {row['insertion_key_comparisons']:>15} | "
              f"{row['insertion_milliseconds']:>12.3f} | {row['timsort_milliseconds']:>10.3f} | "
              f"{row['outputs_match']}")
    print("CSV files: Supporting_Files/distance_experiments.csv, Supporting_Files/sort_experiments.csv")


if __name__ == "__main__":
    main()
