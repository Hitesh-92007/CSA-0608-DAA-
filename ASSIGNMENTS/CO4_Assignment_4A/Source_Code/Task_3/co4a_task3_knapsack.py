"""0/1 knapsack dynamic programming with item reconstruction."""
def solve_knapsack(items, capacity):
    n = len(items)
    if capacity < 0 or any(w < 0 or v < 0 for _,w,v in items): raise ValueError("Invalid capacity/item")
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i, (_,w,v) in enumerate(items, 1):
        for c in range(capacity+1):
            dp[i][c] = dp[i-1][c]
            if w <= c: dp[i][c] = max(dp[i][c], v + dp[i-1][c-w])
    chosen, c = [], capacity
    for i in range(n,0,-1):
        if dp[i][c] != dp[i-1][c]:
            name,w,v = items[i-1]; chosen.append(name); c -= w
    chosen.reverse()
    return dp[n][capacity], chosen, dp

def main():
    items=[("P",2,12),("Q",3,20),("R",4,25),("S",5,30)]
    value, chosen, dp=solve_knapsack(items,7)
    print("CO4A Task 3: 0/1 knapsack, capacity=7")
    print("DP optimum by item row:", [row[7] for row in dp])
    print("Selected items:", chosen); print("Maximum value:",value)
    assert value==45 and chosen==["Q","R"]
    assert solve_knapsack([("X",8,100)],7)[:2] == (0,[])
    print("Checks: passed (given instance, item heavier than capacity)")

if __name__ == "__main__": main()
