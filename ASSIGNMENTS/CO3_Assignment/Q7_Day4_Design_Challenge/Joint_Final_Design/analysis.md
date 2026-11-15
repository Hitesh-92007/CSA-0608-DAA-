# Q7 joint design reference: Maximum Subarray Sum

**Problem:** Given a non-empty array of integers, return the contiguous segment with maximum sum.

## Decomposition and combine

Split the interval into left and right halves. A best segment lies wholly in the left half, wholly in the right half, or crosses the midpoint. Each recursive call returns the best sum and its start/end indices. The combine step scans once from the midpoint leftward for the best suffix and once rightward for the best prefix; their sum is the best crossing segment. Select the greatest of the three candidates.

## Base case and recurrence

A one-element interval returns that item. At each level two half-size subproblems are solved and the boundary scans take linear work: `T(n)=2T(n/2)+Theta(n)=Theta(n log n)`. Recursion space is `Theta(log n)`. A straightforward brute-force baseline checks all `n(n+1)/2` segments and uses `Theta(n^2)` time.

## Design comparison record

The supplied question requires the two students to compare their independently written proposals before producing a joint design. Record actual agreements, differences, retained ideas, and revisions after that discussion here. Do not fill this as a historical discussion record until it has happened.

- Agreement:
- Differences:
- Ideas retained and why:
- Change made to the final design:
- Names and date of discussion:
