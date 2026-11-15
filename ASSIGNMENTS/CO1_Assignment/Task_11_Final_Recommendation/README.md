## 12. Task 11 — Final design recommendation

For exact registration-number queries, use a hash-based index as the primary lookup path. It has expected constant-time lookup after an expected linear-time build and was the fastest search in the measured batches. At one million records, the hash batch took 0.007 ms for 32 queries in this run, compared with 0.229 ms for recursive binary search and 1,224.754 ms for linear search.

The trade-offs are `Θ(n)` extra space and reliance on expected hash behavior. Binary search is a useful alternative when keys must remain ordered for range queries or ordered traversal; linear search needs no index but is unsuitable for frequent large-scale lookups. A production database should maintain an indexed registration-number column rather than loading a million Python objects into a single process.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
