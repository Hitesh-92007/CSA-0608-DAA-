"""Create a tagged, readable PDF version of the generated assignment report."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, PageTemplate, PageBreak, Paragraph, Spacer, Table,
    TableStyle, KeepTogether,
)

from build_report import FINAL, ROOT, sections


OUTPUT = FINAL / "CO2_Assignment_Report.pdf"
PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.68 * inch
TOP = 0.72 * inch
BOTTOM = 0.68 * inch
CONTENT_W = PAGE_W - LEFT - RIGHT
CONTENT_H = PAGE_H - TOP - BOTTOM

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, leading=27, textColor=colors.HexColor("#1F4E78"),
    alignment=TA_CENTER, spaceAfter=16,
))
styles.add(ParagraphStyle(
    name="SubTitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Section1", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=15, leading=18, textColor=colors.HexColor("#1F4E78"),
    spaceBefore=12, spaceAfter=6, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Section2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=14, textColor=colors.HexColor("#365F91"),
    spaceBefore=10, spaceAfter=5, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.2, leading=13.1, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=7.4, leading=9.2, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=7.5, leading=9.2, textColor=colors.white, alignment=TA_CENTER,
    spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="CaptionCustom", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"),
    spaceBefore=3, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="CoverMeta", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=16, alignment=TA_CENTER, spaceAfter=6,
))


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 0.42 * inch,
                               "CSA06 | CO2 Brute Force and Exhaustive Search")
        canvas.drawCentredString(PAGE_W / 2, 0.38 * inch,
                                 f"CO2 Assignment Report | Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=letter, leftMargin=LEFT, rightMargin=RIGHT,
    topMargin=TOP, bottomMargin=BOTTOM, title="CO2 Assignment Report",
    author="Hitesh C",
)
frame = Frame(LEFT, BOTTOM, CONTENT_W, CONTENT_H, id="normal")
doc.addPageTemplates([PageTemplate(id="report", frames=frame, onPage=on_page)])
story = []

story.extend([
    Spacer(1, 1.15 * inch),
    Paragraph("CO2 Assignment Report", styles["ReportTitle"]),
    Paragraph("Brute Force and Exhaustive Search", styles["SubTitle"]),
    Paragraph("CSA06 Design and Analysis of Algorithms", styles["SubTitle"]),
    Paragraph("Course Outcome 2", styles["SubTitle"]),
    Spacer(1, 0.45 * inch),
    Paragraph("Student: Hitesh C", styles["CoverMeta"]),
    Paragraph("Register number: 192524005", styles["CoverMeta"]),
    Paragraph("Assignment type: Individual", styles["CoverMeta"]),
    Paragraph("Report date: 15 November 2026", styles["CoverMeta"]),
    PageBreak(),
])


def add_table(headers, rows):
    data = [[Paragraph(escape(str(x)), styles["TableHead"]) for x in headers]]
    for row in rows:
        data.append([Paragraph(escape(str(x)), styles["TableCell"]) for x in row])
    count = len(headers)
    # Allocate more width to descriptive fields and keep numeric fields readable.
    if count == 7:
        proportions = [0.50, 1.0, 1.0, 0.68, 0.7, 0.8, 0.8]
    elif count == 6:
        proportions = [1.35, 1.0, 0.9, 0.8, 0.8, 0.7]
    elif count == 5:
        proportions = [1.25, 0.8, 0.8, 1.3, 1.0]
    elif count == 4:
        proportions = [1.0, 1.0, 1.1, 1.0]
    else:
        proportions = [1.0] * count
    total = sum(proportions)
    widths = [CONTENT_W * p / total for p in proportions]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F1F5F9")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([Spacer(1, 4), table, Spacer(1, 8)])


def add_figure(relative_path, caption):
    full_path = ROOT / relative_path
    if not full_path.exists():
        return
    figure = Image(str(full_path))
    max_width = CONTENT_W
    max_height = 4.3 * inch
    scale = min(max_width / figure.imageWidth, max_height / figure.imageHeight, 1.0)
    figure.drawWidth = figure.imageWidth * scale
    figure.drawHeight = figure.imageHeight * scale
    story.append(KeepTogether([
        Spacer(1, 3),
        figure,
        Paragraph(escape(caption), styles["CaptionCustom"]),
    ]))


for block in sections:
    kind = block[0]
    if kind == "h1":
        if block[1] == "Complexity Summary":
            story.append(PageBreak())
        story.append(Paragraph(escape(block[1]), styles["Section1"]))
    elif kind == "h2":
        story.append(Paragraph(escape(block[1]), styles["Section2"]))
    elif kind == "p":
        story.append(Paragraph(escape(block[1]), styles["BodyCustom"]))
    elif kind == "table":
        add_table(block[1], block[2])
    elif kind == "image":
        add_figure(block[1], block[2])

story.extend([PageBreak(), Paragraph("Execution evidence", styles["Section1"])])
story.append(Paragraph(
    "These images are rendered from the saved program output transcripts. "
    "Each corresponding RUN_OUTPUT.txt file is included beside its image.",
    styles["BodyCustom"],
))
for number, folder in enumerate([
    "Q1_Sorting_Algorithms",
    "Q2_Sequential_Search",
    "Q3_Brute_Force_String_Matching",
    "Q4_Brute_Force_Closest_Pair",
    "Q5_Brute_Force_Convex_Hull",
    "Q6_Exhaustive_Search",
    "Q7_Day4_Design_Challenge",
], 1):
    add_figure(f"{folder}/Output_Screenshots/output_capture.png",
               f"Q{number} saved run transcript.")

doc.build(story)
print(f"Built {OUTPUT}")
