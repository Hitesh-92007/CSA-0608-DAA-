"""Create report charts from the saved experiment CSV files using Pillow."""
import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT
FONT_PATH = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_BOLD_PATH = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def distance_chart():
    with (ROOT / "distance_experiments.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    width, height = 1200, 700
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title = font(30, True)
    label = font(19)
    small = font(16)
    draw.text((70, 32), "Closest pair distance evaluations", fill="#18324B", font=title)
    draw.text((70, 78), "Full squared-distance evaluations; y-axis is logarithmic", fill="#506070", font=label)
    left, right, top, bottom = 140, 1120, 150, 570
    y_min, y_max = 2.5, 8.0
    ticks = [3, 4, 5, 6, 7, 8]
    for tick in ticks:
        y = bottom - (tick - y_min) / (y_max - y_min) * (bottom - top)
        draw.line((left, y, right, y), fill="#D8E0E8", width=2)
        draw.text((70, y - 10), f"10^{tick}", fill="#506070", font=small)
    draw.line((left, top, left, bottom), fill="#54697C", width=2)
    draw.line((left, bottom, right, bottom), fill="#54697C", width=2)
    x_positions = [left + 70, (left + right) // 2, right - 70]
    series = [
        ("Brute force", "bruteforce_distance_evaluations", "#D2693C"),
        ("Divide and conquer", "optimized_distance_evaluations", "#2B77A8"),
    ]
    for name, field, color in series:
        coords = []
        for x, row in zip(x_positions, rows):
            value = int(row[field])
            y = bottom - (math.log10(value) - y_min) / (y_max - y_min) * (bottom - top)
            coords.append((x, y))
        draw.line(coords, fill=color, width=5)
        for (x, y), row in zip(coords, rows):
            draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color, outline="white", width=2)
            draw.text((x - 34, y - 33), f"{int(row[field]):,}", fill=color, font=small)
        draw.line((790 if name == "Brute force" else 790, 625 + (0 if name == "Brute force" else 32),
                   830, 625 + (0 if name == "Brute force" else 32)), fill=color, width=5)
        draw.text((842, 614 + (0 if name == "Brute force" else 32)), name, fill="#283B4D", font=small)
    for x, row in zip(x_positions, rows):
        draw.text((x - 32, bottom + 15), f"{int(row['events']):,}", fill="#283B4D", font=small)
    draw.text((520, 655), "Number of login events", fill="#283B4D", font=label)
    image.save(OUT_DIR / "distance_evaluations.png", optimize=True)


def sort_chart():
    with (ROOT / "sort_experiments.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    width, height = 1000, 620
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title, label, small = font(30, True), font(19), font(18)
    draw.text((65, 32), "Insertion sort comparisons depend on input order", fill="#18324B", font=title)
    draw.text((65, 78), "5,000 alerts; severity-key comparisons on a logarithmic scale", fill="#506070", font=label)
    left, right, top, bottom = 135, 930, 145, 495
    y_min, y_max = 3.0, 7.0
    for tick in range(3, 8):
        y = bottom - (tick - y_min) / (y_max - y_min) * (bottom - top)
        draw.line((left, y, right, y), fill="#D8E0E8", width=2)
        draw.text((55, y - 10), f"10^{tick}", fill="#506070", font=font(16))
    draw.line((left, top, left, bottom), fill="#54697C", width=2)
    draw.line((left, bottom, right, bottom), fill="#54697C", width=2)
    centers = [335, 720]
    colors_ = ["#2B77A8", "#D2693C"]
    for center, row, color in zip(centers, rows, colors_):
        value = int(row["insertion_key_comparisons"])
        y = bottom - (math.log10(value) - y_min) / (y_max - y_min) * (bottom - top)
        draw.rectangle((center - 90, y, center + 90, bottom), fill=color)
        draw.text((center - 60, y - 35), f"{value:,}", fill=color, font=small)
        draw.text((center - 100, bottom + 18), row["dataset"].replace("_", " "), fill="#283B4D", font=small)
    draw.text((240, 560), "Nearly sorted input needs far fewer comparisons than shuffled input.", fill="#506070", font=label)
    image.save(OUT_DIR / "insertion_sort_comparisons.png", optimize=True)


if __name__ == "__main__":
    distance_chart()
    sort_chart()
    print("Created distance_evaluations.png and insertion_sort_comparisons.png")
