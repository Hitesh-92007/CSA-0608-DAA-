"""Render readable PNG evidence from the submitted source, report, and run log."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPORT = Path(__file__).resolve().parent
EVIDENCE = REPORT / "Evidence"
SOURCE = REPORT.parent / "Source_Code" / "scalability_audit.cpp"
OUTPUT = REPORT / "program_output.txt"
EVIDENCE.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path("C:/Windows/Fonts")
MONO = ImageFont.truetype(str(FONT_DIR / "consola.ttf"), 22)
MONO_SMALL = ImageFont.truetype(str(FONT_DIR / "consola.ttf"), 15)
SANS = ImageFont.truetype(str(FONT_DIR / "segoeui.ttf"), 24)
SANS_BOLD = ImageFont.truetype(str(FONT_DIR / "segoeuib.ttf"), 27)


def render_panel(path: Path, title: str, subtitle: str, lines: list[str],
                 *, code: bool = False, width: int = 1800,
                 line_offset: int = 0) -> None:
    top, margin, line_height = 42, 56, 32 if code else 34
    header_height = 122
    height = header_height + top + len(lines) * line_height + 56
    bg = "#0b1220" if code else "#f4f7fb"
    fg = "#dce7f5" if code else "#172033"
    muted = "#7f91a8" if code else "#607086"
    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 10), fill="#2b7fff")
    draw.text((margin, 28), title, font=SANS_BOLD, fill=fg)
    draw.text((margin, 73), subtitle, font=SANS, fill=muted)
    draw.line((margin, 113, width - margin, 113), fill="#34445a" if code else "#d3dce8", width=2)
    y = header_height + top
    for index, line in enumerate(lines):
        if code:
            draw.text((margin, y), f"{line_offset + index + 1:>3}", font=MONO_SMALL, fill=muted)
            draw.text((margin + 55, y), line.rstrip("\n"), font=MONO, fill=fg)
        else:
            draw.text((margin, y), line.rstrip("\n"), font=MONO, fill=fg)
        y += line_height
    image.quantize(colors=16, method=Image.Quantize.FASTOCTREE,
                   dither=Image.Dither.NONE).save(path, optimize=True)


source_lines = SOURCE.read_text(encoding="utf-8").splitlines()
page_size = 30
for page, start in enumerate(range(0, len(source_lines), page_size), 1):
    chunk = source_lines[start:start + page_size]
    render_panel(
        EVIDENCE / f"source_code_screenshot_{page}.png",
        f"C++ source code — part {page}",
        f"scalability_audit.cpp | lines {start + 1}–{start + len(chunk)} | rendered from submitted source",
        chunk,
        code=True,
        width=1250,
        line_offset=start,
    )

output_lines = OUTPUT.read_text(encoding="utf-8").splitlines()
render_panel(
    EVIDENCE / "program_output_screenshot.png",
    "Program output",
    "Captured stdout from the compiled C++ program | program_output.txt",
    output_lines,
)

analysis_lines = [
    "M1 pair comparisons: n(n−1)/2 = 499,999,500,000 at n = 1,000,000.",
    "M2 windows: 1 + 2 + 4 + … + 2^(k−1) = 2^k − 1, k = ceil(log₂ n).",
    "At n = 1,024, M2 performs 1,023 Audit operations; therefore its bound is Θ(n).",
    "S2 substitution: T(n) = T(n/2) + 1 = T(1) + log₂ n = 1 + log₂ n.",
    "M4 current: 4T(n/2)+n → Θ(n²); proposed: 2T(n/2)+n → Θ(n log n).",
    "M5 recursion tree: n(log n + … + 1) + Θ(n) = Θ(n log² n).",
    "For f(n), choose c₁=3, c₂=63, n₀=2; thus 3n² ≤ f(n) ≤ 63n².",
    "At one million items, M1 and current M4 exceed the 10-minute window.",
    "Recommendation: index M1 by seller/title and remove M4's replicated recursion.",
]
render_panel(
    EVIDENCE / "analysis_screenshot.png",
    "Analysis summary",
    "Rendered excerpt from Report.md | full derivations are in the report",
    analysis_lines,
)

documentation_lines = [
    "Files included in this question folder:",
    "  Source_Code/scalability_audit.cpp",
    "  Report/Report.md",
    "  Report/program_output.txt",
    "  Report/Evidence/*.png",
    "",
    "Compile from the Source_Code folder:",
    "  g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic scalability_audit.cpp -o scalability_audit",
    "",
    "Run on Linux/macOS:",
    "  ./scalability_audit",
    "",
    "Run on Windows after compilation:",
    "  .\\scalability_audit.exe",
    "",
    "The program assumes 100,000,000 operations per second, checks M2 at n=1,024,",
    "and estimates the requested modules at n=1,000,000.",
]
render_panel(
    EVIDENCE / "documentation_screenshot.png",
    "Documentation and run instructions",
    "Rendered excerpt from the CO1_AT1 README and Report",
    documentation_lines,
)

print(f"Rendered {len(list(EVIDENCE.glob('*.png')))} evidence images in {EVIDENCE}")
