# CO2 Assignment — Brute-Force and Exhaustive Search

This folder contains the seven-question individual assignment for CSA06 Design and Analysis of Algorithms, CO2. Each question has separate pseudocode, source code, and output evidence. The supporting folder contains the test data, benchmarks, charts, and test harness.

## Final report

- [Complete report (PDF)](Report/CO2_Assignment_Report.pdf)
- [Complete report (Word)](Report/CO2_Assignment_Report.docx)

The **Report** folder contains only these two final report files. The earlier report files and report-building scripts are preserved under `Supporting_Files/Report_Source/Previous_Final_Report/`.

## Questions

1. Selection, Bubble, and Insertion Sort under different input arrangements.
2. Sequential Search in a changing tool list.
3. Brute-Force String Matching under different text and pattern structures.
4. Brute-Force Closest Pair and its quadratic pair count.
5. A Brute-Force Convex Hull derived from the one-side geometric test.
6. Exhaustive Search for the payload-constrained package selection.
7. A measured redesign of Closest Pair using divide-and-conquer.

## Run

Use Python 3.10 or later; the algorithms use the standard library. From this folder:

```bash
python Supporting_Files/run_all.py
python Supporting_Files/test_harness.py
python Supporting_Files/run_experiments.py
```

The first command saves output logs and images in each question's `Output_Screenshots` folder. The experiment command writes CSV results and comparison graphs to `Supporting_Files/results/`.

## Evidence and limits

Operation counts are the main evidence. Timings are local measurements and can vary across computers. The output images are rendered from saved program transcripts; matching plain-text logs are included beside them. The supplied brief leaves the dataset range blank, so each question states its selected test sizes.

This is an individual assignment. Review the algorithms and measured outputs before submission; do not claim work or observations you have not personally checked.
