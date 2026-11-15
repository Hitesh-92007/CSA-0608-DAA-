"""Instrumented elementary sorts for CO2 Q1."""

from __future__ import annotations

import random
from time import perf_counter


def selection_sort(values):
    data = list(values)
    comparisons = swaps = moves = 0
    start = perf_counter()
    for i in range(len(data) - 1):
        smallest = i
        for j in range(i + 1, len(data)):
            comparisons += 1
            if data[j] < data[smallest]:
                smallest = j
        if smallest != i:
            data[i], data[smallest] = data[smallest], data[i]
            swaps += 1
            moves += 3
    return data, {"comparisons": comparisons, "swaps": swaps,
                  "moves": moves, "seconds": perf_counter() - start}


def bubble_sort(values):
    data = list(values)
    comparisons = swaps = moves = 0
    start = perf_counter()
    for end in range(len(data) - 1, 0, -1):
        swapped = False
        for j in range(end):
            comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                moves += 3
                swapped = True
        if not swapped:
            break
    return data, {"comparisons": comparisons, "swaps": swaps,
                  "moves": moves, "seconds": perf_counter() - start}


def insertion_sort(values):
    data = list(values)
    comparisons = moves = 0
    start = perf_counter()
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if data[j] <= key:
                break
            data[j + 1] = data[j]
            moves += 1
            j -= 1
        data[j + 1] = key
        moves += 1
    return data, {"comparisons": comparisons, "swaps": 0,
                  "moves": moves, "seconds": perf_counter() - start}


def input_cases(seed=6102):
    rng = random.Random(seed)
    random_data = [rng.randrange(0, 10_000) for _ in range(800)]
    existing = list(range(760))
    arrivals = [rng.randrange(-100, 900) for _ in range(40)]
    nearly_sorted = existing + arrivals
    reverse = list(range(800, 0, -1))
    edge_duplicates = [5, 5, -1, 5, 0, -1, 0, 5]
    return {
        "random_800": random_data,
        "95pct_ordered_plus_40_arrivals": nearly_sorted,
        "reverse_800": reverse,
        "edge_duplicates": edge_duplicates,
        "edge_empty": [],
        "edge_single": [7],
    }


def run():
    algorithms = (("Selection", selection_sort),
                  ("Bubble", bubble_sort),
                  ("Insertion", insertion_sort))
    rows = []
    for case_name, values in input_cases().items():
        for algorithm_name, algorithm in algorithms:
            result, metrics = algorithm(values)
            assert result == sorted(values), f"{algorithm_name} failed {case_name}"
            rows.append((case_name, algorithm_name, len(values), metrics))
    return rows


if __name__ == "__main__":
    for case, algorithm, size, metrics in run():
        print(f"{case:34} {algorithm:9} n={size:4} "
              f"comparisons={metrics['comparisons']:8} "
              f"swaps={metrics['swaps']:7} moves={metrics['moves']:8} "
              f"time={metrics['seconds']:.6f}s")
