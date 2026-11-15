# Q5 pseudocode

```text
CLOSEST-PAIR(Px, Py)
    if |Px| <= 3: check all pairs and return the best squared distance
    split Px at its median x-coordinate into Lx and Rx
    partition Py by point identity into Ly and Ry
    (dL, pairL) = CLOSEST-PAIR(Lx, Ly)
    (dR, pairR) = CLOSEST-PAIR(Rx, Ry)
    d = min(dL, dR); best = corresponding pair
    build strip of Py points whose squared x-distance from split line < d
    for each strip point, check at most the next 7 y-ordered points
        stop early when squared y-gap >= d
        update d and best pair
    return (d, best)
```

Sort once in `O(n log n)`, then partition and scan in `O(n)` per recursion level: `T(n)=2T(n/2)+O(n)=O(n log n)`. Brute force requires `n(n-1)/2` distance calculations and `O(n^2)` time. The seven-neighbor bound follows from packing points into the two half-strips under the current distance. The reference Python version uses copied lists and identity sets; this simple implementation can use `O(n log n)` temporary storage. A buffer-reuse implementation can reduce auxiliary storage to `O(n)`.
