"""Run all seven questions and render each actual output transcript to PNG."""

from pathlib import Path
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ("Q1_Sorting_Algorithms", "Implementation_Code/sorting_algorithms.py"),
    ("Q2_Sequential_Search", "Implementation_Code/sequential_search.py"),
    ("Q3_Brute_Force_String_Matching",
     "Implementation_Code/brute_force_string_matching.py"),
    ("Q4_Brute_Force_Closest_Pair",
     "Implementation_Code/brute_force_closest_pair.py"),
    ("Q5_Brute_Force_Convex_Hull",
     "Implementation_Code/brute_force_convex_hull.py"),
    ("Q6_Exhaustive_Search", "Implementation_Code/exhaustive_knapsack.py"),
    ("Q7_Day4_Design_Challenge", "Implementation_Code/closest_pair_redesign.py"),
]


def render_transcript(text, destination):
    lines = []
    for line in text.rstrip().splitlines():
        lines.extend(textwrap.wrap(line, width=100, replace_whitespace=False,
                                   drop_whitespace=False) or [""])
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    width = 1400
    line_height = 27
    height = max(170, 104 + line_height * len(lines))
    image = Image.new("RGB", (width, height), "#111827")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 18, width - 22, height - 18), radius=12,
                           fill="#0b1220", outline="#334155", width=2)
    draw.text((42, 36), "PROGRAM OUTPUT - saved run transcript",
              fill="#93c5fd", font=font)
    y = 78
    for line in lines:
        draw.text((42, y), line, fill="#e5e7eb", font=font)
        y += line_height
    image.save(destination)


def main():
    for folder, script in SCRIPTS:
        question = ROOT / folder
        source = question / script
        result = subprocess.run([sys.executable, str(source)], cwd=ROOT,
                                text=True, capture_output=True)
        transcript = result.stdout
        if result.stderr:
            transcript += "\nSTDERR:\n" + result.stderr
        output_dir = question / "Output_Screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "RUN_OUTPUT.txt").write_text(transcript, encoding="utf-8")
        render_transcript(transcript or "(no output)", output_dir / "output_capture.png")
        if result.returncode:
            raise SystemExit(f"{folder} failed with code {result.returncode}")
        print(f"{folder}: PASS; output saved")
    print("All seven question programs completed.")


if __name__ == "__main__":
    main()
