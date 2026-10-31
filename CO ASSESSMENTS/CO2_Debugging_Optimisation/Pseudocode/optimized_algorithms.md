# Optimized algorithms

## 1. Stable severity ordering

```text
stable_sort alerts by severity descending
write the sorted sequence back into the original list
RETURN alerts
```

Python's stable Timsort is used so equal severities retain input order.

## 2. Repeated blocklist lookups

```text
ONCE: index = hash set of every blocked address
FOR each query ip
    RETURN whether ip is in index
```

Build the set once and reuse it for the batch of queries.

## 3. Knuth-Morris-Pratt signature scan

```text
BUILD lps table for pattern
i = 0; j = 0
WHILE i < length(log)
    IF log[i] equals pattern[j]
        advance i and j
        IF j reaches pattern length
            record i - j
            set j = lps[j - 1] to preserve overlapping matches
    ELSE IF j > 0
        set j = lps[j - 1] without moving i backwards
    ELSE
        advance i
RETURN all recorded offsets
```

The LPS table reuses known prefix information, so the scan does not restart at each text position. Total character comparisons are O(n + m), not O(nm).

## 4. Divide-and-conquer closest pair

```text
IF fewer than two events
    RETURN no pair and infinity
IF duplicate coordinates exist
    RETURN earliest zero-distance index pair
SORT points by x and by y
SOLVE(px, py)
    IF at most three points
        check each unordered pair, comparing squared distance
    split points by x into left and right halves
    partition the y-sorted list by point identity
    recursively solve both halves
    keep the shorter pair and deterministic index tie-break
    make a y-sorted strip whose x-distance from the split is no greater than best
    for each strip point, compare only following points while y-distance squared
        is no greater than best, and only across opposite halves
        update with squared Euclidean distance
RETURN best pair and one square root of the best squared distance
```

This checks no self-pairs or repeated unordered pairs. The strip bounds discard pairs that cannot improve the best known distance.
