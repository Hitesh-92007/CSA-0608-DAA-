# Q4 - Brute-Force Closest Pair Pseudocode

    BRUTE-FORCE-CLOSEST-PAIR(points)
      if fewer than two points, return NOT-DEFINED
      best_pair = first two points
      for i from 0 through n-2
        for j from i+1 through n-1
          calculate squared Euclidean distance
          if it is smaller than the best distance, save this pair
      calculate one square root for the final reported distance
      return the pair and distance

The loops use j > i, so each unordered pair is visited once. The exact number is n(n-1)/2.
