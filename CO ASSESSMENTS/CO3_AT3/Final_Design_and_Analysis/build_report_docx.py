"""Build an editable Word report from the checked case-study Markdown."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Final_Design_and_Analysis" / "CO3_Final_Report.md"
OUTPUT = ROOT / "Final_Design_and_Analysis" / "CO3_Final_Report.docx"
IMAGE_WIDTH = 6.55
BLUE = "17365D"
PALE_BLUE = "E9F0F7"
GRID = "C8D3DF"
BODY = "202B36"
CODE = "34495E"


def add_field(run, field_name: str) -> None:
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = field_name
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, placeholder, end])


def set_cell_shading(cell, fill: str) -> None:
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=70, start=80, bottom=70, end=80) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    table_header = OxmlElement("w:tblHeader")
    table_header.set(qn("w:val"), "true")
    tr_pr.append(table_header)


def prevent_row_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tr_pr.append(OxmlElement("w:cantSplit"))


def set_run_font(run, name="Arial", size=9.5, color=BODY, bold=False, italic=False):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold
    run.italic = italic


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+\*|\[[^\]]+\]\([^)]+\))")


def append_inline(paragraph, text: str, *, base_size=9.5, base_color=BODY, bold=False):
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, size=base_size, color=base_color, bold=True)
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, name="Consolas", size=max(7, base_size - 0.4), color=CODE)
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, size=base_size, color=base_color, italic=True)
        elif part.startswith("[") and "](" in part:
            run = paragraph.add_run(part[1:part.index("](")])
            set_run_font(run, size=base_size, color=base_color, bold=bold)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, size=base_size, color=base_color, bold=bold)


def heading_text(raw: str) -> str:
    part = re.match(r"Part \(([a-f])\):\s*(.*)", raw, re.IGNORECASE)
    if part:
        prefix = f"Part {part.group(1).upper()} "
        body = part.group(2)
    else:
        prefix = ""
        body = raw
    body = body.replace("divide-and-conquer", "divide and conquer")
    body = body.replace("Strassen's method", "Strassen method")
    body = re.sub(r"[-,:;()]+", " ", body)
    body = re.sub(r"\s+", " ", body).strip().title()
    return prefix + body


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def add_markdown_table(doc: Document, lines: list[str]) -> None:
    rows = [table_cells(line) for line in lines]
    if len(rows) > 1 and is_separator(lines[1]):
        rows.pop(1)
    columns = max(len(row) for row in rows)
    table = doc.add_table(rows=len(rows), cols=columns)
    table.autofit = True
    table.style = "Table Grid"
    table.alignment = 1
    for r, row_values in enumerate(rows):
        row_values = row_values + [""] * (columns - len(row_values))
        row = table.rows[r]
        prevent_row_split(row)
        if r == 0:
            set_repeat_table_header(row)
        for c, value in enumerate(row_values):
            cell = row.cells[c]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            set_cell_margins(cell)
            if r == 0:
                set_cell_shading(cell, PALE_BLUE)
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(0)
            para.paragraph_format.line_spacing = 1.0
            append_inline(para, value, base_size=7.2, base_color=BODY, bold=(r == 0))
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(3)
    spacer.paragraph_format.space_before = Pt(0)


def add_image(doc: Document, alt: str, relative_path: str) -> None:
    path = (SOURCE.parent / relative_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Report image not found: {path}")
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_before = Pt(3)
    caption.paragraph_format.space_after = Pt(4)
    run = caption.add_run(alt)
    set_run_font(run, size=8, color="526579", italic=True)
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.add_run().add_picture(str(path), width=Inches(IMAGE_WIDTH))


def setup_document(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)
    section.top_margin = Inches(0.62)
    section.bottom_margin = Inches(0.62)
    section.footer_distance = Inches(0.3)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = RGBColor.from_string(BODY)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08

    title = doc.styles["Title"]
    title.font.name = "Arial"
    title._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    title._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    title.font.size = Pt(23)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(12)
    title.paragraph_format.keep_with_next = True
    title_ppr = title._element.get_or_add_pPr()
    for border in title_ppr.findall(qn("w:pBdr")):
        title_ppr.remove(border)

    for name, size, before, after in (
        ("Heading 1", 15, 13, 6),
        ("Heading 2", 11.5, 9, 4),
        ("Heading 3", 10.2, 7, 3),
    ):
        style = doc.styles[name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(BLUE)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.paragraph_format.space_before = Pt(0)
    footer.paragraph_format.space_after = Pt(0)
    run = footer.add_run("Hitesh C  |  CSA06 CO3 Case Study  |  Page ")
    set_run_font(run, size=8, color="526579")
    page = footer.add_run()
    set_run_font(page, size=8, color="526579")
    add_field(page, "PAGE")

    doc.core_properties.title = "KartIQ Divide and Conquer Case Study"
    doc.core_properties.subject = "CSA06 CO3 AT3 case study report"
    doc.core_properties.author = "Hitesh C"


def build_document() -> None:
    doc = Document()
    setup_document(doc)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 0
    inside_code = False
    code_lines: list[str] = []

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if inside_code:
                para = doc.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.12)
                para.paragraph_format.right_indent = Inches(0.12)
                para.paragraph_format.space_before = Pt(3)
                para.paragraph_format.space_after = Pt(8)
                para.paragraph_format.line_spacing = 1.0
                for code_index, code_line in enumerate(code_lines):
                    if code_index:
                        para.add_run().add_break()
                    run = para.add_run(code_line)
                    set_run_font(run, name="Consolas", size=8.1, color=CODE)
                code_lines = []
                inside_code = False
            else:
                inside_code = True
            i += 1
            continue
        if inside_code:
            code_lines.append(line)
            i += 1
            continue

        image_match = re.match(r"!\[([^\]]*)\]\(([^\)]+)\)", line.strip())
        if image_match:
            add_image(doc, image_match.group(1), image_match.group(2))
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        if line.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            add_markdown_table(doc, rows)
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1:
                text = "KartIQ Divide and Conquer Case Study"
                paragraph = doc.add_paragraph(style="Title")
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = paragraph.add_run(text)
                set_run_font(run, size=23, color="000000", bold=True)
                paragraph_ppr = paragraph._p.get_or_add_pPr()
                for border in paragraph_ppr.findall(qn("w:pBdr")):
                    paragraph_ppr.remove(border)
            else:
                text = heading_text(text)
                paragraph = doc.add_paragraph(style=f"Heading {min(level, 3)}")
                paragraph.add_run(text)
                if text.casefold() == "program And Test Output Captures".casefold():
                    paragraph.paragraph_format.page_break_before = True
            i += 1
            continue
        if line.strip() in ("---", "___", "***"):
            i += 1
            continue
        if line.startswith("- "):
            para = doc.add_paragraph(style="List Bullet")
            para.paragraph_format.space_after = Pt(3)
            append_inline(para, line[2:])
            i += 1
            continue
        if re.match(r"^\d+\.\s", line):
            para = doc.add_paragraph(style="List Number")
            append_inline(para, re.sub(r"^\d+\.\s", "", line))
            i += 1
            continue

        paragraph_lines = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") \
                and not lines[i].strip().startswith(("|", "```", "![", "- ")) \
                and not re.match(r"^\d+\.\s", lines[i]):
            paragraph_lines.append(lines[i].strip())
            i += 1
        para = doc.add_paragraph()
        append_inline(para, " ".join(paragraph_lines))

    doc.save(OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build_document()
