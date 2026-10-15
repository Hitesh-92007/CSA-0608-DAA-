# Task 8 — Implementation and testing

The implementation is in [Source_Code/student_record_search.py](Source_Code/student_record_search.py). It contains all three algorithms, generates reproducible synthetic records, tests 1,000, 10,000, 100,000, and 1,000,000 records, and checks both successful and unsuccessful lookups.

From the repository root, run:

```bash
python CO1_Assignment/Task_8_Implementation_Testing/Source_Code/student_record_search.py
```

The program tests the same query set against each algorithm, checks present and absent keys, and includes first-position, last-position, and missing-key edge cases. Sorting and hash-index construction are timed separately from searches. The default run writes its measurements to `CO1_Assignment/Report/Tables_and_Graphs/benchmark_results.csv`.

See [the complete report](../Report/Documentation/CO1_Assignment_Report.md#task-8-implementation-and-test-procedure) for the test procedure, assumptions, and output evidence.
