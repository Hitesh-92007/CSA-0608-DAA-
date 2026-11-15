# Final design summary

| Module | Final algorithm | Time | Extra memory | Selection reason |
|---|---|---|---|---|
| Nightly orders | Stable Merge Sort, with external merge for data larger than RAM | `O(n log n)` | `O(n)` RAM buffers or disk runs | Predictable performance and stable timestamp ties |
| Live leaderboard | Median-of-three guarded Quick Sort with Hoare partition and heapsort fallback | `O(n log n)` worst case | `O(log n)` internal stack; copy API uses `O(n)` | Avoids first-pivot degeneration while retaining the requested Quick Sort design |
| Order lookup | Lower-bound Binary Search | `O(log n)` | `O(1)` | Returns the first duplicate timestamp in the sorted snapshot |
| Recommendation scores | Strassen recursion with classical cutoff 64 as a measured candidate | `O(n^2.807)` above the cutoff | `O(n^2)` peak temporary matrices | Reduces 1,024-square scalar multiplication count by 41.38% versus cubic multiplication |

The complete rationale, recurrences, sample traces, production arithmetic, test results, experimental tables, charts, and evidence are in [`CO3_Final_Report.md`](CO3_Final_Report.md). For the live service, replace full sorting with an incremental ranking index if score updates become sparse enough to justify maintaining one. For matrix multiplication, measure the cutoff on production hardware and use conventional or BLAS multiplication if it is faster or more numerically suitable.
