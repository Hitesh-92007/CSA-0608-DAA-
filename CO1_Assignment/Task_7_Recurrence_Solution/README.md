## 8. Task 7 — Recurrence solution

Using iteration and ignoring floor effects for the growth-rate derivation:

```text
T(n) = T(n/2) + c
     = T(n/4) + 2c
     = T(n/8) + 3c
     = T(n/2^k) + kc
```

The recursion reaches a base case when `n/2^k ≤ 1`, so `k ≈ log2 n`. Therefore `T(n) = Θ(log n)`. The Master Theorem gives the same result: `a=1`, `b=2`, and `f(n)=Θ(1)`; since `n^(log_b a)=1`, the equal-growth case yields `Θ(log n)`. The method applies because there is one half-sized recursive subproblem and constant work at each level.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
