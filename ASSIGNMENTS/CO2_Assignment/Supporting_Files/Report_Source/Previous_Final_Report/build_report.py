"""Build the CO2 report in Markdown and Word from the saved experiment CSVs."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "Final_Report"
RESULTS = ROOT / "Supporting_Files" / "results"
FINAL.mkdir(parents=True, exist_ok=True)


def read_csv(name):
    with (RESULTS / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


q1 = read_csv("q1_sorting_results.csv")
q2 = read_csv("q2_sequential_search_results.csv")
q3 = read_csv("q3_string_matching_results.csv")
q4 = read_csv("q4_brute_closest_pair_results.csv")
q5 = read_csv("q5_convex_hull_results.csv")
q6 = read_csv("q6_exhaustive_search_results.csv")
q7 = read_csv("q7_redesign_comparison.csv")

main_cases = ["random_800", "95pct_ordered_plus_40_arrivals", "reverse_800"]
q1_table = [
    [r["case"], r["algorithm"], r["comparisons"], r["swaps"], r["moves"],
     f"{float(r['seconds']):.6f}"]
    for r in q1 if r["case"] in main_cases
]
q2_table = [[r["list_size"], r["case"], r["returned_index"], r["comparisons"]]
            for r in q2]
q3_table = [[r["case"], r["text_length"], r["pattern_length"],
             r["match_positions"], r["comparisons"]] for r in q3]
q4_table = [[r["n"], r["distance_calculations"], f"{float(r['minimum_distance']):.3f}",
             f"{float(r['seconds']):.6f}"] for r in q4]
q5_table = [[r["points"], r["candidate_pairs"], r["orientation_tests"],
             r["hull_vertices"]] for r in q5]
q6_table = [[r["packages"], r["candidate_subsets"], r["item_checks"],
             r["best_weight"], r["best_value"], f"{float(r['seconds']):.4f}"]
            for r in q6]
q7_table = [[r["n"], r["brute_distance_calculations"],
             r["dc_distance_calculations"],
             f"{float(r['distance_calculation_reduction_percent']):.2f}%",
             "Yes" if abs(float(r["brute_distance"]) -
                          float(r["dc_distance"])) < 1e-9 else "No",
             f"{float(r['brute_seconds']):.6f}",
             f"{float(r['dc_seconds']):.6f}"] for r in q7]

q4_last = q4[-1]
q4_threshold_n = int(round(
    int(q4_last["n"]) *
    (1.0 / float(q4_last["seconds"])) ** 0.5
))
q2_expected_comparisons = 0.9 * (20_000 + 1) / 2 + 0.1 * 20_000
q2_hourly_comparisons = int(round(q2_expected_comparisons * 50_000))
q6_last = q6[-1]
q6_next_checks = 21 * (2 ** 21)
q6_next_seconds = float(q6_last["seconds"]) * q6_next_checks / int(q6_last["item_checks"])


def table_md(headers, rows):
    lines = ["| " + " | ".join(map(str, headers)) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(map(str, row)) + " |" for row in rows)
    return "\n".join(lines)


sections = [
    ("h1", "CO2 Assignment Report"),
    ("p", "CSA06 Design and Analysis of Algorithms"),
    ("p", "Course Outcome 2 - Brute Force and Exhaustive Search"),
    ("p", "Student: Hitesh C | Register number: 192524005 | Assignment type: Individual"),
    ("p", f"Report date: {date(2026, 11, 15).strftime('%d %B %Y')}"),
    ("p", "This report studies the seven assigned problems using operation counts as the main evidence and elapsed time as supporting evidence. The experiments show where simple exhaustive methods are suitable, where input order changes performance, and why the Q4 closest-pair scan becomes expensive. The Q7 redesign reuses the same closest-pair input sets and returns the same measured minimum distances with substantially fewer distance calculations."),
    ("p", "Programming and report drafting assistance was used. The test harness and experiment scripts are included so the student can rerun, review, and explain the submitted work."),
    ("h1", "Scope and Method"),
    ("p", "The assignment covers Selection, Bubble, and Insertion Sort; Sequential Search; Brute-Force String Matching; Brute-Force Closest Pair; a supporting-line Brute-Force Convex Hull; Exhaustive Search for a payload-limited package set; and a redesign of one measured bottleneck. The provided question text leaves the requested dataset-size range blank. The selected sizes are therefore stated explicitly in the tables and are not presented as instructor-specified limits."),
    ("p", "The scripts use deterministic datasets and count comparisons, swaps, movements, orientation tests, candidate subsets, or distance calculations as appropriate. Timings are single-run local measurements on Python 3.12.14 and should be treated as environment-dependent. The CSV files retain the raw measurements. The included test harness checks edge cases and compares the geometric implementations with independent references."),
    ("h1", "Q1 Sorting Under Different Data Conditions"),
    ("p", "Prediction before the run: Selection Sort should make nearly the same number of comparisons for every arrangement. Bubble Sort should improve when input is already ordered but still do many comparisons when inversions remain. Insertion Sort should be the strongest of these three when only a small arrival batch disturbs an ordered list, and the weakest on reverse order."),
    ("p", "The nearly ordered test starts with 760 ordered values and appends 40 new priority scores. The random and reverse tests contain 800 values. Duplicate, empty, and single-element inputs are also checked. All three implementations are compared with Python's sorted result."),
    ("table", ["Input", "Algorithm", "Comparisons", "Swaps", "Moves", "Seconds"], q1_table),
    ("p", "Observed result: on the nearly ordered list, Insertion Sort used 15,697 key comparisons and 15,699 movements, compared with 319,600 comparisons for Selection Sort and 319,555 for Bubble Sort. On reverse order, Insertion Sort used 319,600 comparisons and 320,399 movements. The measured random case also confirms that these quadratic methods are poor choices for large unrestricted lists."),
    ("p", "Decision: among the three required algorithms, use Insertion Sort for small batches added to a list that remains almost ordered. It is adaptive and shifts only the elements that need to move. If the list becomes large or frequently disordered, use a production sorting method with an O(n log n) guarantee instead. This recommendation applies to the stated 95-percent-ordered workload, not to every input arrangement."),
    ("image", "Supporting_Files/results/q1_sorting_comparisons.png", "Figure 1. Sorting comparison counts for the tested arrangements."),
    ("h1", "Q2 Sequential Search"),
    ("p", "Sequential Search is useful when the temporary list is small, changes continuously, and is searched only occasionally. It needs no ordering or index construction, which can matter when records are inserted and removed often. A successful search at zero-based position k takes k+1 comparisons; an unsuccessful search takes n."),
    ("table", ["List size", "Case", "Returned index", "Comparisons"], q2_table),
    ("p", "The experiments match the position-based prediction: first-position hits take one comparison, middle hits take about n/2, and last-position or unsuccessful searches take n. For the changed condition, assume 20 facilities have 1,000 active records each (20,000 total), 50,000 requests arrive per hour, 90 percent are successful at uniformly distributed positions, and 10 percent miss. Expected comparisons are approximately 11,000.45 per request, or about 550,022,500 per hour. These figures describe the stated model, not measured workload data."),
    ("p", "Decision: retain Sequential Search for small, low-frequency temporary lists. With 20 facilities and a high request rate, use a hash index keyed by tool ID or a database index, and update it as tools are issued and returned. The data changes do not remove the need to meet lookup latency."),
    ("h1", "Q3 Brute-Force String Matching"),
    ("p", "The implementation tries each possible text alignment and stops an alignment at its first mismatching character. The fast case uses a short text with a match at the start. The high-work case uses a long run of A characters and a pattern that matches almost all of each window before a final mismatch, with a valid match at the last alignment. The third case checks overlapping occurrences."),
    ("table", ["Test", "Text length", "Pattern length", "Match positions", "Character comparisons"], q3_table),
    ("p", "The late near-match performs 247,600 character comparisons: 4,951 failed alignments each compare 50 characters, and the final alignment compares all 50 characters and matches. The overlapping example returns positions 0, 2, and 4. Text length alone does not predict cost; repeated prefix matches and the location of a mismatch determine how much work each alignment performs."),
    ("p", "Worst-case time is O((n-m+1)m), commonly written O(nm), where n is text length and m is pattern length. Extra working space is O(1), excluding the returned list of match positions."),
    ("h1", "Q4 Brute-Force Closest Pair"),
    ("p", "The program visits each unordered pair once by setting j greater than i. It compares squared distances and takes one square root after finding the minimum. Thus it performs exactly n(n-1)/2 distance calculations and uses constant auxiliary space."),
    ("table", ["Points n", "Distance calculations", "Minimum distance", "Seconds"], q4_table),
    ("p", f"At 2,000 points the measured scan makes {int(q4_last['distance_calculations']):,} distance calculations and takes {float(q4_last['seconds']):.3f} seconds. Using a one-second response target and quadratic scaling from this run gives an estimated limit near {q4_threshold_n:,} points. This is a rough extrapolation from one computer and one point distribution, not a hard capacity guarantee. The source of the inefficiency is examining every possible pair, even when most pairs are far apart."),
    ("h1", "Q5 Brute-Force Convex Hull"),
    ("p", "For each candidate line through two points, the program checks the sign of the cross product for the other points. If both positive and negative signs occur, points lie on both sides and the pair cannot be a supporting boundary edge. If all points lie on one side or on the line, the segment is accepted only when no collinear point lies outside it. The accepted edges form a graph that is walked to list the boundary vertices."),
    ("table", ["Points", "Candidate pairs", "Orientation tests", "Hull vertices"], q5_table),
    ("p", "The two designed examples include interior points, duplicate coordinates, and collinear boundary points; a fully collinear set is also tested. The independent randomized test compares the returned hull vertices with a monotone-chain reference on 60 point sets. A supporting line proves that the point set is contained in one closed half-plane, so the accepted extreme segment lies on the convex boundary. The collinear segment check is needed to avoid accepting a shorter segment when another point extends beyond it."),
    ("p", "There are n(n-1)/2 candidate pairs. In the worst case, each pair may inspect n-2 other points, giving O(n^3) time. Early rejection makes the measured orientation count data-dependent. Space is O(n+h), where h is the number of hull vertices and graph edges. Floating-point coordinates close to collinear can create numerical sensitivity; production geometry should use scaled integers or a robust orientation predicate."),
    ("image", "Supporting_Files/results/q5_orientation_growth.png", "Figure 2. Orientation tests on the chosen convex-position datasets."),
    ("h1", "Q6 Exhaustive Search"),
    ("p", "Each bit mask represents one package subset. The program evaluates the total weight and humanitarian value for all 2^n masks, keeps only subsets that satisfy the payload limit, and retains the feasible subset with the largest value."),
    ("p", "For the independently checkable four-package example with capacity 15, packages A and B weigh 10 and 5 and deliver values 60 and 40. The program returns A+B with total weight 15 and value 100. The alternative C+D+B has the same weight and value 90, so the returned result is the verified optimum."),
    ("table", ["Packages n", "Candidate subsets", "Item checks", "Best weight", "Best value", "Seconds"], q6_table),
    ("p", f"The candidate count doubles whenever one package is added. The implementation performs n item checks per subset, so its direct loop is O(n2^n) time. At n=20 it evaluates {int(q6_last['candidate_subsets']):,} subsets and {int(q6_last['item_checks']):,} item checks in {float(q6_last['seconds']):.2f} seconds on this run. With a three-second response budget, n=20 is the largest tested size accepted for this environment. The n=21 case would require {q6_next_checks:,} item checks and is projected at about {q6_next_seconds:.2f} seconds from the measured item-check rate, so it is outside that budget. This projection is not a separate timing measurement."),
    ("image", "Supporting_Files/results/q6_subset_growth.png", "Figure 3. Candidate subsets double with each added package."),
    ("h1", "Q7 Day-4 Design Challenge"),
    ("h2", "A Diagnose the bottleneck"),
    ("p", "The Q4 implementation repeats a distance calculation for every unordered pair. The count grows as n(n-1)/2: it rises from 4,950 at 100 points to 1,999,000 at 2,000 points. Most of the work is comparing pairs that cannot be closest."),
    ("h2", "B State the design objective"),
    ("p", "Keep the same closest-pair answer on the same points while reducing distance calculations. The comparison uses identical deterministic point sets and treats distance calculations as the primary measure."),
    ("h2", "C Revised design"),
    ("p", "The redesigned program sorts points by x and y once, divides the x-ordered list into halves, recursively finds the closest pair in each half, and checks a narrow strip around the split. Because the strip remains ordered by y, comparisons stop as soon as vertical separation is at least the best known distance. Duplicate coordinates are detected before recursion and return distance zero."),
    ("p", "The recurrence is T(n)=2T(n/2)+O(n): the two recursive halves contribute 2T(n/2), while partitioning and strip scanning contribute linear work per level. The solution is O(n log n) time with O(n) auxiliary space. Sorting has an upfront cost and the implementation uses additional lists and sets."),
    ("h2", "D Prediction before the final comparison run"),
    ("p", "The saved prediction expected equal minimum distances, an exact n(n-1)/2 count for brute force, and increasing distance-count reductions from divide-and-conquer as n grows. The prediction file was saved before regenerating the final comparison CSV; earlier exploratory runs were used to debug the implementation."),
    ("table", ["n", "Brute distances", "D&C distances", "Reduction", "Same distance", "Brute seconds", "D&C seconds"], q7_table),
    ("image", "Supporting_Files/results/q4_q7_distance_calculations.png", "Figure 4. Closest-pair distance calculation counts on identical inputs."),
    ("h2", "E Validate the redesign"),
    ("p", f"All five listed point-set sizes return the same minimum distance. At n=2,000 the redesign makes {int(q7[-1]['dc_distance_calculations']):,} distance calculations instead of {int(q7[-1]['brute_distance_calculations']):,}, a {float(q7[-1]['distance_calculation_reduction_percent']):.2f} percent reduction. It also lowers the measured runtime from about {float(q7[-1]['brute_seconds']):.3f} seconds to about {float(q7[-1]['dc_seconds']):.3f} seconds on this machine. The test harness compares the redesign with the brute-force baseline for 40 random point sets and checks duplicate coordinates."),
    ("h2", "F Defend the design"),
    ("p", "The operation-count prediction was supported for these datasets. The redesign adds sorting, recursion, temporary lists, and more code, so brute force remains a clear choice for very small inputs and as a simple correctness reference. The reported timing advantage is environment-specific; the distance-count reduction is the stronger evidence."),
    ("h1", "Complexity Summary"),
    ("table", ["Question", "Best time", "Average / expected", "Worst time", "Extra space"], [
        ["Q1 Selection", "Theta(n^2)", "Theta(n^2)", "Theta(n^2)", "O(1)"],
        ["Q1 Bubble (early exit)", "Theta(n)", "Theta(n^2)", "Theta(n^2)", "O(1)"],
        ["Q1 Insertion", "Theta(n)", "Theta(n^2)", "Theta(n^2)", "O(1)"],
        ["Q2 Sequential Search", "Theta(1)", "Theta(n)", "Theta(n)", "O(1)"],
        ["Q3 Brute String Match", "O(n) for easy mismatches", "Data dependent", "O(nm)", "O(1) + output"],
        ["Q4 Brute Closest Pair", "Theta(n^2)", "Theta(n^2)", "Theta(n^2)", "O(1)"],
        ["Q5 Brute Hull", "Data dependent", "Data dependent", "O(n^3)", "O(n+h)"],
        ["Q6 Exhaustive Knapsack", "Theta(n 2^n)", "Theta(n 2^n)", "Theta(n 2^n)", "O(n) output"],
        ["Q7 Closest Pair D&C", "Theta(n log n)", "Theta(n log n)", "Theta(n log n)", "O(n)"],
    ]),
    ("h1", "Conclusion"),
    ("p", "Among the required sorting methods, Insertion Sort best fits a small arrival batch on a mostly ordered list. Sequential Search is defensible only for small or infrequently searched lists. Brute-force string matching is simple but sensitive to repeated prefix matches. The convex-hull and exhaustive-search implementations make their geometric and combinatorial work visible, but their cubic and exponential growth limit scale. The closest-pair comparison demonstrates a measured reason to redesign an all-pairs scan when the input grows."),
    ("h1", "Test and Output Evidence"),
    ("p", "The included test harness ran ten checks successfully: sorting equivalence, sequential-search positions and misses, string overlaps and edge cases, closest-pair baseline, convex-hull examples and randomized reference comparison, the knapsack optimum, randomized closest-pair equivalence, duplicate-coordinate handling, and empty/single-point closest-pair inputs."),
]

def build_markdown():
    lines = []
    for block in sections:
        kind = block[0]
        if kind == "h1":
            lines.append("# " + block[1])
        elif kind == "h2":
            lines.append("## " + block[1])
        elif kind == "p":
            lines.append(block[1])
        elif kind == "table":
            lines.append(table_md(block[1], block[2]))
        elif kind == "image":
            lines.append(f"![{block[2]}](../{block[1]})")
        lines.append("")
    lines.extend([
        "## Execution evidence",
        "",
        "The seven output images below are rendered from the saved actual program transcripts. The corresponding RUN_OUTPUT.txt files are stored beside each image.",
        "",
    ])
    for i, (folder, _) in enumerate([
        ("Q1_Sorting_Algorithms", ""),
        ("Q2_Sequential_Search", ""),
        ("Q3_Brute_Force_String_Matching", ""),
        ("Q4_Brute_Force_Closest_Pair", ""),
        ("Q5_Brute_Force_Convex_Hull", ""),
        ("Q6_Exhaustive_Search", ""),
        ("Q7_Day4_Design_Challenge", ""),
    ], 1):
        lines.append(f"![Q{i} saved output](../{folder}/Output_Screenshots/output_capture.png)")
        lines.append("")
    (FINAL / "CO2_Assignment_Report.md").write_text("\n".join(lines), encoding="utf-8")


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    tc_pr.append(shading)


def set_cell_margins(cell, top=100, start=100, bottom=100, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def add_page_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for item in (begin, instruction, separate, text, end):
        run._r.append(item)


def add_docx_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.autofit = True
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for idx, value in enumerate(headers):
        cell = table.rows[0].cells[idx]
        cell.text = str(value)
        shade_cell(cell, "1F4E78")
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            cells[idx].text = str(value)
            set_cell_margins(cells[idx])
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cells[idx].paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.size = Pt(8.5)
    doc.add_paragraph()
    return table


def build_docx():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.72)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    for style_name, size, color in (("Heading 1", 16, "1F4E78"),
                                    ("Heading 2", 12.5, "365F91")):
        style = doc.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before = Pt(14)
        style.paragraph_format.space_after = Pt(5)

    header = section.header.paragraphs[0]
    header.text = "CSA06  |  CO2 Brute Force and Exhaustive Search"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        run.font.name = "Arial"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(100, 116, 139)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("CO2 Assignment Report  |  Page ")
    add_page_field(footer)
    for run in footer.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(100, 116, 139)

    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(110)
    run = p.add_run("CO2 Assignment Report")
    run.font.name = "Arial"
    run.font.size = Pt(25)
    run.font.bold = True
    run.font.color.rgb = RGBColor(31, 78, 121)
    for line in (
        "Brute Force and Exhaustive Search",
        "CSA06 Design and Analysis of Algorithms",
        "Course Outcome 2",
        "",
        "Student: Hitesh C",
        "Register number: 192524005",
        "Assignment type: Individual",
        f"Report date: {date(2026, 11, 15).strftime('%d %B %Y')}",
    ):
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(8)
        r = para.add_run(line)
        r.font.name = "Arial"
        r.font.size = Pt(12 if line else 6)
        if line == "Brute Force and Exhaustive Search":
            r.bold = True
            r.font.size = Pt(15)
    doc.add_page_break()

    for block in sections:
        kind = block[0]
        if kind == "h1":
            if block[1] == "Complexity Summary":
                doc.add_page_break()
            doc.add_heading(block[1], level=1)
        elif kind == "h2":
            doc.add_heading(block[1], level=2)
        elif kind == "p":
            doc.add_paragraph(block[1])
        elif kind == "table":
            add_docx_table(doc, block[1], block[2])
        elif kind == "image":
            path = ROOT / block[1]
            if path.exists():
                picture = doc.add_picture(str(path), width=Inches(6.45))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                caption = doc.add_paragraph(block[2])
                caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in caption.runs:
                    run.italic = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(75, 85, 99)

    doc.add_page_break()
    doc.add_heading("Execution evidence", level=1)
    doc.add_paragraph(
        "These images are rendered from the saved program output transcripts. "
        "Each corresponding RUN_OUTPUT.txt file is included beside its image."
    )
    for i, folder in enumerate([
        "Q1_Sorting_Algorithms",
        "Q2_Sequential_Search",
        "Q3_Brute_Force_String_Matching",
        "Q4_Brute_Force_Closest_Pair",
        "Q5_Brute_Force_Convex_Hull",
        "Q6_Exhaustive_Search",
        "Q7_Day4_Design_Challenge",
    ], 1):
        image_path = ROOT / folder / "Output_Screenshots" / "output_capture.png"
        if image_path.exists():
            doc.add_picture(str(image_path), width=Inches(6.35))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    output = FINAL / "CO2_Assignment_Report.docx"
    doc.save(output)
    return output


if __name__ == "__main__":
    build_markdown()
    path = build_docx()
    print(f"Built {path}")
