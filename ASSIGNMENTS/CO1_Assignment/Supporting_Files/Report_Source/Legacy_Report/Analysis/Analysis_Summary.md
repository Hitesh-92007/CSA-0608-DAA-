# Analysis summary

The complete derivations and discussion are in [the assignment report](../Documentation/CO1_Assignment_Report.md).

## Main result

- Iterative linear search grows with the number of records and has no preprocessing requirement.
- Recursive binary search needs sorted records (`Θ(n log n)` sorting) and then searches in `Θ(log n)` time.
- A hash index takes expected `Θ(n)` to build, expected `Θ(1)` per exact-key lookup, and `Θ(n)` additional space.
- The benchmark shows the hash lookup as the fastest repeated-query path for every tested size. Search timing is hardware-dependent; counts and growth trends are the more portable evidence.
- For the Day-4 workload, keep a registration-number hash index available and apply daily additions incrementally or rebuild once per daily batch.

The benchmark assumptions, complete mathematical analysis, tables, and limitations are documented in the report.
