"""Assemble the final Markdown report from the debugging log and evidence links."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = Path(__file__).resolve().parent
debug_log = (REPORT / "Debugging_Log.md").read_text(encoding="utf-8")
debug_log = debug_log.replace("# Debugging log", "## Detailed findings", 1)

header = """# SentinelOps SOC Alert Triage Debugging and Optimisation Report

**Student:** Hitesh C  
**Register number:** 192524005  
**Course:** CSA06 - Design and Analysis of Algorithms  
**Assessment:** CO2 Debugging and Optimisation Task

This report records the defects in the supplied alert-triage code, the minimal corrections, the optimized algorithms, test results, complexity analysis, and measured comparisons. The original, corrected, and optimized Python programs are included in `Source_Code/`.

## Debugging, optimisation, analysis, and delivery

"""

appendices = """\
## Appendix A: Experimental charts

![Closest-pair pair-distance evaluations](../Supporting_Files/distance_evaluations.png)

![Insertion-sort comparisons by input order](../Supporting_Files/insertion_sort_comparisons.png)

## Appendix B: Source and output evidence captures

These are captures of source files and saved run logs displayed in Notepad. The complete source and text logs are included in the task folders. The output logs came from actual Python runs in this workspace; the images are not live terminal screenshots.

![Original source code, first section](../Supporting_Files/evidence/original_source_top.jpg)

![Original source code, closest-pair section](../Supporting_Files/evidence/original_source_bottom.jpg)

![Optimized implementation, first section](../Supporting_Files/evidence/optimized_source.jpg)

![Optimized closest-pair implementation](../Supporting_Files/evidence/optimized_closest_source.jpg)

![Original program output](../Supporting_Files/evidence/original_output.jpg)

![Corrected and optimized test output](../Supporting_Files/evidence/test_output.jpg)

![Experiment output](../Supporting_Files/evidence/experiment_output.jpg)
"""

content = header + debug_log + "\n\n" + appendices
(REPORT / "Report.md").write_text(content, encoding="utf-8")
print(REPORT / "Report.md")
