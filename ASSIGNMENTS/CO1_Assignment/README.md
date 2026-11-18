# CO1 Assignment 1 — Student Record Search

This assignment compares ways to find student records by registration number for CSA06 Design and Analysis of Algorithms. It contains the 12 task responses, implementation, mathematical analysis, benchmark evidence, and the Day-4 design challenge.

## Final report

- [Complete report (PDF)](Report/CO1_Assignment_Report.pdf)
- [Complete report (Word)](Report/CO1_Assignment_Report.docx)

The **Report** folder contains only these two final report files. The earlier Markdown report, screenshots, chart, CSV, and logs are preserved under `Supporting_Files/Report_Source/Legacy_Report/`.

## Algorithms

1. Iterative linear search over unsorted records.
2. Recursive binary search over records sorted by registration number.
3. Hash-table lookup using a registration-number index.

## Run the implementation

Use Python 3.10 or newer; only the standard library is required. From the repository root:

```bash
python ASSIGNMENTS/CO1_Assignment/Task_8_Implementation_Testing/Source_Code/student_record_search.py
```

The default benchmark uses 1,000, 10,000, 100,000, and 1,000,000 records, 32 queries per size, a 50% hit rate, and three timing repetitions. It checks results and edge cases and saves the CSV to `ASSIGNMENTS/CO1_Assignment/Supporting_Files/Experiment_Results/benchmark_results.csv`.

## Repository structure

- `Task_1_...` through `Task_12_...`: task explanations and implementation.
- `Report/`: final Word and PDF reports only.
- `Supporting_Files/Experiment_Results/`: CSV created by a new benchmark run.
- `Supporting_Files/Report_Source/Legacy_Report/`: previous report source and evidence files.

Timing varies by computer. The report records the benchmark assumptions, operation counts, limitations, and measured results.
