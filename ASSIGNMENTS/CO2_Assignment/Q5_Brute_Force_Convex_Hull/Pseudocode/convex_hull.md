# Q5 - Brute-Force Convex Hull Pseudocode

    BRUTE-FORCE-HULL(points)
      remove duplicate coordinates
      for each unordered candidate pair (a,b)
        positive = false; negative = false
        examine every other point p
        compute cross((b-a),(p-a))
        if cross is positive, positive = true
        if cross is negative, negative = true
        if both flags become true, stop: (a,b) is not a supporting edge
        if all points are on one side or on the line
          reject the pair if a collinear point lies outside segment [a,b]
          otherwise add (a,b) to the hull-edge graph
      walk the edge graph from the lexicographically smallest coordinate
      return the ordered extreme boundary vertices

Orientation is determined by the sign of a 2D cross product. The outside-segment check removes interior points from collinear edges, including in the all-collinear case.
