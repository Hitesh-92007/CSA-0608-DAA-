"""Run all seven assignment programs and save reproducible text/PNG captures."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIRS = [
    "Q1_MaxMin_Binary_Search", "Q2_MergeSort_QuickSort", "Q3_Karatsuba_Multiplication",
    "Q4_Strassen_Matrix_Multiplication", "Q5_Divide_Conquer_Closest_Pair",
    "Q6_Advanced_Divide_Conquer", "Q7_Day4_Design_Challenge",
]
SCRIPTS = [
    "Q1_MaxMin_Binary_Search/Implementation_Code/max_min_binary_search.py",
    "Q2_MergeSort_QuickSort/Implementation_Code/sorting_comparison.py",
    "Q3_Karatsuba_Multiplication/Implementation_Code/karatsuba_multiplication.py",
    "Q4_Strassen_Matrix_Multiplication/Implementation_Code/strassen_comparison.py",
    "Q5_Divide_Conquer_Closest_Pair/Implementation_Code/closest_pair_comparison.py",
    "Q6_Advanced_Divide_Conquer/Implementation_Code/q6_advanced.py",
    "Q7_Day4_Design_Challenge/Implementation_Code/day4_challenge.py",
]


def output_image(text: str, path: Path, title: str) -> None:
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)
        heading = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 19)
    except OSError:
        font = ImageFont.load_default(); heading = font
    lines = text.splitlines() or ["(no output)"]
    wrapped = []
    for line in lines:
        while len(line) > 100:
            wrapped.append(line[:100]); line = "  " + line[100:]
        wrapped.append(line)
    width, top, line_h = 1080, 64, 25
    height = top + len(wrapped) * line_h + 28
    image = Image.new("RGB", (width, height), "#101820")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 48), fill="#182a38")
    draw.text((22, 14), title, font=heading, fill="#f1f5f9")
    for i, line in enumerate(wrapped):
        draw.text((24, top + i * line_h), line, font=font, fill="#d5e8d4")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def main() -> None:
    for q, script in zip(CAPTURE_DIRS, SCRIPTS):
        result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT,
                                text=True, capture_output=True, check=True)
        output = result.stdout.rstrip() + ("\n" + result.stderr.rstrip() if result.stderr.strip() else "")
        target = ROOT / q / "Output_Screenshots"
        target.mkdir(parents=True, exist_ok=True)
        (target / "RUN_OUTPUT.txt").write_text(output + "\n", encoding="utf-8")
        output_image(output, target / "output_capture.png", q.replace("_", " ") + " program output")
        print(f"[PASS] {q}: saved text log and output capture")


if __name__ == "__main__":
    main()
