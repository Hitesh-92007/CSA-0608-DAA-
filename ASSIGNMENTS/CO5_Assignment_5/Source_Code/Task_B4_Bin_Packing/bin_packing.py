"""Next Fit bin-packing heuristic for quick sequential placement."""


def next_fit(demands, capacity):
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if any(d < 0 or d > capacity for d in demands):
        raise ValueError("each demand must be between zero and capacity")
    bins = []
    remaining = []
    checks = 0
    for demand in demands:
        if not bins:
            bins.append([demand])
            remaining.append(capacity - demand)
            continue
        checks += 1
        if demand <= remaining[-1]:
            bins[-1].append(demand)
            remaining[-1] -= demand
        else:
            bins.append([demand])
            remaining.append(capacity - demand)
    return bins, remaining, checks


def show_case(label, demands, capacity):
    bins, remaining, checks = next_fit(demands, capacity)
    print(f"{label}: capacity={capacity}; workloads={demands}")
    print(f"  servers={len(bins)}; capacity_checks={checks}; items_processed={len(demands)}")
    for i, (items, free) in enumerate(zip(bins, remaining), start=1):
        print(f"  server {i}: {items}; used={sum(items)}; remaining={free}")
    return bins


def run_tests():
    print("B4 NEXT FIT BIN PACKING (C = 10)")
    ordinary = show_case("ordinary", [2, 5, 4, 7, 1, 3, 8], 10)
    challenge = show_case("challenge", [6, 6, 4, 4], 10)
    empty = show_case("boundary empty", [], 10)
    assert len(ordinary) == 5
    assert len(challenge) == 3
    assert len(empty) == 0
    optimal_challenge = [[6, 4], [6, 4]]
    assert len(optimal_challenge) == 2
    failures = [([-1], 10), ([11], 10), ([1], 0)]
    for demands, capacity in failures:
        try:
            next_fit(demands, capacity)
        except ValueError:
            continue
        raise AssertionError("invalid capacity or demand was accepted")
    print("failure checks: negative/oversized demand and non-positive capacity rejected")
    print("challenge comparison: Next Fit uses 3 servers; feasible optimum uses 2")
    print("RESULT: ordinary, challenge, and empty-boundary tests passed")


if __name__ == "__main__":
    run_tests()
