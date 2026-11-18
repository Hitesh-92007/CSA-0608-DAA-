"""Supplementary executable check for CO4A Task 1 (fractional loading)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Package:
    name: str
    weight: float
    value: float

def fractional_knapsack(packages, capacity):
    if capacity < 0 or any(p.weight <= 0 or p.value < 0 for p in packages):
        raise ValueError("Capacity must be non-negative; weights positive; values non-negative")
    ordered = sorted(packages, key=lambda p: p.value / p.weight, reverse=True)
    remaining, total, selected, trace = capacity, 0.0, [], []
    for p in ordered:
        if remaining <= 0:
            break
        amount = min(1.0, remaining / p.weight)
        gain = amount * p.value
        selected.append((p.name, amount, gain))
        remaining -= amount * p.weight
        total += gain
        trace.append((p.name, p.value / p.weight, amount, remaining, total))
    return selected, total, trace

def main():
    packages = [Package("A", 10, 60), Package("B", 20, 100), Package("C", 30, 120)]
    selected, total, trace = fractional_knapsack(packages, 40)
    print("CO4A Task 1: Fractional loading")
    for row in trace: print(f"{row[0]} ratio={row[1]:.1f}, fraction={row[2]:.3f}, remaining={row[3]:.1f}, value={row[4]:.1f}")
    print("Selected:", selected)
    print(f"Maximum value: {total:.1f}")
    assert total == 200 and selected[-1][1] == 1/3
    assert fractional_knapsack([], 0)[1] == 0
    print("Checks: passed (fractional case, empty input)")

if __name__ == "__main__": main()
