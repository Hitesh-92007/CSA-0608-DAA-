## 10. Task 9 — Experimental performance

Times below are milliseconds for a complete 32-query batch. Operation counts are mean dominant operations per request; for hashing, this means one dictionary lookup, not internal collision probes. The measured preprocessing columns are the sort time and the hash-index build time.

| Records | Linear search ms / operations per query | Binary sort ms / search ms / comparisons per query | Hash build ms / search ms / lookups per query |
|---:|---:|---:|---:|
| 1,000 | 0.844 / 730.188 | 0.210 / 0.070 / 17.125 | 0.084 / 0.006 / 1 |
| 10,000 | 12.221 / 7,339.688 | 2.831 / 0.164 / 24.562 | 1.018 / 0.012 / 1 |
| 100,000 | 103.784 / 77,613.125 | 43.023 / 0.183 / 31.250 | 13.422 / 0.009 / 1 |
| 1,000,000 | 1,224.754 / 828,876.562 | 643.896 / 0.229 / 37.312 | 302.734 / 0.007 / 1 |

All three methods returned correct results for all benchmark and edge-case queries.

![Measured operations and search time comparison](../Report/Tables_and_Graphs/comparison_chart.png)

**Source-code screenshot:**

![Screenshot of the three source-code implementations](../Report/Source_Code_Screenshots/source_code_algorithms.png)

**Benchmark output screenshot:**

![Screenshot of the benchmark output](../Report/Output_Screenshots/benchmark_output.png)

The raw data is in [`benchmark_results.csv`](../Report/Tables_and_Graphs/benchmark_results.csv), and the captured console output is in [`../Report/Output_Screenshots/benchmark_output.txt`](../Report/Output_Screenshots/benchmark_output.txt).

Raw measurements: [benchmark_results.csv](../Report/Tables_and_Graphs/benchmark_results.csv).


See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
