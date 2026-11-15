# Q3 - Brute-Force String Matching Pseudocode

    BRUTE-FORCE-MATCH(text, pattern)
      matches = empty list
      comparisons = 0
      if pattern is empty, return every boundary 0 through length(text)
      for shift from 0 through length(text)-length(pattern)
        j = 0
        while j < length(pattern)
          comparisons = comparisons + 1
          if text[shift+j] differs from pattern[j], stop this alignment
          j = j + 1
        if j equals length(pattern), append shift
      return (matches, comparisons)

The algorithm preserves overlapping matches because the next alignment starts one character later.
