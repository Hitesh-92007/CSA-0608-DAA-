## 5. Task 4 — Best, average, and worst cases

| Algorithm | Best case | Average case under stated assumptions | Worst case |
|---|---|---|---|
| Linear | Target is first: 1 comparison, `Θ(1)` | Successful uniform target: `(n+1)/2`; mixed present/absent: `(3n+1)/4`; both `Θ(n)` | Target last or absent: `n`, `Θ(n)` |
| Recursive binary | Target is at the first middle: 1 equality comparison, `Θ(1)` | Search follows about half the remaining range per level: `Θ(log n)` | Target absent or reached at the deepest level: at most `floor(log2 n)+1` inspected midpoints; at most twice that many primitive key comparisons, `Θ(log n)` |
| Hash table | Key resolves immediately with no collision: expected `Θ(1)` | Expected `Θ(1)` lookup with a well-distributed hash | Severe collisions can require `Θ(n)` work |

Linear search varies because it stops as soon as it finds the key. Binary search reduces the candidate range at every call, so even a miss follows only a logarithmic number of levels. Hashing usually addresses the bucket directly, but collisions explain its linear worst case.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
