"""Repeatable operation-count and timing comparisons for Q1-Q7."""
from __future__ import annotations

import csv
import importlib.util
import math
import random
import statistics
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Supporting_Files" / "Experimental_Results"
CHARTS = RESULTS / "Charts"
sys.path.insert(0, str(ROOT / "Q6_Advanced_Divide_Conquer/Median_of_Medians"))
sys.path.insert(0, str(ROOT / "Q6_Advanced_Divide_Conquer/Meet_in_the_Middle"))


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module; spec.loader.exec_module(module)
    return module


q1 = load("q1", "Q1_MaxMin_Binary_Search/Implementation_Code/max_min_binary_search.py")
q2 = load("q2", "Q2_MergeSort_QuickSort/Implementation_Code/sorting_comparison.py")
q3 = load("q3", "Q3_Karatsuba_Multiplication/Implementation_Code/karatsuba_multiplication.py")
q4 = load("q4", "Q4_Strassen_Matrix_Multiplication/Implementation_Code/strassen_comparison.py")
q5 = load("q5", "Q5_Divide_Conquer_Closest_Pair/Implementation_Code/closest_pair_comparison.py")
from median_of_medians import median_of_medians
from meet_in_the_middle import exhaustive_subset_sum, meet_in_middle
q6 = load("q6", "Q6_Advanced_Divide_Conquer/Implementation_Code/q6_advanced.py")
q7 = load("q7", "Q7_Day4_Design_Challenge/Implementation_Code/day4_challenge.py")


def save_csv(name: str, rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def median_time(function, repeats: int = 3) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter(); function(); samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def font(size: int):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def chart(title: str, labels: list[str], series: list[tuple[str, list[float], str]], path: Path,
          log2: bool = False) -> None:
    width, height = 1120, 650
    img = Image.new("RGB", (width, height), "white"); draw = ImageDraw.Draw(img)
    title_font, label_font = font(25), font(15)
    draw.text((60, 24), title, font=title_font, fill="#142b3b")
    left, top, right, bottom = 90, 95, 1060, 535
    transformed = [[math.log2(max(v, 1)) if log2 else float(v) for v in values] for _, values, _ in series]
    max_y = max([1.0] + [v for values in transformed for v in values])
    for k in range(6):
        y = bottom - (bottom - top) * k / 5
        draw.line((left, y, right, y), fill="#dce4eb", width=1)
        draw.text((18, y - 8), f"{max_y*k/5:.0f}", font=label_font, fill="#465868")
    draw.line((left, top, left, bottom), fill="#506575", width=2)
    draw.line((left, bottom, right, bottom), fill="#506575", width=2)
    xs = [left + (right - left) * i / max(1, len(labels) - 1) for i in range(len(labels))]
    for x, label in zip(xs, labels):
        draw.text((x - 18, bottom + 10), label, font=label_font, fill="#344958")
    for label, values, color in series:
        ys = [bottom - (bottom - top) * v / max_y for v in (math.log2(max(x, 1)) for x in values)] if log2 else [bottom - (bottom - top) * v / max_y for v in values]
        pts = list(zip(xs, ys))
        if len(pts) > 1:
            draw.line(pts, fill=color, width=4)
        for x, y in pts:
            draw.ellipse((x-5, y-5, x+5, y+5), fill=color)
    lx = left
    for label, _values, color in series:
        draw.line((lx, 585, lx+28, 585), fill=color, width=4)
        draw.text((lx+35, 574), label, font=label_font, fill="#253a49")
        lx += max(170, len(label)*9+55)
    if log2:
        draw.text((left, 64), "Y-axis uses log2(operation count)", font=label_font, fill="#526575")
    path.parent.mkdir(parents=True, exist_ok=True); img.save(path)


def run_all() -> None:
    rng = random.Random(192524005)
    # Q1: comparison counts for powers of two.
    rows = []
    for n in (8, 16, 32, 64, 128, 256, 512):
        values = [rng.randrange(-10**6, 10**6) for _ in range(n)]
        dc = q1.max_min_divide_conquer(values); naive = q1.max_min_independent(values)
        rows.append({"n": n, "dc_comparisons": dc[2], "independent_comparisons": naive[2], "dc_expected_power2": 3*n//2-2})
    save_csv("q1_max_min_comparisons.csv", rows)
    chart("Q1 max/min comparisons", [str(r["n"]) for r in rows], [
        ("divide and conquer", [r["dc_comparisons"] for r in rows], "#087e8b"),
        ("independent scans", [r["independent_comparisons"] for r in rows], "#ff5a5f")], CHARTS/"q1_comparisons.png")

    # Q2: engineered balanced pivots and sorted last-pivot worst cases.
    rows = []
    for n in (31, 63, 127, 255, 511):
        balanced = q2.balanced_last_pivot_permutation(0, n-1)
        for case, values in (("balanced_last_pivot", balanced), ("ascending_last_pivot", list(range(n)))):
            _, qs = q2.quick_sort(values); _, ms = q2.merge_sort(values)
            partitions = qs["partitions"]
            ratios = [max(a, b)/size for a, b, size in partitions]
            rows.append({"case": case, "n": n, "quick_comparisons": qs["comparisons"],
                         "quick_depth": qs["max_depth"], "merge_comparisons": ms["comparisons"],
                         "merge_depth": ms["max_depth"], "largest_partition_fraction": f"{max(ratios, default=0):.6f}"})
    save_csv("q2_sort_decomposition.csv", rows)
    for case, fname in (("balanced_last_pivot", "q2_balanced_depth.png"), ("ascending_last_pivot", "q2_unbalanced_depth.png")):
        chosen = [r for r in rows if r["case"] == case]
        chart(f"Q2 recursion depth: {case.replace('_', ' ')}", [str(r["n"]) for r in chosen], [
            ("Quick Sort", [r["quick_depth"] for r in chosen], "#087e8b"),
            ("Merge Sort", [r["merge_depth"] for r in chosen], "#ff5a5f")], CHARTS/fname)

    # Q3: schoolbook digit products vs Karatsuba base products and median timings.
    rows = []
    for digits in (8, 16, 24, 32, 48, 64, 96, 128, 192, 256):
        a = int(str(rng.randrange(1, 10)) + "".join(str(rng.randrange(10)) for _ in range(digits-1)))
        b = int(str(rng.randrange(1, 10)) + "".join(str(rng.randrange(10)) for _ in range(digits-1)))
        stats = {"digit_multiplications": 0, "recursive_calls": 0, "max_depth": 0}
        result = q3.karatsuba_multiply(a, b, threshold_digits=24, stats=stats)
        assert result == q3.schoolbook_multiply(a, b)
        s_time = median_time(lambda: q3.schoolbook_multiply(a, b), 3)
        k_time = median_time(lambda: q3.karatsuba_multiply(a, b, threshold_digits=24), 3)
        rows.append({"digits": digits, "schoolbook_digit_products": digits*digits,
                     "karatsuba_digit_products": stats["digit_multiplications"],
                     "karatsuba_recursive_calls": stats["recursive_calls"],
                     "schoolbook_median_seconds": f"{s_time:.8f}", "karatsuba_median_seconds": f"{k_time:.8f}",
                     "threshold_digits": 24})
    save_csv("q3_karatsuba_experiments.csv", rows)
    chart("Q3 digit multiplications", [str(r["digits"]) for r in rows], [
        ("schoolbook", [r["schoolbook_digit_products"] for r in rows], "#ff5a5f"),
        ("Karatsuba base cases", [r["karatsuba_digit_products"] for r in rows], "#087e8b")], CHARTS/"q3_digit_products.png")

    # Q4: same deterministic matrices, cutoff=16; sizes include powers of two.
    rows = []
    for n in (8, 16, 32, 64, 128, 256):
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        classic_stats = {"multiplications": 0, "additions": 0}
        strassen_stats = {"multiplications": 0, "additions": 0, "recursive_calls": 0}
        assert q4.conventional(a, b, classic_stats) == q4.strassen(a, b, cutoff=16, stats=strassen_stats)
        repeats = 3 if n <= 128 else 1
        ct = median_time(lambda: q4.conventional(a, b), repeats)
        st = median_time(lambda: q4.strassen(a, b, cutoff=16), repeats)
        rows.append({"n": n, "padding_size": 1 << (n-1).bit_length(),
                     "conventional_multiplications": classic_stats["multiplications"],
                     "strassen_multiplications": strassen_stats["multiplications"],
                     "strassen_additions_subtractions": strassen_stats["additions"],
                     "conventional_median_seconds": f"{ct:.8f}", "strassen_median_seconds": f"{st:.8f}",
                     "cutoff": 16, "repeats": repeats})
    save_csv("q4_strassen_experiments.csv", rows)
    chart("Q4 scalar multiplication counts", [str(r["n"]) for r in rows], [
        ("conventional", [r["conventional_multiplications"] for r in rows], "#ff5a5f"),
        ("Strassen with cutoff 16", [r["strassen_multiplications"] for r in rows], "#087e8b")], CHARTS/"q4_multiplications.png")

    # Q5: identical point sets, comparison by distance evaluations and time.
    rows = []
    for n in (20, 100, 300, 600, 1000, 1600):
        points = [(rng.randrange(10**9), rng.randrange(10**9)) for _ in range(n)]
        bd, _, bc = q5.brute_force(points); dd, _, dc = q5.divide_conquer(points)
        assert abs(bd - dd) < 1e-12
        bt = median_time(lambda: q5.brute_force(points), 3)
        dt = median_time(lambda: q5.divide_conquer(points), 3)
        rows.append({"n": n, "brute_distance_calculations": bc, "dc_distance_calculations": dc,
                     "distance_equal": True, "brute_median_seconds": f"{bt:.8f}", "dc_median_seconds": f"{dt:.8f}"})
    save_csv("q5_closest_pair_experiments.csv", rows)
    chart("Q5 distance calculations", [str(r["n"]) for r in rows], [
        ("brute force", [r["brute_distance_calculations"] for r in rows], "#ff5a5f"),
        ("divide and conquer", [r["dc_distance_calculations"] for r in rows], "#087e8b")], CHARTS/"q5_distance_calculations.png")

    # Q6a: deterministic MoM, randomized QuickSelect, and deliberate first-pivot adversary.
    rows = []
    for n in (101, 501, 1001, 2001, 3001):
        values = [rng.randrange(-10**6, 10**6) for _ in range(n)]; rank = n//2
        med_stats = {"comparisons": 0, "partitions": 0, "max_depth": 0}
        rand_stats = {"comparisons": 0, "partitions": 0, "max_depth": 0}
        poor_stats = {"comparisons": 0, "partitions": 0, "max_depth": 0}
        expected = sorted(values)[rank]
        assert median_of_medians(values, rank, med_stats) == expected
        assert q6.quickselect(values, rank, seed=2026, stats=rand_stats) == expected
        ordered = list(range(n))
        assert q6.quickselect(ordered, rank, poor_first=True, stats=poor_stats) == rank
        mt = median_time(lambda: median_of_medians(values, rank), 3)
        rt = median_time(lambda: q6.quickselect(values, rank, seed=2026), 3)
        pt = median_time(lambda: q6.quickselect(ordered, rank, poor_first=True), 1)
        rows.append({"n": n, "mom_comparisons": med_stats["comparisons"], "mom_depth": med_stats["max_depth"],
                     "random_quickselect_comparisons": rand_stats["comparisons"], "random_quickselect_depth": rand_stats["max_depth"],
                     "first_pivot_sorted_comparisons": poor_stats["comparisons"], "first_pivot_partitions": poor_stats["partitions"],
                     "mom_median_seconds": f"{mt:.8f}", "random_median_seconds": f"{rt:.8f}", "first_pivot_seconds": f"{pt:.8f}"})
    save_csv("q6_selection_experiments.csv", rows)
    chart("Q6 selection comparisons", [str(r["n"]) for r in rows], [
        ("Median of Medians", [r["mom_comparisons"] for r in rows], "#087e8b"),
        ("Randomized QuickSelect", [r["random_quickselect_comparisons"] for r in rows], "#2e86ab"),
        ("First pivot on sorted input", [r["first_pivot_sorted_comparisons"] for r in rows], "#ff5a5f")], CHARTS/"q6_selection_comparisons.png")

    # Q6b: impossible target forces both methods to finish their search.
    rows = []
    for n in (10, 14, 18, 22, 26, 30, 34):
        values = [rng.randint(1, 1000) for _ in range(n)]; target = sum(values) + 1
        solution, stats = meet_in_middle(values, target)
        assert solution is None
        mitm_time = median_time(lambda: meet_in_middle(values, target), 3)
        brute_subsets = 1 << n
        if n <= 22:
            brute, examined = exhaustive_subset_sum(values, target)
            assert brute is None and examined == brute_subsets
            brute_time = median_time(lambda: exhaustive_subset_sum(values, target), 1)
        else:
            examined = brute_subsets; brute_time = None
        rows.append({"n": n, "left_subsets": stats["left_subsets"], "right_subsets": stats["right_subsets"],
                     "mitm_binary_search_comparisons": stats["binary_search_comparisons"],
                     "exhaustive_subsets": brute_subsets, "enumeration_verified": n <= 22,
                     "mitm_median_seconds": f"{mitm_time:.8f}",
                     "exhaustive_seconds": "" if brute_time is None else f"{brute_time:.8f}"})
    save_csv("q6_meet_middle_experiments.csv", rows)
    chart("Q6 subset-sum search space (log2 counts)", [str(r["n"]) for r in rows], [
        ("subsets per half", [max(r["left_subsets"], r["right_subsets"]) for r in rows], "#087e8b"),
        ("full enumeration", [r["exhaustive_subsets"] for r in rows], "#ff5a5f")], CHARTS/"q6_subset_search_space.png", log2=True)

    # Q7: same array compared with an O(n^2) baseline.
    rows = []
    for n in (16, 64, 256, 1024, 2048, 4096):
        values = [rng.randint(-1000, 1000) for _ in range(n)]
        dc = q7.maximum_subarray_divide_conquer(values); brute = q7.maximum_subarray_brute_force(values)
        assert dc[:3] == brute[:3]
        dt = median_time(lambda: q7.maximum_subarray_divide_conquer(values), 3)
        bt = median_time(lambda: q7.maximum_subarray_brute_force(values), 1)
        rows.append({"n": n, "dc_boundary_additions": dc[3], "brute_subarray_sum_updates": brute[3],
                     "results_equal": True, "dc_median_seconds": f"{dt:.8f}", "brute_seconds": f"{bt:.8f}"})
    save_csv("q7_maximum_subarray_experiments.csv", rows)
    chart("Q7 measured work", [str(r["n"]) for r in rows], [
        ("D&C boundary additions", [r["dc_boundary_additions"] for r in rows], "#087e8b"),
        ("brute-force sum updates", [r["brute_subarray_sum_updates"] for r in rows], "#ff5a5f")], CHARTS/"q7_work_counts.png")
    (RESULTS / "experiment_run.txt").write_text(
        "Experiments use deterministic seed 192524005. Timing columns are medians of repeated runs where shown; Q6 first-pivot worst-case and exhaustive subset-sum baselines are single runs. Timings are environment-specific. All algorithm pairs were checked for equal results on the same input before recording the comparison.\n",
        encoding="utf-8")
    print("Experiment tables and charts written to", RESULTS)


if __name__ == "__main__":
    run_all()
