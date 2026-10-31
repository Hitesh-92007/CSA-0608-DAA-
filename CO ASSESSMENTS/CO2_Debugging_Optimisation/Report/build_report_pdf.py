"""Build the printable report from Report.md, charts, and evidence captures."""
from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted,
    Table, TableStyle, Image
)

REPORT_DIR = Path(__file__).resolve().parent
ROOT = REPORT_DIR.parent
MD_PATH = REPORT_DIR / "Report.md"
PDF_PATH = REPORT_DIR / "Report.pdf"
FONT_DIR = Path(r"C:\Windows\Fonts")
for font_name, font_file in (("Segoe", "segoeui.ttf"), ("Segoe-Bold", "segoeuib.ttf"),
                            ("Consolas", "consola.ttf")):
    path = FONT_DIR / font_file
    if path.exists():
        pdfmetrics.registerFont(TTFont(font_name, str(path)))
REGISTERED = pdfmetrics.getRegisteredFontNames()
BODY = "Segoe" if "Segoe" in REGISTERED else "Helvetica"
BOLD = "Segoe-Bold" if "Segoe-Bold" in REGISTERED else "Helvetica-Bold"
MONO = "Consolas" if "Consolas" in REGISTERED else "Courier"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", parent=styles["Title"], fontName=BOLD,
                          fontSize=22, leading=27, alignment=TA_CENTER,
                          textColor=colors.HexColor("#17365D"), spaceAfter=12))
styles.add(ParagraphStyle(name="H1X", parent=styles["Heading1"], fontName=BOLD,
                          fontSize=16, leading=20, textColor=colors.HexColor("#17365D"),
                          spaceBefore=9, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="H2X", parent=styles["Heading2"], fontName=BOLD,
                          fontSize=12.5, leading=15.5, textColor=colors.HexColor("#285A8E"),
                          spaceBefore=8, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H3X", parent=styles["Heading3"], fontName=BOLD,
                          fontSize=10, leading=13, textColor=colors.HexColor("#3E5368"),
                          spaceBefore=6, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName=BODY,
                          fontSize=8.8, leading=12, spaceAfter=5))
styles.add(ParagraphStyle(name="CaptionX", parent=styles["BodyText"], fontName=BODY,
                          fontSize=8, leading=10, textColor=colors.HexColor("#5B6570"),
                          alignment=TA_CENTER, spaceAfter=5))
styles.add(ParagraphStyle(name="CodeX", parent=styles["Code"], fontName=MONO,
                          fontSize=7.3, leading=9.3, leftIndent=8, rightIndent=8,
                          backColor=colors.HexColor("#F3F5F8"),
                          borderColor=colors.HexColor("#D6DCE5"), borderWidth=0.4,
                          borderPadding=5, spaceBefore=3, spaceAfter=6))
styles.add(ParagraphStyle(name="CellX", parent=styles["BodyText"], fontName=BODY,
                          fontSize=7.1, leading=8.8, spaceAfter=0))


def inline_markup(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", lambda m: f'<font name="{MONO}">{m.group(1)}</font>', value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    return value


def table_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))


def col_widths(count: int):
    total = 7.0 * inch
    patterns = {
        2: [0.25, 0.75],
        3: [0.18, 0.34, 0.48],
        4: [0.10, 0.18, 0.32, 0.40],
        5: [0.14, 0.18, 0.22, 0.22, 0.24],
        6: [0.10, 0.18, 0.18, 0.18, 0.18, 0.18],
    }
    weights = patterns.get(count, [1 / count] * count)
    return [total * w for w in weights]


def parse_markdown(text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    story = []
    paragraph_lines = []
    in_code = False
    code_lines = []
    section = ""

    def flush_paragraph():
        if paragraph_lines:
            content = " ".join(x.strip() for x in paragraph_lines)
            story.append(Paragraph(inline_markup(content), styles["BodyX"]))
            paragraph_lines.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            flush_paragraph()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                story.append(Preformatted("\n".join(code_lines), styles["CodeX"]))
                in_code = False
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not line.strip():
            flush_paragraph()
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            section = heading.group(2).strip().lower()
            style = "H1X" if level == 1 else ("H2X" if level == 2 else "H3X")
            story.append(Paragraph(inline_markup(heading.group(2)), styles[style]))
            i += 1
            continue
        image_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if image_match:
            flush_paragraph()
            alt, rel_path = image_match.groups()
            image_path = (REPORT_DIR / rel_path.replace("/", "\\")).resolve()
            if not image_path.exists():
                raise FileNotFoundError(f"Report image not found: {image_path}")
            img = Image(str(image_path))
            max_w, max_h = 7.0 * inch, 5.25 * inch
            factor = min(max_w / img.imageWidth, max_h / img.imageHeight, 1.0)
            img.drawWidth = img.imageWidth * factor
            img.drawHeight = img.imageHeight * factor
            story.append(Paragraph(inline_markup(alt), styles["CaptionX"]))
            story.append(img)
            story.append(Spacer(1, 7))
            more_images_follow = any(
                re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", candidate.strip())
                for candidate in lines[i + 1:]
            )
            if section.startswith("appendix a:") or section.startswith("appendix b:"):
                if more_images_follow:
                    story.append(PageBreak())
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and table_separator(lines[i + 1]):
            flush_paragraph()
            table_lines = [line]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            rows = []
            for rowline in table_lines:
                cells = [x.strip() for x in rowline.strip().strip("|").split("|")]
                rows.append([Paragraph(inline_markup(cell), styles["CellX"]) for cell in cells])
            if rows:
                table = Table(rows, colWidths=col_widths(len(rows[0])), repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                    ("FONTNAME", (0, 0), (-1, 0), BOLD),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAB6C4")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                story.extend([table, Spacer(1, 6)])
            continue
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        numbered = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if bullet or numbered:
            flush_paragraph()
            item = bullet.group(1) if bullet else numbered.group(1)
            story.append(Paragraph("&#8226; " + inline_markup(item), styles["BodyX"]))
            i += 1
            continue
        paragraph_lines.append(line)
        i += 1
    flush_paragraph()
    if in_code and code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["CodeX"]))
    return story


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY, 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawRightString(A4[0] - 0.7 * inch, 0.32 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(PDF_PATH), pagesize=A4, rightMargin=0.7*inch,
                        leftMargin=0.7*inch, topMargin=0.58*inch,
                        bottomMargin=0.58*inch, title="SentinelOps SOC Alert Triage Report",
                        author="Hitesh C")
doc.build(parse_markdown(MD_PATH.read_text(encoding="utf-8")),
          onFirstPage=page_number, onLaterPages=page_number)
print(PDF_PATH)
