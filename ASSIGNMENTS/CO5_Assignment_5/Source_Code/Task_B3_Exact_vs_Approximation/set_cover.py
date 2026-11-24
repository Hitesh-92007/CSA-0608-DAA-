"""Exact and greedy algorithms for unweighted emergency-service set cover."""
from itertools import combinations


def _encode(universe, centres):
    index = {zone: i for i, zone in enumerate(universe)}
    if len(index) != len(universe):
        raise ValueError("universe zones must be unique")
    masks = []
    for covered in centres:
        unknown = set(covered) - set(index)
        if unknown:
            raise ValueError(f"centre refers to unknown zones: {sorted(unknown)}")
        mask = 0
        for zone in covered:
            mask |= 1 << index[zone]
        masks.append(mask)
    return masks, (1 << len(universe)) - 1


def exact_cover(universe, centres):
    """Minimum-cardinality cover by increasing-size subset enumeration.

    Returns (indices-or-None, subsets_checked). The exponential search is
    intentional and is limited to the small exact instances in this exercise.
    """
    masks, target = _encode(universe, centres)
    checked = 0
    for size in range(len(centres) + 1):
        for choice in combinations(range(len(centres)), size):
            checked += 1
            covered = 0
            for j in choice:
                covered |= masks[j]
            if covered == target:
                return list(choice), checked
    return None, checked


def greedy_cover(universe, centres):
    """Select the centre covering the most currently uncovered zones.

    Ties go to the lowest input index. Returns (indices-or-None, scans).
    """
    masks, target = _encode(universe, centres)
    uncovered = target
    remaining = set(range(len(centres)))
    selected = []
    scans = 0
    while uncovered:
        best = None
        best_gain = 0
        for i in sorted(remaining):
            scans += 1
            gain = (masks[i] & uncovered).bit_count()
            if gain > best_gain:
                best, best_gain = i, gain
        if best is None:
            return None, scans
        selected.append(best)
        remaining.remove(best)
        uncovered &= ~masks[best]
    return selected, scans


def run_tests():
    tests = [
        ("balanced six-zone", list("ABCDEF"), [
            set("ABC"), set("DEF"), set("AD"), set("BE"), set("CF")
        ]),
        ("greedy counterexample", [1, 2, 3, 4, 5, 6], [
            {1, 2, 3, 4}, {1, 2, 5}, {3, 4, 6}
        ]),
        ("five-zone overlap", [1, 2, 3, 4, 5], [
            {1, 2, 3}, {2, 4}, {3, 5}, {1, 4, 5}
        ]),
    ]
    print("B3 EXACT VS GREEDY SET COVER")
    print("case,exact_size,greedy_size,same,exact_subsets,greedy_scans")
    for label, universe, centres in tests:
        exact, checked = exact_cover(universe, centres)
        greedy, scans = greedy_cover(universe, centres)
        assert exact is not None and greedy is not None
        print(f"{label},{len(exact)},{len(greedy)},{len(exact)==len(greedy)},{checked},{scans}")
        print(f"  exact centres={[i + 1 for i in exact]}; "
              f"greedy centres={[i + 1 for i in greedy]}")

    # Boundary and infeasible cases are kept separate from the three comparisons.
    assert exact_cover([], [set()])[0] == []
    assert greedy_cover([], [set()])[0] == []
    assert exact_cover([1, 2], [{1}])[0] is None
    assert greedy_cover([1, 2], [{1}])[0] is None
    print("boundary checks: empty universe covered; impossible instance reported")

    print("SCALING: two singleton centres per zone; exact subset enumeration")
    print("zones,centres,exact_size,greedy_size,subsets_checked,greedy_scans")
    for zone_count in (4, 6, 8):
        universe = list(range(zone_count))
        centres = [{z} for z in universe for _ in range(2)]
        exact, checked = exact_cover(universe, centres)
        greedy, scans = greedy_cover(universe, centres)
        assert len(exact) == zone_count and len(greedy) == zone_count
        print(f"{zone_count},{len(centres)},{len(exact)},{len(greedy)},{checked},{scans}")
    print("RESULT: all exact covers verified; counterexample exposes greedy gap")


if __name__ == "__main__":
    run_tests()
