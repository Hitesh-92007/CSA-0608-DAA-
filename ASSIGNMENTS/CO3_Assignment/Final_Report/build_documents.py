"""Build CO3 assignment report and contribution-record DOCX/PDF outputs."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Image as RLImage, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle, KeepTogether)

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "Final_Report"
RESULTS = ROOT / "Supporting_Files" / "Experimental_Results"
CHARTS = RESULTS / "Charts"
DIAGRAMS = ROOT / "Supporting_Files" / "Decomposition_Diagrams"


def rows(filename: str) -> list[dict[str, str]]:
    with (RESULTS / filename).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sec(name: str, paragraphs: list[str], table_file: str | None, columns: list[tuple[str, str]] | None,
        diagram: str | None = None, charts: list[str] | None = None) -> dict:
    return {"name": name, "paragraphs": paragraphs, "table_file": table_file, "columns": columns,
            "diagram": diagram, "charts": charts or []}


SECTIONS = [
    sec("Q1 Max Min and Binary Search", [
        "The max/min function uses a tournament-style divide-and-conquer recurrence. A one-item range returns the item twice; a two-item range needs one comparison. Larger ranges are split, solved recursively, and combined with one comparison for the minima and one for the maxima. The comparison counts match the power-of-two formula 3n/2 - 2 and improve on two independent scans, which use 2n - 2 comparisons.",
        "Binary Search is iterative over an ascending array. At each midpoint it tests equality and, if needed, whether the midpoint is below the target. The sorted-order invariant proves that the opposite half cannot contain the target. Its recurrence is T(n)=T(n/2)+O(1)=O(log n), with O(1) extra space."
    ], "q1_max_min_comparisons.csv", [("n", "n"), ("D&C comparisons", "dc_comparisons"), ("Two scans", "independent_comparisons"), ("D&C formula", "dc_expected_power2")],
       "q1_max_min_binary_search.png", ["q1_comparisons.png"]),
    sec("Q2 Merge Sort and Quick Sort", [
        "Merge Sort halves every input range, recursively sorts both halves, then merges in linear time. T(n)=2T(n/2)+Theta(n)=Theta(n log n), with Theta(n) auxiliary storage. Quick Sort uses the last element as the Lomuto pivot. The balanced case is an engineered distinct-key permutation that produces nearly equal partitions; the unbalanced case is ascending distinct data, for which each pivot leaves n-1 keys on one side.",
        "The measured recursion depths show the effect of decomposition directly. At n=511, balanced Quick Sort reaches depth 9; ascending input reaches depth 511 and takes 130,305 comparisons. Merge Sort remains at depth 10 and uses 2,295 comparisons on the ascending input. Quick Sort has average Theta(n log n) time but worst-case Theta(n^2); Merge Sort has predictable Theta(n log n) time. For unknown input, a randomized or introspective pivot strategy is safer unless stability or predictable worst-case performance makes Merge Sort preferable."
    ], "q2_sort_decomposition.csv", [("Case", "case"), ("n", "n"), ("Quick comps", "quick_comparisons"), ("Quick depth", "quick_depth"), ("Merge comps", "merge_comparisons"), ("Merge depth", "merge_depth")],
       "q2_sorting.png", ["q2_balanced_depth.png", "q2_unbalanced_depth.png"]),
    sec("Q3 Karatsuba Multiplication", [
        "The decimal operands are split at a common power-of-ten boundary: x=x1*10^m+x0 and y=y1*10^m+y0. The algorithm computes z0=x0*y0, z2=x1*y1, and z1=(x0+x1)(y0+y1)-z0-z2, then recombines the shifted terms. This replaces four recursive products with three. T(n)=3T(n/2)+Theta(n)=Theta(n^(log2 3)), approximately Theta(n^1.585), compared with Theta(n^2) schoolbook digit products.",
        "With a 24-digit base-case threshold, Karatsuba uses fewer base digit products at 32 digits and above. In the measured timings, schoolbook remains faster through 96 digits; Karatsuba first becomes faster at 128 digits and stays faster in the 192- and 256-digit samples. This run places the observed crossover between 96 and 128 digits for this implementation and runtime, not at a universal threshold. Integer conversion, recursion, and additions explain why fewer products do not guarantee a speedup for small inputs."
    ], "q3_karatsuba_experiments.csv", [("Digits", "digits"), ("Schoolbook products", "schoolbook_digit_products"), ("Karatsuba products", "karatsuba_digit_products"), ("Schoolbook s", "schoolbook_median_seconds"), ("Karatsuba s", "karatsuba_median_seconds")],
       "q3_karatsuba.png", ["q3_digit_products.png"]),
    sec("Q4 Strassen Matrix Multiplication", [
        "Conventional block multiplication forms eight half-size products. Strassen's identities reduce this to seven products M1 through M7, followed by block additions and subtractions. T(n)=7T(n/2)+Theta(n^2)=Theta(n^(log2 7)), approximately Theta(n^2.807), compared with conventional Theta(n^3). Non-power-of-two square matrices are zero-padded to the next power of two and cropped after multiplication; the implementation switches to conventional multiplication at a 16 by 16 cutoff.",
        "The operation counts favor Strassen from n=32 onward, but the wall-clock advantage starts only at larger sizes. In this run, conventional multiplication is slightly faster at n=32, while Strassen is faster at n=64 and n=128; the single n=256 run also favors Strassen. This places the observed crossover between 32 and 64 for this implementation, but the n=256 timing is not repeated and the threshold is not universal. Matrix additions, temporary allocations, cache behavior, and the small number of sizes limit the timing conclusion. Conventional multiplication remains a sensible choice for small or memory-constrained matrices."
    ], "q4_strassen_experiments.csv", [("n", "n"), ("Classical mults", "conventional_multiplications"), ("Strassen mults", "strassen_multiplications"), ("Strassen add/sub", "strassen_additions_subtractions"), ("Classical s", "conventional_median_seconds"), ("Strassen s", "strassen_median_seconds")],
       "q4_strassen.png", ["q4_multiplications.png"]),
    sec("Q5 Closest Pair of Points", [
        "The divide-and-conquer implementation sorts points by x and y, splits at the x-median, recursively solves both halves, and scans a y-ordered strip around the dividing line. With the current best distance as a bound, each strip point needs to be checked against at most the next seven points. Sorting and linear combine work at each level give T(n)=2T(n/2)+O(n)=O(n log n), while brute force checks n(n-1)/2 pairs in O(n^2) time.",
        "Both methods returned the same distance on every measured point set. At n=20, brute force is slightly faster despite doing 190 distance calculations versus 23 for the recursive method. From n=100, divide and conquer is faster in the observed runs; at n=1,600 it performs 2,174 distance calculations versus 1,279,200 for brute force. The Python reference uses copied slices and identity sets, so its actual temporary storage can reach O(n log n); a buffer-reuse implementation can reduce auxiliary storage to O(n)."
    ], "q5_closest_pair_experiments.csv", [("n", "n"), ("Brute distances", "brute_distance_calculations"), ("D&C distances", "dc_distance_calculations"), ("Brute s", "brute_median_seconds"), ("D&C s", "dc_median_seconds")],
       "q5_closest_pair.png", ["q5_distance_calculations.png"]),
    sec("Q6 Median of Medians and Meet in the Middle", [
        "Median of Medians groups values in fives, finds each group median, recursively selects the median of those medians, and partitions into less/equal/greater groups. The pivot guarantees constant-fraction elimination. T(n)<=T(n/5)+T(7n/10+O(1))+O(n), so worst-case time is O(n), with O(n) storage in this list-based version. Randomized QuickSelect is expected O(n) but worst-case O(n^2); first-pivot QuickSelect on ascending input demonstrates the poor-partition case. Randomization reduces the likelihood of bad pivots but cannot remove the worst-case bound.",
        "Meet-in-the-Middle splits a subset-sum input, enumerates each half, sorts one side's sums, and searches for a complement on the other side. Its time is O(n*2^(n/2)) and space is O(2^(n/2)), versus O(n*2^n) time for full enumeration. The no-solution experiments verify full enumeration through n=22; larger exhaustive counts in the table are theoretical counts, not executed timings. At n=34 the method stores 131,072 partial sums per half and completes in about 0.406 s in this run."
    ], "q6_selection_experiments.csv", [("n", "n"), ("MoM comps", "mom_comparisons"), ("Random QS comps", "random_quickselect_comparisons"), ("First-pivot comps", "first_pivot_sorted_comparisons"), ("MoM s", "mom_median_seconds"), ("Random QS s", "random_median_seconds")],
       "q6_advanced.png", ["q6_selection_comparisons.png", "q6_subset_search_space.png"]),
    sec("Q7 Day 4 Design Challenge: Maximum Subarray", [
        "The supplied assignment describes the Day-4 design stages but does not identify the challenge problem. This submission uses maximum contiguous subarray sum as a stated working example. The input is a non-empty integer array. A recursive call returns the best sum and its indices. The best interval is either in the left half, in the right half, or crosses the midpoint; the crossing candidate is built from the best left suffix and right prefix.",
        "The combine scan is linear, so T(n)=2T(n/2)+Theta(n)=Theta(n log n), using Theta(log n) recursion space. The brute-force reference checks all n(n+1)/2 segments in Theta(n^2) time. The outputs matched on the demonstration input and randomized harness inputs. For the selected sample, D&C uses 29 boundary sum updates versus 45 brute-force updates; at n=4,096 the experiment uses 49,152 versus 8,390,656 updates. If the class supplied a different Day-4 problem, replace this section and implementation before submission."
    ], "q7_maximum_subarray_experiments.csv", [("n", "n"), ("D&C updates", "dc_boundary_additions"), ("Brute updates", "brute_subarray_sum_updates"), ("D&C s", "dc_median_seconds"), ("Brute s", "brute_seconds")],
       "q7_max_subarray.png", ["q7_work_counts.png"]),
]

ROLE_ROWS = [
    ("Q1", "Max/min design, derivation; binary-search experiments", "Max/min instrumentation; binary-search elimination", "Implement/test both parts"),
    ("Q2", "Quick Sort partition experiments", "Merge Sort analysis and recursion-tree comparison", "Implement and compare both sorts"),
    ("Q3", "Karatsuba derivation and recurrence", "Crossover experiment and overhead analysis", "Implement both multipliers"),
    ("Q4", "Matrix experiments and engineering analysis", "Strassen algebra and correctness", "Implement and verify both methods"),
    ("Q5", "Closest-pair decomposition", "Equivalent-data comparison and evidence", "Implement and test both methods"),
    ("Q6", "Median of Medians; cross-explain Meet-in-the-Middle", "Meet-in-the-Middle; cross-explain pivot quality", "Verify the complete investigation"),
    ("Q7", "Independent proposal; recurrence and solution", "Independent proposal; implementation and tests", "Compare proposals, finalize and evaluate design"),
]

COMPLEXITY_ROWS = [
    ("Q1", "Max/min D&C", "Theta(n)", "3n/2-2 comparisons for powers of two", "Theta(log n) recursion"),
    ("Q1", "Binary Search", "Theta(log n)", "At most two key comparisons per iteration", "Theta(1) iterative"),
    ("Q2", "Merge Sort", "Theta(n log n)", "All cases", "Theta(n)"),
    ("Q2", "Quick Sort", "Average Theta(n log n); worst Theta(n^2)", "Pivot-dependent", "Worst recursion Theta(n)"),
    ("Q3", "Karatsuba", "Theta(n^1.585)", "3T(n/2)+Theta(n)", "Recursive temporaries"),
    ("Q4", "Strassen", "Theta(n^2.807)", "7T(n/2)+Theta(n^2)", "Temporary matrices"),
    ("Q5", "Closest pair D&C", "Theta(n log n)", "2T(n/2)+O(n)", "Reference slices can reach Theta(n log n)"),
    ("Q6", "Median of Medians", "Worst-case O(n)", "T(n/5)+T(7n/10)+O(n)", "O(n) list storage"),
    ("Q6", "Meet-in-the-Middle", "O(n*2^(n/2))", "Half-subsets + binary search", "O(2^(n/2))"),
    ("Q7", "Maximum subarray D&C", "Theta(n log n)", "2T(n/2)+Theta(n)", "Theta(log n) recursion"),
]


def md_table(headers: list[str], data: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    out.extend("| " + " | ".join(row) + " |" for row in data)
    return "\n".join(out)


def build_markdown() -> None:
    parts = ["# CO3 Assignment 3 Divide and Conquer Algorithms", "",
             "**Course:** CSA06 Design and Analysis of Algorithms  ",
             "**Student:** Hitesh C, Register No. 192524005  ",
             "**Partner:** [Add partner name and register number]  ",
             "**Assignment mode:** Pair work  ",
             "**Question set:** Q1-Q7", "",
             "## Executive summary", "",
             "This report presents implementations and measured comparisons for seven divide-and-conquer investigations: max/min and binary search; Merge Sort and Quick Sort; Karatsuba multiplication; Strassen multiplication; closest pair; Median of Medians and Meet-in-the-Middle; and a maximum-subarray design challenge. Programs were run, their compared outputs were checked, and the test harness passed ten test groups covering 50 deterministic randomized inputs plus edge cases.",
             "",
             "Q7 uses maximum-subarray sum as a working example because the supplied question file specifies the design process but not the actual challenge problem. Confirm this choice against the instructor's Day-4 prompt. The partner name, actual per-person contributions, and authentic pre-discussion Q7 proposals are left for both students to complete; the report does not claim that unverified pair-work steps have already happened.",
             "",
             "## Method and evidence", "",
             "Programs use Python 3.10 or later. The experiment generator uses fixed seed 192524005. Counts are instrumented algorithm operations; timing values are medians of three runs except where the table explicitly records one run. Timing values depend on runtime and machine. CSV files preserve raw results. Output images are rendered from each program's saved stdout log, not captured from a live terminal window.",
             "",
             "The selected input sizes are stated in the experiment tables because the question file does not provide numeric size ranges. Correctness was checked against independent/reference implementations, including randomized tests for sorting, multiplication, matrix products, closest pair, selection, subset sum, and maximum subarray.",
             ""]
    for section in SECTIONS:
        parts += [f"## {section['name']}", ""]
        parts += [p + "\n" for p in section["paragraphs"]]
        if section["table_file"]:
            data = rows(section["table_file"])
            cols = section["columns"]
            parts += [md_table([x[0] for x in cols], [[r[x[1]] for x in cols] for r in data]), ""]
        if section["diagram"]:
            parts += [f"![Decomposition diagram](../Supporting_Files/Decomposition_Diagrams/{section['diagram']})", ""]
        for chart_name in section["charts"]:
            parts += [f"![Experimental graph](../Supporting_Files/Experimental_Results/Charts/{chart_name})", ""]
    parts += ["## Complexity summary", "", md_table(["Question", "Algorithm", "Time", "Recurrence / operation note", "Space"], [list(r) for r in COMPLEXITY_ROWS]), "",
              "## Technical conclusions", "",
              "- The max/min tournament meets its comparison bound, and binary search benefits from sorted order by discarding half the remaining keys.",
              "- Merge Sort has predictable recursion depth. Last-pivot Quick Sort is highly sensitive to input order; use a guarded pivot strategy when input characteristics are unknown.",
              "- Karatsuba reduced digit products and became faster only beyond the measured small-input range. Select its cutoff empirically.",
              "- Strassen's measured timing crossover was between n=32 and n=64 in this run; the threshold requires broader repeated measurements.",
              "- Divide-and-conquer closest pair reduced distance calculations sharply and was faster from the tested n=100 point set onward.",
              "- Median of Medians provides deterministic worst-case selection; randomized QuickSelect was faster in these samples but does not provide the same worst-case guarantee.",
              "- Meet-in-the-Middle is useful when 2^(n/2) storage is feasible. Its memory requirement is the main limit.",
              "- Divide-and-conquer maximum subarray outperformed the brute-force baseline as n increased, although Kadane's linear algorithm is preferable if only the final answer is needed and the assignment does not require D&C.",
              "",
              "## Pair contribution record", "",
              "The table below reproduces the primary roles prescribed by the assignment. The companion Student Contribution Record document has blank fields for actual work, names, dates, and confirmations. Both students must complete these fields truthfully. The Q7 proposal templates are intentionally blank for each student's independent pre-discussion work.", "",
              md_table(["Question", "Student A primary role", "Student B primary role", "Joint work"], [list(r) for r in ROLE_ROWS]), "",
              "## Output evidence", "",
              "Each question folder contains the program's plain-text output and a matching image capture rendered from that stdout. The report builder includes these images in the appendix. Source code, pseudocode, diagrams, CSV data, and test logs are available beside the report.", "",
              "## References", "",
              "- Cormen, Leiserson, Rivest, and Stein, Introduction to Algorithms, 4th edition. Divide-and-conquer, sorting, selection, and matrix multiplication chapters.",
              "- The CO3 Assignment 3 question sheet supplied with this submission.", ""]
    FINAL.mkdir(parents=True, exist_ok=True)
    (FINAL / "CO3_Assignment_Report.md").write_text("\n".join(parts), encoding="utf-8")


def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), fill); tc_pr.append(shd)


def set_cell_borders(cell, color="D9D9D9") -> None:
    tc = cell._tc; tc_pr = tc.get_or_add_tcPr(); borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge); el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "5"); el.set(qn("w:color"), color); borders.append(el)
    tc_pr.append(borders)


def style_doc(doc: Document, title: str) -> None:
    section = doc.sections[0]; section.page_width = Inches(8.5); section.page_height = Inches(11)
    section.top_margin = Inches(.68); section.bottom_margin = Inches(.68); section.left_margin = Inches(.72); section.right_margin = Inches(.72)
    normal = doc.styles["Normal"]; normal.font.name = "Aptos"; normal.font.size = Pt(9.5); normal.font.color.rgb = RGBColor(35, 48, 58)
    normal.paragraph_format.space_after = Pt(6); normal.paragraph_format.line_spacing = 1.08
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        st = doc.styles[name]; st.font.name = "Aptos Display"; st.font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Title"].font.size = Pt(27)
    doc.styles["Heading 1"].font.size = Pt(17)
    doc.styles["Heading 1"].paragraph_format.space_before = Pt(7); doc.styles["Heading 1"].paragraph_format.space_after = Pt(7)
    doc.styles["Heading 2"].font.size = Pt(12)
    doc.core_properties.title = title; doc.core_properties.author = "Hitesh C"


def add_word_table(doc: Document, headers: list[str], data: list[list[str]], font_size=8.1) -> None:
    table = doc.add_table(rows=1, cols=len(headers)); table.autofit = True
    table.style = "Table Grid"
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]; cell.text = header; shade(cell, "173A50")
    for row_index, row in enumerate(data):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            if row_index % 2:
                shade(cells[i], "F2F6F8")
    for row_index, row in enumerate(table.rows):
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_borders(cell)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)
                for run in p.runs:
                    run.font.name = "Aptos"; run.font.size = Pt(font_size)
                    if row_index == 0:
                        run.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph()


def add_figure_docx(doc: Document, path: Path, caption: str, width=6.65) -> None:
    if not path.exists():
        return
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Inches(width))
    cap = doc.add_paragraph(caption); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in cap.runs:
        r.italic = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor(75, 90, 100)


def build_report_docx() -> None:
    doc = Document(); style_doc(doc, "CO3 Assignment 3 Divide and Conquer Algorithms")
    title = doc.add_paragraph(style="Title"); title.add_run("CO3 Assignment 3\nDivide and Conquer Algorithms")
    p = doc.add_paragraph("CSA06 Design and Analysis of Algorithms"); p.runs[0].font.size = Pt(15)
    doc.add_paragraph("Q1-Q7 technical report and experimental comparison")
    doc.add_paragraph("Student: Hitesh C  |  Register No.: 192524005")
    doc.add_paragraph("Partner: [Add partner name and register number]")
    doc.add_paragraph("Pair assignment | CO3")
    doc.add_paragraph("Prepared from the supplied assignment brief and recorded program runs")
    doc.add_page_break()
    doc.add_heading("Executive summary", 1)
    doc.add_paragraph("This report presents implementations and measured comparisons for seven divide-and-conquer investigations: max/min and binary search; Merge Sort and Quick Sort; Karatsuba multiplication; Strassen multiplication; closest pair; Median of Medians and Meet-in-the-Middle; and a maximum-subarray design challenge. Programs were run, compared outputs were checked, and the harness passed ten test groups covering 50 deterministic randomized inputs plus edge cases.")
    doc.add_paragraph("Q7 uses maximum-subarray sum as a working example because the supplied question file specifies the design process but not the actual challenge problem. Confirm this choice against the instructor's Day-4 prompt. Partner identity, actual per-person contributions, and authentic pre-discussion Q7 proposals must be completed by both students; they are not represented as verified facts here.")
    doc.add_heading("Method and evidence", 1)
    doc.add_paragraph("Programs use Python 3.10 or later. Experiments use fixed seed 192524005. Operation counts are instrumented algorithm work. Timings are medians of three runs except where stated otherwise, and vary by runtime and machine. CSV files retain the measurements. Output images are rendered from each program's saved stdout log, not from a live terminal window.")
    doc.add_paragraph("The question file gives no numeric ranges for experiment sizes, so each question states the selected sizes in its CSV and table. Correctness was checked against reference implementations for sorting, multiplication, matrix products, closest pair, selection, subset sum, and maximum subarray.")
    for section in SECTIONS:
        doc.add_page_break(); doc.add_heading(section["name"], 1)
        for text in section["paragraphs"]:
            doc.add_paragraph(text)
        if section["table_file"]:
            data = rows(section["table_file"]); cols = section["columns"]
            add_word_table(doc, [x[0] for x in cols], [[r[x[1]] for x in cols] for r in data])
        if section["diagram"]:
            add_figure_docx(doc, DIAGRAMS / section["diagram"], "Decomposition diagram")
        for chart_name in section["charts"]:
            add_figure_docx(doc, CHARTS / chart_name, chart_name.replace("_", " ").replace(".png", ""))
    doc.add_page_break(); doc.add_heading("Complexity summary", 1)
    add_word_table(doc, ["Q", "Algorithm", "Time", "Recurrence / operation note", "Space"], [list(r) for r in COMPLEXITY_ROWS], 7.7)
    doc.add_heading("Technical conclusions", 1)
    for item in [
        "The max/min tournament meets its comparison bound, and Binary Search discards the half that cannot contain the key.",
        "Merge Sort has predictable recursion depth. Last-pivot Quick Sort is input-sensitive; use a guarded pivot strategy when input characteristics are unknown.",
        "Karatsuba reduced digit products and crossed the measured timing range only at larger operands. Its cutoff should be measured.",
        "Strassen reduced multiplication counts, but measured runtime did not show a stable crossover through n=256.",
        "Closest-pair divide and conquer sharply reduced distance evaluations and became faster on the tested sets by n=100.",
        "Median of Medians offers a deterministic worst-case selection bound; randomized QuickSelect was faster on these samples but retains a quadratic worst case.",
        "Meet-in-the-Middle reduces the enumeration space at the cost of storing half-subset sums.",
        "For a production maximum-subarray request, Kadane's linear method is preferable if a D&C design is not required."
    ]:
        doc.add_paragraph(item, style="List Bullet")
    doc.add_page_break(); doc.add_heading("Prescribed pair responsibilities", 1)
    doc.add_paragraph("This table reproduces the primary role allocation stated in the assignment. It is not a claim that a student completed that work. Use the companion contribution record to add the work actually completed by each partner.")
    add_word_table(doc, ["Q", "Student A primary role", "Student B primary role", "Shared work"], [list(r) for r in ROLE_ROWS], 7.7)
    doc.add_paragraph("Before submission, both partners should add names, actual contributions, dates, and their independently completed Q7 proposals. The contribution document contains fillable fields for those items.")
    doc.add_heading("References", 1)
    doc.add_paragraph("Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C. Introduction to Algorithms, 4th edition. Divide-and-conquer, sorting, selection, and matrix multiplication sections.")
    doc.add_paragraph("CSA06 Assignment 3 CO3 question sheet supplied for this work.")
    doc.add_page_break(); doc.add_heading("Appendix A: output evidence", 1)
    doc.add_paragraph("Each image below is a legible output capture rendered from the matching saved program stdout. The adjacent RUN_OUTPUT.txt file preserves the plain-text output.")
    q_dirs = ["Q1_MaxMin_Binary_Search", "Q2_MergeSort_QuickSort", "Q3_Karatsuba_Multiplication",
              "Q4_Strassen_Matrix_Multiplication", "Q5_Divide_Conquer_Closest_Pair",
              "Q6_Advanced_Divide_Conquer", "Q7_Day4_Design_Challenge"]
    for q in q_dirs:
        doc.add_heading(q.replace("_", " "), 2)
        add_figure_docx(doc, ROOT / q / "Output_Screenshots" / "output_capture.png", "Program output capture", width=6.65)
    doc.add_page_break(); doc.add_heading("Appendix B: automated test results", 1)
    test_log = (ROOT / "Supporting_Files" / "test_output.txt").read_text(encoding="utf-8-sig")
    p = doc.add_paragraph()
    run = p.add_run(test_log); run.font.name = "Consolas"; run.font.size = Pt(8)
    FINAL.mkdir(parents=True, exist_ok=True)
    doc.save(FINAL / "CO3_Assignment_Report.docx")


def pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=31, textColor=colors.HexColor("#000000"), alignment=TA_CENTER, spaceAfter=16))
    styles.add(ParagraphStyle(name="ReportH1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#000000"), spaceBefore=7, spaceAfter=8, keepWithNext=True))
    styles.add(ParagraphStyle(name="ReportH2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#000000"), spaceBefore=6, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="ReportBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=13, spaceAfter=7))
    styles.add(ParagraphStyle(name="TableText", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.3, leading=9, spaceAfter=0))
    styles.add(ParagraphStyle(name="SmallCaption", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=colors.HexColor("#4b5a64"), alignment=TA_CENTER, spaceAfter=8))
    return styles


def pdf_table(headers: list[str], data: list[list[str]], widths: list[float] | None = None) -> Table:
    style = pdf_styles()
    matrix = [[Paragraph(str(x), style["TableText"]) for x in headers]] + [[Paragraph(str(x), style["TableText"]) for x in r] for r in data]
    table = Table(matrix, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173A50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#D9D9D9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(matrix)):
        if i % 2 == 0:
            commands.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F2F6F8")))
    table.setStyle(TableStyle(commands))
    return table


def pdf_image(path: Path, max_w=6.9*inch, max_h=4.2*inch) -> RLImage | None:
    if not path.exists():
        return None
    img = RLImage(str(path)); scale = min(max_w/img.imageWidth, max_h/img.imageHeight)
    img.drawWidth = img.imageWidth*scale; img.drawHeight = img.imageHeight*scale
    img.hAlign = "CENTER"
    return img


def build_report_pdf() -> None:
    styles = pdf_styles(); story = []
    story += [Spacer(1, 1.25*inch), Paragraph("CO3 Assignment 3<br/>Divide and Conquer Algorithms", styles["ReportTitle"]),
              Paragraph("CSA06 Design and Analysis of Algorithms", styles["ReportBody"]), Spacer(1, .35*inch),
              Paragraph("Q1-Q7 technical report and experimental comparison", styles["ReportBody"]),
              Spacer(1, .4*inch), Paragraph("Student: Hitesh C  |  Register No.: 192524005", styles["ReportBody"]),
              Paragraph("Partner: [Add partner name and register number]", styles["ReportBody"]),
              Paragraph("Pair assignment | CO3", styles["ReportBody"]), PageBreak()]
    story += [Paragraph("Executive summary", styles["ReportH1"]),
              Paragraph("This report presents implementations and measured comparisons for seven divide-and-conquer investigations: max/min and binary search; Merge Sort and Quick Sort; Karatsuba multiplication; Strassen multiplication; closest pair; Median of Medians and Meet-in-the-Middle; and a maximum-subarray design challenge. Programs were run, compared outputs were checked, and the harness passed ten test groups covering 50 deterministic randomized inputs plus edge cases.", styles["ReportBody"]),
              Paragraph("Q7 uses maximum-subarray sum as a working example because the supplied question file specifies the design process but not the actual challenge problem. Confirm this choice against the instructor's Day-4 prompt. Partner identity, actual per-person contributions, and authentic pre-discussion Q7 proposals must be completed by both students; they are not represented as verified facts here.", styles["ReportBody"]),
              Paragraph("Method and evidence", styles["ReportH1"]),
              Paragraph("Programs use Python 3.10 or later. Experiments use fixed seed 192524005. Operation counts are instrumented algorithm work. Timings are medians of three runs except where stated otherwise, and vary by runtime and machine. CSV files retain the measurements. Output images are rendered from each program's saved stdout log, not from a live terminal window. The question file does not state numeric ranges; selected sizes are recorded in the result tables.", styles["ReportBody"]), PageBreak()]
    for index, section in enumerate(SECTIONS):
        if index > 0:
            story.append(PageBreak())
        story.append(Paragraph(section["name"], styles["ReportH1"]))
        for text in section["paragraphs"]:
            story.append(Paragraph(text, styles["ReportBody"]))
        if section["table_file"]:
            data = rows(section["table_file"]); cols = section["columns"]
            if len(cols) == 7:
                widths = [0.4*inch, .85*inch, .92*inch, .9*inch, .75*inch, .8*inch, .75*inch]
            else:
                widths = None
            story.append(pdf_table([x[0] for x in cols], [[r[x[1]] for x in cols] for r in data], widths))
            story.append(Spacer(1, 9))
        image = pdf_image(DIAGRAMS / section["diagram"], max_w=6.8*inch, max_h=1.55*inch) if section["diagram"] else None
        if image:
            story.append(KeepTogether([image, Paragraph("Decomposition diagram", styles["SmallCaption"])]))
        for chart_name in section["charts"]:
            image = pdf_image(CHARTS / chart_name, max_w=6.8*inch, max_h=3.6*inch)
            if image:
                story.append(KeepTogether([image, Paragraph(chart_name.replace("_", " ").replace(".png", ""), styles["SmallCaption"])]))
        story.append(Spacer(1, 10))
    story += [PageBreak(), Paragraph("Complexity summary", styles["ReportH1"]),
              pdf_table(["Q", "Algorithm", "Time", "Recurrence / operation note", "Space"], [list(r) for r in COMPLEXITY_ROWS],
                        [0.35*inch, 1.05*inch, 1.35*inch, 2.25*inch, 1.65*inch]), Spacer(1, 14),
              Paragraph("Technical conclusions", styles["ReportH1"])]
    for item in [
        "The max/min tournament meets its comparison bound; Binary Search uses sorted order to discard half the search space.",
        "Merge Sort is predictable, while last-pivot Quick Sort can degrade to quadratic work on ordered input.",
        "Karatsuba's observed timing crossover was between 96 and 128 digits for the measured threshold and runtime.",
        "Strassen's measured timing crossover was between n=32 and n=64 in this run; the timing threshold requires broader repeated measurements.",
        "Divide-and-conquer closest pair reduced distance calculations and was faster from the tested n=100 case.",
        "Median of Medians provides a worst-case linear selection bound; randomized QuickSelect was faster in these samples but can be quadratic.",
        "Meet-in-the-Middle reduces the exponential search space by using memory for half-subset sums.",
        "Kadane's linear algorithm is preferable for production maximum-subarray queries when D&C is not a course requirement."
    ]:
        story.append(Paragraph("• " + item, styles["ReportBody"]))
    story += [PageBreak(), Paragraph("Prescribed pair responsibilities", styles["ReportH1"]),
              Paragraph("This table lists primary responsibilities from the assignment brief. It is not a claim that either student has completed that work. Both partners should complete actual contributions and independently authored Q7 proposals in the companion record.", styles["ReportBody"]),
              pdf_table(["Q", "Student A", "Student B", "Joint work"], [list(r) for r in ROLE_ROWS],
                        [.35*inch, 2.1*inch, 2.1*inch, 2.1*inch]), PageBreak(),
              Paragraph("Appendix A: output evidence", styles["ReportH1"]),
              Paragraph("Output images are rendered from the saved stdout of each run; matching text logs are stored in the question folders.", styles["ReportBody"])]
    q_dirs = ["Q1_MaxMin_Binary_Search", "Q2_MergeSort_QuickSort", "Q3_Karatsuba_Multiplication",
              "Q4_Strassen_Matrix_Multiplication", "Q5_Divide_Conquer_Closest_Pair",
              "Q6_Advanced_Divide_Conquer", "Q7_Day4_Design_Challenge"]
    for q in q_dirs:
        story.append(Paragraph(q.replace("_", " "), styles["ReportH2"]))
        image = pdf_image(ROOT/q/"Output_Screenshots"/"output_capture.png", max_w=6.8*inch, max_h=3.2*inch)
        if image:
            story += [image, Spacer(1, 9)]
    story += [PageBreak(), Paragraph("Appendix B: automated test results", styles["ReportH1"])]
    test_text = (ROOT / "Supporting_Files" / "test_output.txt").read_text(encoding="utf-8-sig")
    for line in test_text.splitlines():
        story.append(Paragraph(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), styles["TableText"]))
    FINAL.mkdir(parents=True, exist_ok=True)
    pdf = SimpleDocTemplate(str(FINAL/"CO3_Assignment_Report.pdf"), pagesize=letter,
                            rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.58*inch, bottomMargin=.58*inch,
                            title="CO3 Assignment 3 Divide and Conquer Algorithms", author="Hitesh C")
    pdf.build(story)


def build_contribution_record() -> None:
    doc = Document(); style_doc(doc, "CO3 Student Contribution Record")
    doc.add_paragraph("CO3 Student Contribution Record", style="Title")
    doc.add_paragraph("CSA06 Design and Analysis of Algorithms | Assignment 3")
    doc.add_paragraph("Student A name and register number: __________________________________________")
    doc.add_paragraph("Student B name and register number: __________________________________________")
    doc.add_paragraph("This form records the work actually completed. Primary roles below come from the question sheet; they do not prove that work was done. Both students should complete the actual-work fields, dates, and initials together before submission.")
    doc.add_heading("Primary responsibilities and actual work", 1)
    headers = ["Q", "Student A role from brief", "Student B role from brief", "Actual work completed by each student", "Date / initials"]
    data = [[q, a, b, "A: ____________________\nB: ____________________", "__________"] for q, a, b, _joint in ROLE_ROWS]
    add_word_table(doc, headers, data, 7.2)
    doc.add_heading("Q7 independent design proposals", 1)
    doc.add_paragraph("Each student should complete a separate initial proposal before discussing the challenge. Save the original proposal and add the completion date. The blank templates in Student_A_Initial_Design and Student_B_Initial_Design can be completed separately.")
    for label in ["Student A proposal completed independently before discussion", "Student B proposal completed independently before discussion"]:
        doc.add_paragraph(label, style="Heading 2")
        for item in ["Decomposition:", "Base case:", "Information returned:", "Combine strategy:", "Date and initials:"]:
            doc.add_paragraph(item + " ______________________________________________________________")
    doc.add_heading("Q7 design comparison and joint validation", 1)
    for item in ["Where the proposals agreed:", "Where they differed:", "Ideas kept and reasons:", "Final design change after discussion:", "Student A initials and date:", "Student B initials and date:"]:
        doc.add_paragraph(item + " ______________________________________________________________")
    doc.add_heading("Cross-understanding check", 1)
    doc.add_paragraph("Student A explained Student B's primary area: ______________________________ Date: __________")
    doc.add_paragraph("Student B explained Student A's primary area: ______________________________ Date: __________")
    doc.add_paragraph("Both students confirm that this record describes the work actually completed.")
    doc.add_paragraph("Student A signature: ______________________________  Date: ______________")
    doc.add_paragraph("Student B signature: ______________________________  Date: ______________")
    FINAL.mkdir(parents=True, exist_ok=True)
    doc.save(FINAL / "Student_Contribution_Record.docx")


def main() -> None:
    build_markdown(); build_report_docx(); build_contribution_record(); build_report_pdf()
    print("Built report Markdown, report Word/PDF, and contribution record Word document.")


if __name__ == "__main__":
    main()
