"""Create report-ready comparison charts using Pillow."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Supporting_Files" / "results"
OUT = RESULTS / "charts"
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(r"C:\Windows\Fonts")


def font(size: int, bold: bool = False):
    path = FONT_DIR / ("segoeuib.ttf" if bold else "segoeui.ttf")
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def read_csv(name: str):
    with (RESULTS / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def text_center(draw: ImageDraw.ImageDraw, xy, text: str, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2),
              text, font=fnt, fill=fill)


def sorting_chart():
    rows = [row for row in read_csv("sorting_experiments.csv")
            if row["distribution"] == "nearly_sorted_100_adjacent_swaps"]
    sizes = [int(row["n"]) for row in rows]
    merge = [int(row["merge_key_comparisons"]) for row in rows]
    intro = [int(row["guarded_quick_comparisons"]) for row in rows]
    first = [n * (n - 1) // 2 for n in sizes]
    width, height = 1200, 720
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((72, 36), "Sorting comparisons on nearly ordered seller scores",
              font=font(30, True), fill="#17365D")
    draw.text((72, 82), "Measured nearly-sorted runs; sorted-input first-pivot worst case; logarithmic y-axis",
              font=font(18), fill="#526579")
    left, right, top, bottom = 125, 1110, 150, 565
    y_min, y_max = 1_000, 10_000_000_000
    ymin_log, ymax_log = math.log10(y_min), math.log10(y_max)

    def y_map(value):
        ratio = (math.log10(max(value, y_min)) - ymin_log) / (ymax_log - ymin_log)
        return int(bottom - ratio * (bottom - top))

    ticks = [10**power for power in range(3, 11)]
    for tick in ticks:
        y = y_map(tick)
        draw.line((left, y, right, y), fill="#DCE4ED", width=1)
        draw.text((30, y - 12), f"10^{int(math.log10(tick))}", font=font(15), fill="#526579")
    draw.line((left, top, left, bottom), fill="#50657C", width=2)
    draw.line((left, bottom, right, bottom), fill="#50657C", width=2)
    xs = [left + int(i * (right - left) / (len(sizes) - 1)) for i in range(len(sizes))]
    for x, n in zip(xs, sizes):
        draw.line((x, bottom, x, bottom + 7), fill="#50657C", width=2)
        text_center(draw, (x, bottom + 27), f"{n:,}", font(15), "#33475B")
    text_center(draw, ((left + right) // 2, 625), "Number of sellers", font(18), "#33475B")

    series = [
        (merge, "Stable Merge Sort", "#2878B5"),
        (intro, "Median-of-three guarded Quick Sort", "#2A9D70"),
        (first, "First-pivot sorted worst case (exact)", "#D7653B"),
    ]
    for values, label, color in series:
        points = [(x, y_map(v)) for x, v in zip(xs, values)]
        draw.line(points, fill=color, width=4)
        for x, y in points:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color, outline="white", width=2)

    positions = [(100, 650), (535, 650), (100, 690)]
    for (values, label, color), (x, legend_y) in zip(series, positions):
        draw.line((x, legend_y, x + 32, legend_y), fill=color, width=4)
        draw.text((x + 42, legend_y - 10), label, font=font(14), fill="#33475B")
    image.save(OUT / "sorting_comparisons.png")


def matrix_chart():
    rows = read_csv("matrix_production_counts.csv")
    labels = ["Conventional", "Pure Strassen", "Hybrid cutoff 64"]
    values = [1_024**3,
              int(next(r["scalar_multiplications"] for r in rows if r["method"] == "pure_strassen")),
              int(next(r["scalar_multiplications"] for r in rows if r["method"] == "hybrid_cutoff_64"))]
    colors = ["#6B7C93", "#2878B5", "#2A9D70"]
    width, height = 1200, 650
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((72, 36), "Scalar multiplications for 1,024 x 1,024 matrices",
              font=font(30, True), fill="#17365D")
    draw.text((72, 82), "Pure Strassen and cutoff-64 hybrid counts are recurrence calculations",
              font=font(18), fill="#526579")
    left, right, top, bottom = 150, 1110, 140, 520
    max_value = 1_200_000_000
    for tick in range(0, 1_200_000_001, 200_000_000):
        y = bottom - int((tick / max_value) * (bottom - top))
        draw.line((left, y, right, y), fill="#DCE4ED", width=1)
        draw.text((20, y - 12), f"{tick / 1_000_000:.0f}M", font=font(15), fill="#526579")
    draw.line((left, top, left, bottom), fill="#50657C", width=2)
    draw.line((left, bottom, right, bottom), fill="#50657C", width=2)
    centers = [340, 630, 920]
    bar_width = 145
    for center, label, value, color in zip(centers, labels, values, colors):
        y = bottom - int((value / max_value) * (bottom - top))
        draw.rounded_rectangle((center - bar_width // 2, y, center + bar_width // 2, bottom),
                               radius=8, fill=color)
        draw.text((center - bar_width // 2, y - 34), f"{value:,}", font=font(16, True), fill=color)
        text_center(draw, (center, bottom + 28), label, font(16), "#33475B")
    text_center(draw, ((left + right) // 2, 600), "Algorithm choice", font(18), "#33475B")
    image.save(OUT / "matrix_multiplications_1024.png")


def binary_chart():
    width, height = 1120, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((72, 36), "Lookup work at 10,000,000 orders",
              font=font(30, True), fill="#17365D")
    draw.text((72, 82), "Maximum lower-bound probes compared with a full sequential scan",
              font=font(18), fill="#526579")
    left, right, top, bottom = 160, 1035, 150, 470
    values = [10_000_000, 24]
    labels = ["Sequential scan", "Binary lower bound"]
    colors = ["#D7653B", "#2878B5"]
    ymax_log = 7
    for power in range(0, ymax_log + 1):
        y = bottom - int((power / ymax_log) * (bottom - top))
        draw.line((left, y, right, y), fill="#DCE4ED", width=1)
        draw.text((70, y - 10), f"10^{power}", font=font(15), fill="#526579")
    for center, value, label, color in zip([390, 800], values, labels, colors):
        log_value = math.log10(value)
        y = bottom - int((log_value / ymax_log) * (bottom - top))
        draw.rounded_rectangle((center - 75, y, center + 75, bottom), radius=8, fill=color)
        draw.text((center - 85, y - 32), f"{value:,}", font=font(17, True), fill=color)
        text_center(draw, (center, bottom + 30), label, font(16), "#33475B")
    text_center(draw, ((left + right) // 2, 560), "Key comparisons / probes (log scale)", font(18), "#33475B")
    image.save(OUT / "lookup_comparisons_10m.png")


if __name__ == "__main__":
    sorting_chart()
    matrix_chart()
    binary_chart()
    print("Charts saved under", OUT)
