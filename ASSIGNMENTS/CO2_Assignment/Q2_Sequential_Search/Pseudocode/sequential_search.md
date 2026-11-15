# Q2 - Sequential Search Pseudocode

    SEQUENTIAL-SEARCH(records, target_id)
      comparisons = 0
      for each record at index i, from first to last
        comparisons = comparisons + 1
        if record.tool_id equals target_id
          return (i, comparisons)
      return (NOT-FOUND, comparisons)

The search checks the live list directly, so it needs no sorting or index build. A hit at position k takes k+1 comparisons; a miss examines every record.
