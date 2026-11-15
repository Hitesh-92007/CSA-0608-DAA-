# Module 3 pseudocode: first matching timestamp

```text
FIRST-ORDER-AT-TIMESTAMP(A, target)
    low = 0
    high = length(A)                  // half-open interval [low, high)
    while low < high
        middle = low + floor((high - low) / 2)
        if A[middle].timestamp < target
            low = middle + 1
        else
            high = middle             // retain possible first match
    if low < length(A) and A[low].timestamp = target
        return low
    return NOT-FOUND
```

The input must be sorted by timestamp. Moving `high` to `middle` on equality finds the lower bound, so duplicate timestamps return the earliest consolidated order.
