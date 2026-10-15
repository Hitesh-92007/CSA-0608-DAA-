## 6. Task 5 — Asymptotic comparison

| Algorithm phase | Best / expected growth | Worst growth | Effect as the dataset grows |
|---|---|---|---|
| Linear lookup | Best `Ω(1)`; expected `Θ(n)` for general positions | `O(n)` | Increasing records by 10× can increase a full scan by about 10×. |
| Binary lookup after sorting | Best `Ω(1)`; average `Θ(log n)` | `O(log n)` | A 10× increase adds only about `log2(10) ≈ 3.32` search levels. Sorting remains `Θ(n log n)`. |
| Hash lookup | Expected `Θ(1)` per lookup; expected build `Θ(n)` | `O(n)` per lookup in a collision-heavy worst case | Expected lookup work stays nearly flat as records grow; the index and its build work grow linearly. |

The following values show the expected comparison count for the 50/50 linear-search workload, an upper bound on primitive binary key comparisons, and one logical hash lookup per request:

| `n` | Linear expected comparisons/query `(3n+1)/4` | Binary upper bound `2(floor(log2 n)+1)` | Hash logical lookups/query (expected) |
|---:|---:|---:|---:|
| 1,000 | 750 | 20 | 1 |
| 10,000 | 7,500 | 28 | 1 |
| 100,000 | 75,000 | 34 | 1 |
| 1,000,000 | 750,000 | 40 | 1 |

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
