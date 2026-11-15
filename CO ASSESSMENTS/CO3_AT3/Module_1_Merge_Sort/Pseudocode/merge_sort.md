# Module 1 pseudocode: stable merge sort

```text
MERGE-SORT(A)
    if length(A) <= 1
        return a copy of A
    middle = floor(length(A) / 2)
    left  = MERGE-SORT(A[0 : middle])
    right = MERGE-SORT(A[middle : length(A)])
    return MERGE(left, right)

MERGE(left, right)
    result = empty list
    i = 0; j = 0
    while i < length(left) and j < length(right)
        if left[i].timestamp <= right[j].timestamp
            append left[i] to result   // left wins ties: stable order
            i = i + 1
        else
            append right[j] to result
            j = j + 1
    append left[i : end] to result
    append right[j : end] to result
    return result
```

The split halves are contiguous ranges of the input. Since the left half contains earlier arrivals, selecting the left record when timestamps are equal preserves arrival order across every merge.
