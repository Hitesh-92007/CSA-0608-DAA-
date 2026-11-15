"""Exhaustive subset enumeration for CO2 Q6."""

from time import perf_counter


def exhaustive_knapsack(packages, capacity):
    n = len(packages)
    best_value = 0
    best_weight = 0
    best_mask = 0
    item_checks = 0
    start = perf_counter()
    for mask in range(1 << n):
        weight = value = 0
        for i, package in enumerate(packages):
            item_checks += 1
            if mask & (1 << i):
                weight += package["weight"]
                value += package["value"]
        if weight <= capacity and value > best_value:
            best_value, best_weight, best_mask = value, weight, mask
    elapsed = perf_counter() - start
    selected = [packages[i]["id"] for i in range(n) if best_mask & (1 << i)]
    return {"selected": selected, "weight": best_weight, "value": best_value,
            "candidate_subsets": 1 << n, "item_checks": item_checks,
            "seconds": elapsed}


def sample_packages():
    return [
        {"id": "A", "weight": 10, "value": 60},
        {"id": "B", "weight": 5, "value": 40},
        {"id": "C", "weight": 6, "value": 30},
        {"id": "D", "weight": 4, "value": 20},
    ]


def generated_packages(n, seed=8801):
    return [{"id": f"P{i:02d}", "weight": 1 + ((i * 7 + seed) % 15),
             "value": 5 + ((i * 11 + seed) % 50)} for i in range(n)]


def run():
    result = exhaustive_knapsack(sample_packages(), 15)
    assert result["selected"] == ["A", "B"] and result["value"] == 100
    return result


if __name__ == "__main__":
    result = run()
    print(f"verified sample: selected={result['selected']} weight={result['weight']} "
          f"value={result['value']}")
    print(f"candidate subsets={result['candidate_subsets']} "
          f"item checks={result['item_checks']} time={result['seconds']:.8f}s")
    print("growth experiment: n, subsets, item checks, best value, seconds")
    for n in (8, 12, 16, 18, 20):
        packages = generated_packages(n)
        capacity = sum(package["weight"] for package in packages) // 2
        measured = exhaustive_knapsack(packages, capacity)
        print(f"{n}, {measured['candidate_subsets']}, {measured['item_checks']}, "
              f"{measured['value']}, {measured['seconds']:.6f}")
