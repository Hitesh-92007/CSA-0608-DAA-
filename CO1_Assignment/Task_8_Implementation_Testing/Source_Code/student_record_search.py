"""CO1 Assignment 1: compare three student-registration lookup strategies.

The benchmark uses synthetic records so it can be reproduced without a real
student database. Only the standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import random
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(slots=True)
class StudentRecord:
    """Small synthetic record used to measure key lookup."""

    registration_number: str
    student_id: int


SearchFunction = Callable[[str], tuple[StudentRecord | None, int]]


def make_records(size: int, seed: int) -> list[StudentRecord]:
    """Create unique registration numbers in a reproducibly shuffled order."""
    if size < 1:
        raise ValueError("Dataset size must be at least 1.")

    student_ids = list(range(size))
    random.Random(seed).shuffle(student_ids)
    width = max(7, len(str(size - 1)))
    return [
        StudentRecord(f"REG{student_id:0{width}d}", student_id)
        for student_id in student_ids
    ]


def linear_search(
    records: list[StudentRecord], target: str
) -> tuple[StudentRecord | None, int]:
    """Iterative sequential search; return the record and key comparisons."""
    comparisons = 0
    for record in records:
        comparisons += 1
        if record.registration_number == target:
            return record, comparisons
    return None, comparisons


def recursive_binary_search(
    sorted_records: list[StudentRecord], target: str
) -> tuple[StudentRecord | None, int]:
    """Recursive divide-and-conquer search over records sorted by key."""
    comparisons = 0

    def search(low: int, high: int) -> StudentRecord | None:
        nonlocal comparisons
        if low > high:
            return None

        middle = (low + high) // 2
        record = sorted_records[middle]
        comparisons += 1
        if record.registration_number == target:
            return record
        comparisons += 1
        if target < record.registration_number:
            return search(low, middle - 1)
        return search(middle + 1, high)

    result = search(0, len(sorted_records) - 1)
    return result, comparisons


def hash_search(
    index: dict[str, StudentRecord], target: str
) -> tuple[StudentRecord | None, int]:
    """Expected constant-time dictionary lookup; count one logical lookup."""
    return index.get(target), 1


def make_queries(
    records: list[StudentRecord], query_count: int, seed: int
) -> list[tuple[str, bool]]:
    """Create an even, reproducible mix of unique hits and absent keys."""
    if query_count < 2 or query_count % 2:
        raise ValueError("Query count must be an even number of at least 2.")

    randomizer = random.Random(seed)
    hit_count = query_count // 2
    chosen_records = randomizer.sample(records, hit_count)
    queries = [
        (record.registration_number, True) for record in chosen_records
    ]
    queries.extend(
        (f"MISSING-{seed:04d}-{number:07d}", False)
        for number in range(query_count - hit_count)
    )
    randomizer.shuffle(queries)
    return queries


def measure_search(
    search: SearchFunction,
    queries: list[tuple[str, bool]],
    repeats: int,
) -> tuple[float, float]:
    """Return median batch time in ms and mean logical operations per query."""
    elapsed_samples: list[int] = []
    operation_samples: list[int] = []

    for _ in range(repeats):
        found_keys: list[str | None] = []
        total_operations = 0
        start = time.perf_counter_ns()
        for target, _expected_found in queries:
            record, operations = search(target)
            found_keys.append(record.registration_number if record else None)
            total_operations += operations
        elapsed_samples.append(time.perf_counter_ns() - start)
        operation_samples.append(total_operations)

        for (target, expected_found), found_key in zip(queries, found_keys):
            if (found_key is not None) != expected_found:
                raise AssertionError(f"Incorrect found/not-found result for {target}.")
            if expected_found and found_key != target:
                raise AssertionError(f"Wrong record returned for {target}.")

    median_ms = statistics.median(elapsed_samples) / 1_000_000
    mean_operations = statistics.mean(operation_samples) / len(queries)
    return median_ms, mean_operations


def check_edge_cases(
    records: list[StudentRecord],
    sorted_records: list[StudentRecord],
    hash_index: dict[str, StudentRecord],
) -> None:
    """Check first, last and absent keys outside the timed benchmark."""
    searches: tuple[SearchFunction, ...] = (
        lambda key: linear_search(records, key),
        lambda key: recursive_binary_search(sorted_records, key),
        lambda key: hash_search(hash_index, key),
    )
    expected_records = (records[0], records[-1], None)
    test_keys = (
        records[0].registration_number,
        records[-1].registration_number,
        "MISSING-EDGE-CASE",
    )

    for search in searches:
        for target, expected in zip(test_keys, expected_records):
            result, _operations = search(target)
            expected_key = expected.registration_number if expected else None
            actual_key = result.registration_number if result else None
            if actual_key != expected_key:
                raise AssertionError(f"Edge-case check failed for {target}.")


def benchmark_size(
    size: int, query_count: int, repeats: int, seed: int
) -> tuple[list[dict[str, object]], StudentRecord]:
    records = make_records(size, seed + size)
    queries = make_queries(records, query_count, seed + size * 2)

    start = time.perf_counter_ns()
    sorted_records = sorted(records, key=lambda record: record.registration_number)
    sort_ms = (time.perf_counter_ns() - start) / 1_000_000

    start = time.perf_counter_ns()
    hash_index = {record.registration_number: record for record in records}
    hash_build_ms = (time.perf_counter_ns() - start) / 1_000_000

    check_edge_cases(records, sorted_records, hash_index)

    search_functions: tuple[tuple[str, SearchFunction, float], ...] = (
        (
            "Iterative linear search",
            lambda key: linear_search(records, key),
            0.0,
        ),
        (
            "Recursive binary search",
            lambda key: recursive_binary_search(sorted_records, key),
            sort_ms,
        ),
        (
            "Hash table lookup",
            lambda key: hash_search(hash_index, key),
            hash_build_ms,
        ),
    )

    rows: list[dict[str, object]] = []
    for name, search, preprocess_ms in search_functions:
        search_ms, operations_per_query = measure_search(search, queries, repeats)
        rows.append(
            {
                "input_size": size,
                "algorithm": name,
                "queries": query_count,
                "hit_rate_percent": 50,
                "preprocessing_ms": round(preprocess_ms, 6),
                "search_batch_median_ms": round(search_ms, 6),
                "mean_dominant_operations_per_query": round(operations_per_query, 3),
                "repeats": repeats,
                "seed": seed,
                "correct": True,
            }
        )

    example_target = next(target for target, expected in queries if expected)
    example_record = hash_index[example_target]
    return rows, example_record


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare linear, recursive binary and hash-table search."
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[1_000, 10_000, 100_000, 1_000_000],
        help="dataset sizes (default: 1000 10000 100000 1000000)",
    )
    parser.add_argument(
        "--queries", type=int, default=32, help="even query count per size"
    )
    parser.add_argument("--repeats", type=int, default=3, help="timing repetitions")
    parser.add_argument("--seed", type=int, default=2026, help="random seed")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parents[2]
        / "Report"
        / "Tables_and_Graphs"
        / "benchmark_results.csv",
        help="output CSV path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.repeats < 1:
        raise ValueError("Repeats must be at least 1.")
    if any(size < 1 for size in args.sizes):
        raise ValueError("All dataset sizes must be at least 1.")

    all_rows: list[dict[str, object]] = []
    example_record: StudentRecord | None = None
    for size in args.sizes:
        rows, example_record = benchmark_size(
            size, args.queries, args.repeats, args.seed
        )
        all_rows.extend(rows)

    output_path = args.csv.resolve()
    write_csv(all_rows, output_path)
    print("Student record search benchmark")
    print(
        f"Queries per size: {args.queries} (50% found, 50% absent); "
        f"timing repeats: {args.repeats}; seed: {args.seed}"
    )
    print("Times are medians for a complete query batch; preprocessing is separate.")
    print(
        f"{'n':>10}  {'algorithm':<28} {'prep ms':>11} "
        f"{'search ms':>12} {'ops/query':>12} {'correct':>9}"
    )
    for row in all_rows:
        print(
            f"{row['input_size']:>10,}  {row['algorithm']:<28} "
            f"{row['preprocessing_ms']:>11.3f} "
            f"{row['search_batch_median_ms']:>12.3f} "
            f"{row['mean_dominant_operations_per_query']:>12.3f} "
            f"{str(row['correct']):>9}"
        )
    if example_record is not None:
        print(
            "Example retrieved record: "
            f"{example_record.registration_number} | "
            f"Student {example_record.student_id:07d}"
        )
        try:
            display_path = output_path.relative_to(Path(__file__).resolve().parents[1])
        except ValueError:
            display_path = Path(output_path.name)
        print(f"CSV saved to: {display_path.as_posix()}")


if __name__ == "__main__":
    main()
