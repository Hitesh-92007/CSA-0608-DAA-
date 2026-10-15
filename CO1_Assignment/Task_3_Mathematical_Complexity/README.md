## 4. Task 3 — Mathematical time-complexity derivations

Let `n` be the number of records and `q` the number of search requests.

### Linear search

If the target is at one-based position `k`, the search performs `C(n) = k` equality comparisons. If the target is absent, it performs `C(n) = n`. A successful target uniformly distributed among the records has average count:

```text
E[C | present] = (1 + 2 + ... + n) / n
              = n(n + 1) / (2n)
              = (n + 1) / 2
```

For a 50% present / 50% absent workload, the expected count is:

```text
E[C] = 0.5 × (n + 1)/2 + 0.5 × n = (3n + 1)/4
```

There is no algorithm-specific preprocessing. For `q` requests, the expected search work under this mix is `q(3n + 1)/4`, and the worst case is `qn`.

### Recursive binary search

At each call, binary search inspects the middle record and recurses into at most one subproblem of size approximately `n/2`. A nonmatching midpoint uses an equality comparison and an ordering comparison; this is still constant work per call. The recurrence is:

```text
T(n) = T(floor(n / 2)) + c,  n > 1
T(0) = c0; T(1) = c1
```

The recursive search is `Θ(log n)`. Because the input must be sorted first, sorting costs `Θ(n log n)` time and `Θ(n)` additional space for the sorted list. For `q` requests against that sorted list, total work is `Θ(n log n + q log n)`. If the sorted index is retained across requests, the sorting cost is paid once per rebuild, not once per query.

### Hash-table lookup

Building the index inserts each of the `n` records once. With expected constant-time insertion, the expected build cost is `Θ(n)`. Each exact-key request has expected `Θ(1)` lookup cost, so the expected total for building the index and serving `q` requests is:

```text
T(n, q) = Θ(n) + q × Θ(1) = Θ(n + q)   (expected)
```

The index uses `Θ(n)` additional space. If keys collide pathologically, lookup can degrade to `Θ(n)` in the worst case; the expected result relies on a suitable hash distribution and implementation behavior.

See the [complete assignment report](../Report/Documentation/CO1_Assignment_Report.md) for the full analysis and evidence.
