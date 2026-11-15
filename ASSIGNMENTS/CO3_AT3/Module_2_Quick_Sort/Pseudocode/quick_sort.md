# Module 2 pseudocode: guarded Quick Sort

```text
INTRO-QUICK-SORT(A)
    depthLimit = 2 * floor(log2(length(A)))
    SORT-RANGE(A, 0, length(A), depthLimit)
    return A

SORT-RANGE(A, low, high, depthLimit)
    while high - low > INSERTION-CUTOFF
        if depthLimit = 0
            HEAP-SORT(A[low : high])
            return
        depthLimit = depthLimit - 1
        pivot = median(A[low], A[midpoint], A[high - 1])
        split = HOARE-PARTITION(A, low, high, pivot)
        recursively sort the smaller of:
            A[low : split]
            A[split : high]
        continue the loop on the larger part
    INSERTION-SORT(A[low : high])

HOARE-PARTITION(A, low, high, pivot)
    left = low; right = high - 1
    repeat
        advance left while A[left] < pivot
        move right left while pivot < A[right]
        if left >= right
            return right + 1
        swap A[left], A[right]
        left = left + 1; right = right - 1
```

The first-pivot Lomuto routine is also included as a baseline to reproduce the supplied issue and trace one partition. The production version uses median-of-three with Hoare partitioning, handles short ranges with insertion sort, and falls back to heapsort when partitions become too unbalanced. Hoare's scans also split equal scores across both sides rather than sending every duplicate into one recursive partition.
