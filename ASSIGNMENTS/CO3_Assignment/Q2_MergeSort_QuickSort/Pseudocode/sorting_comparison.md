# Q2 pseudocode

## Merge Sort

```text
MERGE-SORT(A)
    if length(A) <= 1: return A
    split A into left and right halves
    L = MERGE-SORT(left); R = MERGE-SORT(right)
    merge L and R by repeatedly appending the smaller front item
    append either remainder; return merged sequence
```

Both halves are close to equal regardless of input order. `T(n)=2T(n/2)+Theta(n)=Theta(n log n)`; auxiliary storage is `Theta(n)`.

## Lomuto Quick Sort (last element pivot)

```text
QUICK-SORT(A, low, high)
    if low >= high: return
    pivot = A[high]; i = low
    for j = low to high - 1:
        if A[j] <= pivot: swap A[i], A[j]; i = i + 1
    swap A[i], A[high]
    QUICK-SORT(A, low, i - 1)
    QUICK-SORT(A, i + 1, high)
```

Balanced splits give `T(n)=2T(n/2)+Theta(n)=Theta(n log n)`. Sorted distinct input with the last pivot gives sizes `n-1` and `0`, hence `T(n)=T(n-1)+Theta(n)=Theta(n^2)` and linear recursion depth. Merge Sort has predictable height; Quick Sort's height depends on pivot quality. For unknown input, ask about size, order/duplicates, memory limits, stability requirements, and whether a robust worst-case bound matters.
