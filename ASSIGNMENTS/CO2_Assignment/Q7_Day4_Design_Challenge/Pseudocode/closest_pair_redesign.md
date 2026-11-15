# Q7 - Closest-Pair Redesign Pseudocode

## Original bottleneck

The Q4 double loop computes every one of n(n-1)/2 distances. The redesigned objective is to reduce distance calculations while returning the same minimum distance.

## Divide-and-conquer design

    CLOSEST-PAIR-DC(points)
      sort points by x and by y once
      if duplicate coordinates exist, return a duplicate pair at distance zero
      RECURSE(points_x, points_y)

    RECURSE(Px, Py)
      if length(Px) <= 3
        compare every pair directly and return the best pair
      split Px at the middle x coordinate
      partition Py into left_y and right_y using point identifiers
      best_left = RECURSE(left_x, left_y)
      best_right = RECURSE(right_x, right_y)
      best = the better of the two results
      strip = points in Py whose squared x distance from the split is < best distance
      for each point in strip, compare following y-ordered points
        stop when squared y separation >= best distance
        update best for any closer cross-boundary pair
      return best

Pre-sorting avoids sorting at every recursive level. Each level partitions and scans linear-sized lists; the recurrence is T(n)=2T(n/2)+O(n), so expected time is O(n log n) and auxiliary space is O(n).
