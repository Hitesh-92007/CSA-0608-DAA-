# CO1 Assessment Tool 1 — DAA

This folder contains the CO1 assignment for **CSA06: Design and Analysis of Algorithms**. It compares three ways to find a student by registration number and includes the mathematical analysis, reproducible benchmark, results, and evidence.

## Folder contents

```text
CO1_AT1/
├── README.md
└── Question_1/
    ├── Source_Code/
    │   └── student_record_search.py
    └── Report/
        ├── CO1_Assignment_Report.md
        ├── benchmark_results.csv
        └── evidence/
            ├── benchmark_output.png
            ├── benchmark_output.txt
            ├── comparison_chart.png
            └── source_code_algorithms.png
```

## Run the program

Use Python 3.10 or newer. The program uses only the Python standard library.

From the repository root:

```bash
python CO1_AT1/Question_1/Source_Code/student_record_search.py
```

The default run tests 1,000, 10,000, 100,000, and 1,000,000 records. It uses 32 queries per size, three timing repetitions, a fixed seed, and saves the measurements to `CO1_AT1/Question_1/Report/benchmark_results.csv`.

Options can be changed, for example:

```bash
python CO1_AT1/Question_1/Source_Code/student_record_search.py --sizes 1000 5000 --queries 20 --repeats 5
```

The query count must be even and at least 2. Benchmark times depend on the computer and Python version; see the report for the test assumptions and interpretation.
