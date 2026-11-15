## 11. Task 10 — Theory versus experiment

The results follow the predicted growth. Linear-search operations increase from about 730 to about 828,877 per request as `n` increases from 1,000 to 1,000,000; this is linear growth. The observed 50/50 average is above the theoretical expectation of 750,000 at one million because only 16 successful positions were sampled in this run. Repeating with a different seed can change the sample average while preserving the linear trend.

Binary search grows slowly: the measured count rises from about 17 to 37 primitive key comparisons per request across three orders of magnitude. This remains within the logarithmic upper bound of 20 inspected midpoints, or at most 40 primitive key comparisons, at one million records. Search time also stays below 0.3 ms for all 32-query batches. The sort cost is visible separately and grows with `n`.

Hash lookup uses one logical dictionary lookup per request at every size, and its batch search time remains roughly flat in this run. At one million records, building the hash index took less time than sorting the records in this run; those constants depend on the machine and runtime. Both preprocessing steps are paid separately from each batch. Actual times vary with hardware, Python implementation, memory pressure, and runtime state, so operation counts and asymptotic trends are more portable than the milliseconds.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
