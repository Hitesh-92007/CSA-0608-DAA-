# Q6 - Exhaustive Search Pseudocode

    EXHAUSTIVE-KNAPSACK(packages, capacity)
      best_value = 0; best_subset = empty
      for mask from 0 through 2^n - 1
        weight = 0; value = 0; subset = empty
        for each package i
          if bit i of mask is set
            add its weight and value; append it to subset
        if weight <= capacity and value improves the best
          save subset, weight, and value
      return best subset

Every subset, including the empty subset, is checked. There are exactly 2^n candidate subsets; the straightforward implementation inspects up to n package bits for each candidate.
