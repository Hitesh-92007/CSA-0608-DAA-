"""Render the markdown case-study report as a clean, paginated PDF."""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Final_Design_and_Analysis" / "CO3_Final_Report.md"
OUTPUT = ROOT / "Final_Design_and_Analysis" / "CO3_Final_Report.pdf"
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 0.62 * inch
TOP = 0.66 * inch
BOTTOM = 0.66 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=23, leading=28, textColor=colors.HexColor("#17365D"),
    alignment=TA_CENTER, spaceAfter=16,
))
styles.add(ParagraphStyle(
    name="ReportH1", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=16, leading=20, textColor=colors.HexColor("#17365D"),
    spaceBefore=13, spaceAfter=7, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportH2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=colors.HexColor("#24527A"),
    spaceBefore=9, spaceAfter=5, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportH3", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=10, leading=13, textColor=colors.HexColor("#33475B"),
    spaceBefore=7, spaceAfter=4, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportBody", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.2, leading=13.4, textColor=colors.HexColor("#202B36"),
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="ReportBullet", parent=styles["ReportBody"], leftIndent=14,
    firstLineIndent=-8, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="ReportCaption", parent=styles["BodyText"], fontName="Helvetica-Oblique",
    fontSize=8, leading=10, textColor=colors.HexColor("#526579"),
    alignment=TA_CENTER, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="ReportTable", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=7.2, leading=9, textColor=colors.HexColor("#202B36"),
))
styles.add(ParagraphStyle(
    name="ReportTableHead", parent=styles["ReportTable"], fontName="Helvetica-Bold",
    textColor=colors.HexColor("#17365D"),
))
styles.add(ParagraphStyle(
    name="ReportCode", parent=styles["Code"], fontName="Courier",
    fontSize=7.7, leading=10, leftIndent=6, rightIndent=6,
    backColor=colors.HexColor("#F2F5F8"), borderColor=colors.HexColor("#DCE4ED"),
    borderWidth=0.4, borderPadding=6, spaceBefore=3, spaceAfter=7,
))


def plain_ascii(text: str) -> str:
    mapping = {
        "–": "-", "—": "-", "−": "-", "×": "x", "≈": "~=",
        "≤": "<=", "≥": ">=", "’": "'", "‘": "'", "“": '"', "”": '"',
        "…": "...", "Theta": "Theta",
    }
    for src, target in mapping.items():
        text = text.replace(src, target)
    return text


def inline_markup(text: str) -> str:
    text = html.escape(plain_ascii(text), quote=False)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def image_flowable(alt: str, relative_path: str):
    path = (SOURCE.parent / relative_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Report image not found: {path}")
    with PILImage.open(path) as source_image:
        width_px, height_px = source_image.size
    scale = min(CONTENT_W / width_px, 4.75 * inch / height_px, 1.0)
    image = Image(str(path), width=width_px * scale, height=height_px * scale)
    image.hAlign = "CENTER"
    return KeepTogether([
        Paragraph(inline_markup(alt), styles["ReportCaption"]),
        image,
        Spacer(1, 7),
    ])


def render_table(lines: list[str]):
    parsed = [split_table_row(line) for line in lines]
    if len(parsed) > 1 and is_table_separator(lines[1]):
        parsed.pop(1)
    columns = max(len(row) for row in parsed)
    data = []
    for row_index, row in enumerate(parsed):
        row = row + [""] * (columns - len(row))
        cell_style = styles["ReportTableHead"] if row_index == 0 else styles["ReportTable"]
        data.append([Paragraph(inline_markup(cell), cell_style) for cell in row])
    widths = [CONTENT_W / columns] * columns
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9F0F7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D3DF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#DCE4ED"))
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, 0.48 * inch, PAGE_W - RIGHT, 0.48 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526579"))
    canvas.drawString(LEFT, 0.31 * inch, "KartIQ CO3 case study | Hitesh C")
    canvas.drawRightString(PAGE_W - RIGHT, 0.31 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_story():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                code = plain_ascii("\n".join(code_lines))
                story.append(Preformatted(code, styles["ReportCode"], maxLineLength=105))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        image_match = re.match(r"!\[([^\]]*)\]\(([^\)]+)\)", line.strip())
        if image_match:
            story.append(image_flowable(image_match.group(1), image_match.group(2)))
            i += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            story.extend([render_table(table_lines), Spacer(1, 7)])
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            style_name = {1: "ReportTitle", 2: "ReportH1", 3: "ReportH2"}[level]
            story.append(Paragraph(inline_markup(heading.group(2)), styles[style_name]))
            i += 1
            continue
        if line.startswith("- "):
            story.append(Paragraph("&#8226; " + inline_markup(line[2:]), styles["ReportBullet"]))
            i += 1
            continue
        if re.match(r"^\d+\.\s", line):
            story.append(Paragraph(inline_markup(line), styles["ReportBullet"]))
            i += 1
            continue
        if line.strip() in ("---", "___", "***"):
            story.append(Spacer(1, 5))
            i += 1
            continue

        paragraph_lines = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") \
                and not lines[i].strip().startswith(("|", "```", "![", "- ")) \
                and not re.match(r"^\d+\.\s", lines[i]):
            paragraph_lines.append(lines[i].strip())
            i += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["ReportBody"]))
    return story


def main():
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=RIGHT, leftMargin=LEFT,
        topMargin=TOP, bottomMargin=BOTTOM,
        title="KartIQ CO3 Divide-and-Conquer Case Study",
        author="Hitesh C",
        subject="CSA06 CO3 AT3 case study report",
    )
    document.build(build_story(), onFirstPage=footer, onLaterPages=footer)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
