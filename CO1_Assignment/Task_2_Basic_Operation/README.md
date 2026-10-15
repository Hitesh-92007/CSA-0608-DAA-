## 3. Task 2 — Basic operation

| Algorithm | Basic operation | Where it occurs and why it dominates |
|---|---|---|
| Linear search | Compare a record's registration number with the target | Once for each inspected record. The count grows with how far the target is in the list, or to all `n` records if absent. |
| Recursive binary search | Compare the target key with the middle record's key | At each recursive level, the comparison determines whether the target was found or which half remains. The remaining input is approximately halved at each call. |
| Hash-table lookup | Hash-table lookup (`dict.get`) | One logical lookup is issued per request. Its expected cost is constant under a well-distributed hash; internal probes are implementation details and are not exposed by Python's dictionary API. |

The comparison counts for linear and binary search are key comparisons. Hash lookup counts are reported separately as logical dictionary lookups, not as if they were string comparisons.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
