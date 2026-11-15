# Q7 Prediction for Final Comparison Run

This prediction was written before the final comparison run included in the report. Earlier exploratory runs were used during implementation debugging; the reported CSV is regenerated after this prediction was saved.

## Prediction

For the same point set, the divide-and-conquer implementation should return the same minimum distance as the brute-force baseline. The brute-force distance count should equal n(n-1)/2. The divide-and-conquer method should calculate substantially fewer distances as n increases because it compares only small recursive bases and nearby points in the split strip. The reduction should grow with input size. Pre-sorting and recursive list handling may make the redesigned method less attractive for very small n, but at the tested sizes it should use fewer distance calculations and lower runtime.

## Measures to record

- Distance calculations on identical deterministic point sets.
- Returned minimum distances and whether they agree.
- Local elapsed time as secondary evidence.

The final experiment script is Supporting_Files/run_experiments.py. Its results are saved in Supporting_Files/results/q7_redesign_comparison.csv.
