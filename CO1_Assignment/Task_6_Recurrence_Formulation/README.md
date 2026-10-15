## 7. Task 6 — Recurrence relation

For the recursive binary search, the original problem contains `n` sorted records. One recursive call is made after each unsuccessful midpoint check, and that call receives at most `floor(n/2)` records. The equality and ordering checks plus index arithmetic do constant work outside the recursive call. If `T(n)` counts time, the recurrence is:

```text
T(n) = T(floor(n / 2)) + c,  n > 1
T(1) = c1
T(0) = c0
```

The `n=0` base case represents the empty range reached after an unsuccessful search; `n=1` is the final possible record inspection. The recurrence follows the implementation's halving behavior rather than being assumed independently.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
