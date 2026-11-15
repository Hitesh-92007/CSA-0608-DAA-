"""Sequential search over changing tool records for CO2 Q2."""

from time import perf_counter


def sequential_search(records, target_id):
    comparisons = 0
    for index, record in enumerate(records):
        comparisons += 1
        if record["tool_id"] == target_id:
            return index, comparisons
    return -1, comparisons


def records_of_size(size):
    return [{"tool_id": f"T-{i:06d}", "technician": f"TECH-{i % 80:03d}",
             "issue_time": f"09:{i % 60:02d}", "work_bay": f"BAY-{i % 12:02d}"}
            for i in range(size)]


def run():
    rows = []
    for size in (10, 100, 1_000, 10_000):
        records = records_of_size(size)
        targets = (
            ("first", "T-000000"),
            ("middle", f"T-{size // 2:06d}"),
            ("last", f"T-{size - 1:06d}"),
            ("missing", "T-MISSING"),
        )
        for case, target in targets:
            start = perf_counter()
            index, comparisons = sequential_search(records, target)
            elapsed = perf_counter() - start
            rows.append((size, case, index, comparisons, elapsed))
    return rows


if __name__ == "__main__":
    print("n      case       index      comparisons      time")
    for n, case, index, comparisons, seconds in run():
        print(f"{n:<6} {case:<10} {index:>5} {comparisons:>14} "
              f"{seconds:>12.8f}s")
