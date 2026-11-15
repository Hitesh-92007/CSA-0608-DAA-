"""Reproducible operation-count experiments and graphs for Q1-Q7."""

import csv
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Supporting_Files" / "results"
DATA = ROOT / "Supporting_Files" / "datasets"
RESULTS.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
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

from sorting_algorithms import input_cases, selection_sort, bubble_sort, insertion_sort
from sequential_search import records_of_size, sequential_search
from brute_force_string_matching import run as string_cases
from brute_force_closest_pair import generate_points, closest_pair
from brute_force_convex_hull import convex_hull
from exhaustive_knapsack import generated_packages, exhaustive_knapsack
from closest_pair_redesign import closest_pair_dc


def write_csv(name, rows, header):
    with (RESULTS / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def chart(path, title, series, x_label, y_label):
    width, height = 1000, 620
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    left, top, right, bottom = 95, 80, 950, 520
    draw.text((left, 28), title, fill="#111827", font=font)
    draw.line((left, top, left, bottom, right, bottom), fill="#374151", width=2)
    draw.text((left, bottom + 38), x_label, fill="#111827", font=font)
    draw.text((12, top), y_label, fill="#111827", font=font)
    all_x = [x for _, points, _ in series for x, _ in points]
    all_y = [y for _, points, _ in series for _, y in points]
    xmin, xmax = min(all_x), max(all_x)
    ymax = max(all_y) or 1
    colors = ["#2563eb", "#dc2626", "#059669", "#9333ea"]
    if len(set(all_x)) <= 8:
        x_ticks = sorted(set(all_x))
    else:
        x_ticks = [xmin + (xmax - xmin) * tick / 4 for tick in range(5)]
    for tick in range(6):
        y = bottom - tick * (bottom - top) // 5
        value = ymax * tick / 5
        draw.line((left, y, right, y), fill="#e5e7eb", width=1)
        draw.text((42, y - 6), f"{value:.0f}", fill="#4b5563", font=font)
    for value in x_ticks:
        x = left + (value - xmin) / (xmax - xmin or 1) * (right - left)
        draw.line((int(x), bottom - 3, int(x), bottom + 4), fill="#374151", width=1)
        draw.text((int(x) - 10, bottom + 8), f"{value:.0f}", fill="#4b5563", font=font)
    for sidx, (label, points, color_index) in enumerate(series):
        color = colors[color_index % len(colors)]
        mapped = []
        for x, y in points:
            px = left + (x - xmin) / (xmax - xmin or 1) * (right - left)
            py = bottom - y / ymax * (bottom - top)
            mapped.append((int(px), int(py)))
        if len(mapped) > 1:
            draw.line(mapped, fill=color, width=4)
        for px, py in mapped:
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=color)
        draw.text((left + 190 * sidx, 57), label, fill=color, font=font)
    image.save(path)


def main():
    # Q1: deliberately contrasting input structures and a small edge case.
    q1_rows = []
    q1_cases = input_cases()
    q1_algorithms = [("Selection", selection_sort), ("Bubble", bubble_sort),
                     ("Insertion", insertion_sort)]
    for case, values in q1_cases.items():
        for name, fn in q1_algorithms:
            result, m = fn(values)
            assert result == sorted(values)
            q1_rows.append([case, len(values), name, m["comparisons"],
                            m["swaps"], m["moves"], f"{m['seconds']:.8f}"])
    write_csv("q1_sorting_results.csv", q1_rows,
              ["case", "n", "algorithm", "comparisons", "swaps", "moves", "seconds"])

    # Q2: all four positions/conditions at growing list sizes.
    q2_rows = []
    for n in (10, 100, 1_000, 10_000):
        records = records_of_size(n)
        cases = [("first", "T-000000"), ("middle", f"T-{n//2:06d}"),
                 ("last", f"T-{n-1:06d}"), ("unsuccessful", "T-ABSENT")]
        for case, target in cases:
            index, comparisons = sequential_search(records, target)
            q2_rows.append([n, case, index, comparisons])
    write_csv("q2_sequential_search_results.csv", q2_rows,
              ["list_size", "case", "returned_index", "comparisons"])

    # Q3: structured signatures, including a worst-case late match.
    q3_rows = [[name, n, m, repr(matches), comparisons]
               for name, n, m, matches, comparisons in string_cases()]
    write_csv("q3_string_matching_results.csv", q3_rows,
              ["case", "text_length", "pattern_length", "match_positions", "comparisons"])

    # Q4 and Q7: identical point sets and an exact distance-count comparison.
    q4_rows, q7_rows = [], []
    for n in (100, 300, 600, 1_000, 2_000):
        points = generate_points(n)
        pair, distance, count, seconds = closest_pair(points)
        q4_rows.append([n, count, f"{distance:.10f}", f"{seconds:.8f}"])
        dc_pair, dc_distance, dc_count, dc_seconds = closest_pair_dc(points)
        q7_rows.append([n, count, dc_count, f"{distance:.10f}",
                        f"{dc_distance:.10f}", f"{seconds:.8f}",
                        f"{dc_seconds:.8f}", f"{100*(1-dc_count/count):.4f}"])
    write_csv("q4_brute_closest_pair_results.csv", q4_rows,
              ["n", "distance_calculations", "minimum_distance", "seconds"])
    write_csv("q7_redesign_comparison.csv", q7_rows,
              ["n", "brute_distance_calculations", "dc_distance_calculations",
               "brute_distance", "dc_distance", "brute_seconds", "dc_seconds",
               "distance_calculation_reduction_percent"])

    # Q5: measure the geometric tests on several point counts on a circle.
    q5_rows = []
    for n in (12, 24, 48, 72, 96):
        points = [(round(100 * math.cos(2 * math.pi * i / n), 8),
                   round(100 * math.sin(2 * math.pi * i / n), 8)) for i in range(n)]
        hull, orientations, candidates = convex_hull(points)
        q5_rows.append([n, candidates, orientations, len(hull)])
    write_csv("q5_convex_hull_results.csv", q5_rows,
              ["points", "candidate_pairs", "orientation_tests", "hull_vertices"])

    # Q6: subset space and item checks grow exponentially.
    q6_rows = []
    for n in (8, 12, 16, 18, 20):
        packages = generated_packages(n)
        capacity = sum(p["weight"] for p in packages) // 2
        result = exhaustive_knapsack(packages, capacity)
        q6_rows.append([n, result["candidate_subsets"], result["item_checks"],
                        result["weight"], result["value"], f"{result['seconds']:.8f}"])
    write_csv("q6_exhaustive_search_results.csv", q6_rows,
              ["packages", "candidate_subsets", "item_checks", "best_weight",
               "best_value", "seconds"])

    # Save representative inputs exactly as used.
    rng = random.Random(6102)
    representative = {
        "Q1_cases": {k: v for k, v in q1_cases.items()},
        "Q3": [{"name": "easy", "text": "AUTH_FAIL: other log entries",
                "pattern": "AUTH_FAIL"},
               {"name": "late near-match", "text": "A" * 5000 + "B",
                "pattern": "A" * 49 + "B"},
               {"name": "overlap", "text": "ABABABA", "pattern": "ABA"}],
        "Q4_and_Q7_note": "Generated by brute_force_closest_pair.generate_points with seed=604.",
        "Q5": [[[0, 0], [4, 0], [4, 4], [0, 4], [2, 2], [1, 2]],
               [[0, 0], [2, 0], [4, 0], [4, 3], [0, 3], [2, 1], [0, 0]]],
        "Q6_sample": [{"id": "A", "weight": 10, "value": 60},
                      {"id": "B", "weight": 5, "value": 40},
                      {"id": "C", "weight": 6, "value": 30},
                      {"id": "D", "weight": 4, "value": 20}],
        "Q6_growth_seed": 8801,
        "Q2": "Tool IDs are T-000000 through T-(n-1), with TECH and BAY fields generated by sequential_search.records_of_size.",
    }
    (DATA / "test_datasets.json").write_text(
        json.dumps(representative, indent=2), encoding="utf-8")

    major_cases = ["random_800", "95pct_ordered_plus_40_arrivals", "reverse_800"]
    chart(RESULTS / "q1_sorting_comparisons.png", "Q1 - Comparisons by input arrangement",
          [(name, [(index + 1, next(int(r[3]) for r in q1_rows
                                    if r[0] == case and r[2] == name))
                   for index, case in enumerate(major_cases)], index)
           for index, name in enumerate(("Selection", "Bubble", "Insertion"))],
          "case 1=random, 2=95% ordered + arrivals, 3=reverse", "comparisons")
    chart(RESULTS / "q4_q7_distance_calculations.png",
          "Q4 vs Q7 - Closest-pair distance calculations",
          [("Brute force", [(r[0], r[1]) for r in q7_rows], 0),
           ("Divide and conquer", [(r[0], r[2]) for r in q7_rows], 1)],
          "number of points", "distance calculations")
    chart(RESULTS / "q6_subset_growth.png", "Q6 - Exhaustive candidate subsets",
          [("2^n subsets", [(r[0], r[1]) for r in q6_rows], 2)],
          "number of packages", "subsets")
    chart(RESULTS / "q5_orientation_growth.png", "Q5 - Observed orientation tests",
          [("measured tests", [(r[0], r[2]) for r in q5_rows], 3)],
          "number of points", "orientation tests")

    summary = [
        "CO2 assignment experiment run",
        f"Q1 rows: {len(q1_rows)}; inputs: {len(q1_cases)}",
        f"Q2 rows: {len(q2_rows)}",
        f"Q3 rows: {len(q3_rows)}",
        f"Q4 sizes: {[r[0] for r in q4_rows]}",
        f"Q5 sizes: {[r[0] for r in q5_rows]}",
        f"Q6 sizes: {[r[0] for r in q6_rows]}",
        f"Q7 brute distance counts: {[r[1] for r in q7_rows]}",
        f"Q7 D&C distance counts: {[r[2] for r in q7_rows]}",
        "CSV files and PNG graphs were written to Supporting_Files/results.",
    ]
    (RESULTS / "experiment_run.txt").write_text("\n".join(summary) + "\n",
                                                 encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
