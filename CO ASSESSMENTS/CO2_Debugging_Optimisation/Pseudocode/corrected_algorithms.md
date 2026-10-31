# Corrected algorithms

These pseudocode listings keep the original approaches and repair the logic errors. They are in the same order as the four functions in the question.

## 1. Stable insertion sort by descending severity

```text
FOR i from 1 to length(alerts) - 1
    key = alerts[i]
    j = i - 1
    WHILE j >= 0 AND alerts[j].severity < key.severity
        alerts[j + 1] = alerts[j]
        j = j - 1
    alerts[j + 1] = key
RETURN alerts
```

The strict `<` comparison leaves equal-severity alerts in their arrival order.

## 2. Sequential blocklist search

```text
FOR each address in blocklist
    IF address equals ip
        RETURN true
RETURN false
```

## 3. Brute-force signature matching

```text
n = length(log)
m = length(pattern)
hits = empty list
FOR start from 0 through n - m, inclusive
    matched = true
    FOR offset from 0 through m - 1
        IF log[start + offset] differs from pattern[offset]
            matched = false
            BREAK
    IF matched
        append start to hits
RETURN hits
```

An empty pattern is defined to match at every boundary from 0 through n.

## 4. Corrected brute-force closest pair

```text
IF fewer than two events
    RETURN no pair and infinity
best_distance = infinity
best_pair = none
FOR i from 0 through n - 1
    FOR j from 0 through n - 1
        IF i equals j
            CONTINUE
        distance = EuclideanDistance(events[i], events[j])
        candidate = the two indexes in ascending order
        IF distance is smaller, or ties and candidate is lexicographically earlier
            best_distance = distance
            best_pair = candidate
RETURN best_pair, best_distance
```

This intentionally retains the original all-ordered-pairs structure to make the correctness repair easy to follow. The optimized algorithm is in `optimized_algorithms.md`.
