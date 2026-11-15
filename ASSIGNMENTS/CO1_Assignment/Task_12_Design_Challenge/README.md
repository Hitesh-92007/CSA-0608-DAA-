## 13. Task 12 — Day-4 design challenge

### A. Impact analysis

The workload is now specified as 50,000 searches per hour against one million records, with additions only once per day. Search frequency is high relative to the update frequency: there are about 1.2 million lookups between daily update batches. This makes it worthwhile to build and retain an index. The original unsorted-data assumption still applies to linear search; binary search would require a sorted index and rebuild or insertion work when records change.

### B. Evaluate the original recommendation

The hash index remains suitable. In this benchmark, building it for one million records took 302.734 ms, and 32 lookups took 0.007 ms. These measurements are illustrative, not production guarantees. A dictionary lookup is expected `Θ(1)`, and the low daily update rate lets the system amortize index construction over many requests. Linear search would average about 750,000 key comparisons per request under a 50/50 hit/miss assumption; that is approximately 37.5 billion comparisons per hour. Binary search would require at most 40 primitive key comparisons per request (about 2 million per hour), plus sorting when rebuilding.

### C. Adaptation decision: retain and operationally modify

Retain the hash-based design and modify the update process: build the hash index at startup or during the daily batch, then insert each newly added record into the index. A single expected dictionary insertion is `Θ(1)`; a full rebuild is expected `Θ(n)`. Search remains expected `Θ(1)`. In a real database, use a persistent unique index on the registration-number column so the index survives restarts and supports concurrent requests.

### D. Evidence-based defence

The benchmark shows one logical hash lookup per query at all four sizes, while linear operations grow in proportion to the record count. Binary search also scales well, but needs sorted preprocessing and a logarithmic search. With 50,000 requests per hour and records added only once daily, keeping the hash index ready favors repeated lookups over minimizing occasional update work. The choice is therefore supported by the request/update ratio, expected complexity, and measured search results, while acknowledging the memory and worst-case collision trade-offs.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
