# Q1 pseudocode

## Divide-and-conquer maximum and minimum

```text
MAXMIN(A, low, high)
    if low = high: return (A[low], A[low])
    if high = low + 1:
        compare A[low] and A[high] once
        return (smaller, larger)
    mid = floor((low + high) / 2)
    (minL, maxL) = MAXMIN(A, low, mid)
    (minR, maxR) = MAXMIN(A, mid + 1, high)
    return (min(minL, minR), max(maxL, maxR))
```

The combine step uses two comparisons. The recurrence for a power-of-two input is `T(n) = 2T(n/2) + 2`, with `T(2) = 1`, giving `3n/2 - 2` comparisons. Two independent scans use `2n - 2` comparisons.

## Binary Search

```text
BINARY-SEARCH(A, target)
    low = 0; high = length(A) - 1
    while low <= high:
        mid = floor((low + high) / 2)
        if A[mid] = target: return mid
        if A[mid] < target: low = mid + 1
        else: high = mid - 1
    return NOT-FOUND
```

The sorted-order invariant permits discarding the half that cannot contain the target. `T(n) = T(n/2) + O(1) = O(log n)`; iterative auxiliary space is `O(1)`.
