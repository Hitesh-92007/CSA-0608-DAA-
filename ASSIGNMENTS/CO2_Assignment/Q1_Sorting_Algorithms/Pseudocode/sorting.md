# Q1 - Sorting Pseudocode

## Selection Sort

    SELECTION-SORT(A)
      for i from 0 to length(A)-2
        smallest = i
        for j from i+1 to length(A)-1
          count one comparison
          if A[j] < A[smallest], smallest = j
        if smallest != i
          swap A[i] and A[smallest]
      return A

## Bubble Sort with early exit

    BUBBLE-SORT(A)
      for end from length(A)-1 down to 1
        swapped = false
        for j from 0 to end-1
          count one comparison
          if A[j] > A[j+1]
            swap the adjacent values
            swapped = true
        if not swapped, stop
      return A

## Insertion Sort

    INSERTION-SORT(A)
      for i from 1 to length(A)-1
        key = A[i]
        j = i-1
        while j >= 0 and A[j] > key
          count the key comparison
          move A[j] one place right
          j = j-1
        if j >= 0, count the final failed key comparison
        put key at A[j+1]
      return A

Each algorithm returns comparison, swap, and/or movement counts alongside the sorted values.
