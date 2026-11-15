# Q6 pseudocode

## Median of Medians for the k-th smallest

```text
SELECT(A, k)
    if |A| <= 5: sort A and return A[k]
    split A into groups of at most 5; sort each group
    medians = the middle item of each group
    pivot = SELECT(medians, floor(|medians| / 2))
    divide A into items below, equal to, and above pivot
    recurse only into the partition containing rank k
    otherwise return pivot
```

Groups of five ensure a constant fraction of items are discarded at every partition. The recurrence is `T(n) <= T(n/5) + T(7n/10 + O(1)) + O(n)`, so worst-case time is `O(n)` and auxiliary storage is `O(n)` in this list-based version. QuickSelect is expected `O(n)` with random pivots but worst-case `O(n^2)`; a fixed first pivot is quadratic on sorted input when the target is central.

## Meet-in-the-Middle Subset Sum

```text
MITM-SUBSET-SUM(A, target)
    split A into L and R
    enumerate (sum, mask) for every subset of L
    enumerate (sum, mask) for every subset of R and sort by sum
    for each (leftSum, leftMask):
        binary-search R for target - leftSum
        if found: combine masks and return chosen elements
    return NOT-FOUND
```

Each half has about `2^(n/2)` subsets. Sorting and binary search give `O(n*2^(n/2))` time and `O(2^(n/2))` memory. Full enumeration is `O(n*2^n)` time and `O(n)` streaming memory. Meet-in-the-Middle trades memory for a much smaller search space and is unsuitable when half-subset storage is too large.
