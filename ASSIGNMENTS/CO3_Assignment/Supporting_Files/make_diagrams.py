"""Create compact decomposition diagrams for the seven report sections."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Supporting_Files" / "Decomposition_Diagrams"

DIAGRAMS = {
    "q1_max_min_binary_search.png": ("Q1 decomposition", [
        ["Input interval", "Split into halves", "Solve local min/max", "Combine two pairs"],
        ["Sorted array", "Compare midpoint", "Keep possible half", "Repeat or return"]]),
    "q2_sorting.png": ("Q2 sorting decomposition", [
        ["Merge Sort: split evenly", "Sort both halves", "Merge sorted halves"],
        ["Quick Sort: choose last pivot", "Partition around pivot", "Recurse on both sides"]]),
    "q3_karatsuba.png": ("Q3 Karatsuba decomposition", [
        ["Split a and b", "Compute z0 = a0*b0", "Compute z2 = a1*b1", "Compute z1 from sums"],
        ["Three half-size products", "Subtract z0 and z2", "Shift by powers of 10", "Add partial results"]]),
    "q4_strassen.png": ("Q4 Strassen decomposition", [
        ["Split A and B into blocks", "Form seven products M1..M7", "Combine into C11 and C12", "Combine into C21 and C22"],
        ["Pad to power of two", "Recurse to cutoff", "Join result blocks", "Crop padded output"]]),
    "q5_closest_pair.png": ("Q5 closest-pair decomposition", [
        ["Sort points by x and y", "Split at median x", "Solve left and right", "Check narrow y-strip"]]),
    "q6_advanced.png": ("Q6 advanced D&C investigations", [
        ["Selection: groups of five", "Find median of medians", "Partition around pivot", "Recurse on rank side"],
        ["Subset Sum: split items", "Enumerate each half", "Sort right-half sums", "Search complements"]]),
    "q7_max_subarray.png": ("Q7 maximum-subarray design", [
        ["Input interval", "Solve left half", "Solve right half", "Scan crossing suffix/prefix"],
        ["Three candidates", "Left best", "Right best", "Crossing best: choose max"]]),
}


def font(size: int):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make(title: str, rows: list[list[str]], path: Path) -> None:
    width, height = 1200, 120 + len(rows) * 150
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((35, 24), title, font=font(26), fill="#142b3b")
    colors = ["#eaf4f4", "#fff2e5", "#f0efff", "#eef5e8"]
    for r, nodes in enumerate(rows):
        y = 92 + r * 150
        box_w, box_h = 240, 96
        gap = (width - 70 - len(nodes) * box_w) / max(1, len(nodes) - 1)
        x0 = 35
        for i, label in enumerate(nodes):
            x = int(x0 + i * (box_w + gap))
            draw.rounded_rectangle((x, y, x + box_w, y + box_h), radius=14,
                                   fill=colors[i % len(colors)], outline="#4b6678", width=2)
            lines = label.split("\\n")
            start_y = y + (box_h - len(lines) * 22) // 2
            for line_no, line in enumerate(lines):
                bounds = draw.textbbox((0, 0), line, font=font(16))
                tx = x + (box_w - (bounds[2] - bounds[0])) // 2
                draw.text((tx, start_y + line_no * 22), line, font=font(16), fill="#1d3546")
            if i < len(nodes) - 1:
                x1, x2, cy = x + box_w + 5, int(x + box_w + gap - 5), y + box_h // 2
                draw.line((x1, cy, x2, cy), fill="#516d7f", width=3)
                draw.polygon([(x2, cy), (x2 - 10, cy - 6), (x2 - 10, cy + 6)], fill="#516d7f")
    path.parent.mkdir(parents=True, exist_ok=True); image.save(path)


def main() -> None:
    for filename, (title, rows) in DIAGRAMS.items():
        make(title, rows, OUT / filename)
    print(f"Created {len(DIAGRAMS)} decomposition diagrams in {OUT}")


if __name__ == "__main__":
    main()
