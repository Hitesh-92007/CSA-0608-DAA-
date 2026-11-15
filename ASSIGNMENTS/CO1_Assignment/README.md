# CO1 Assignment 1 — Student Record Search

This project compares three ways to find a student record by its unique registration number for CSA06 Design and Analysis of Algorithms. It contains the 12 task responses, the implemented and benchmarked algorithms, mathematical analysis, experimental evidence, and the Day-4 design challenge.

## Algorithms

1. Iterative linear search over unsorted records.
2. Recursive binary search over records sorted by registration number.
3. Hash-table lookup using a registration-number index.

## Run the implementation

Use Python 3.10 or newer; only the standard library is required. From the repository root:

```bash
python CO1_Assignment/Task_8_Implementation_Testing/Source_Code/student_record_search.py
```

The default benchmark uses 1,000, 10,000, 100,000, and 1,000,000 records, 32 queries per size, a 50% hit rate, and three timing repetitions. It checks results and edge cases and saves the CSV to `CO1_Assignment/Report/Tables_and_Graphs/benchmark_results.csv`.

## Repository structure

```text
CO1_Assignment/
├── Task_1_Algorithm_Design/README.md
├── Task_2_Basic_Operation/README.md
├── Task_3_Mathematical_Complexity/README.md
├── Task_4_Case_Analysis/README.md
├── Task_5_Asymptotic_Analysis/README.md
├── Task_6_Recurrence_Formulation/README.md
├── Task_7_Recurrence_Solution/README.md
├── Task_8_Implementation_Testing/
│   ├── README.md
│   └── Source_Code/student_record_search.py
├── Task_9_Experimental_Performance/README.md
├── Task_10_Theory_vs_Experiment/README.md
├── Task_11_Final_Recommendation/README.md
├── Task_12_Design_Challenge/README.md
├── Report/
│   ├── Source_Code_Screenshots/source_code_algorithms.png
│   ├── Output_Screenshots/benchmark_output.png and benchmark_output.txt
│   ├── Analysis/Analysis_Summary.md
│   ├── Tables_and_Graphs/benchmark_results.csv and comparison_chart.png
│   └── Documentation/CO1_Assignment_Report.md
└── README.md
```

The [full report](Report/Documentation/CO1_Assignment_Report.md) consolidates all task explanations, derivations, results, limitations, and evidence. Each task folder also contains its corresponding answer. Timing varies by computer; the benchmark assumptions and operation counts are included for interpretation.
