# Q7 pseudocode: Maximum Subarray Sum

```text
MAX-SUBARRAY(A, low, high)
    if low = high: return (A[low], low, high)
    mid = floor((low + high) / 2)
    left = MAX-SUBARRAY(A, low, mid)
    right = MAX-SUBARRAY(A, mid + 1, high)
    scan left from mid down to low to find best suffix
    scan right from mid + 1 up to high to find best prefix
    cross = bestSuffix + bestPrefix, with their boundary indices
    return the highest-sum of left, right, and cross
```

Each boundary scan is linear in the current interval, so `T(n)=2T(n/2)+Theta(n)=Theta(n log n)` with `Theta(log n)` recursion space. Ties are resolved by keeping the earliest start and then the earliest end.
