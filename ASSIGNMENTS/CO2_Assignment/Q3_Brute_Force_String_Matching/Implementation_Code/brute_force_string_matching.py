"""Naive all-occurrences string matching for CO2 Q3."""


def brute_force_match(text, pattern):
    if pattern == "":
        return list(range(len(text) + 1)), 0
    if len(pattern) > len(text):
        return [], 0
    matches = []
    comparisons = 0
    for shift in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern):
            comparisons += 1
            if text[shift + j] != pattern[j]:
                break
            j += 1
        if j == len(pattern):
            matches.append(shift)
    return matches, comparisons


def run():
    cases = [
        ("early distinct hit", "AUTH_FAIL: other log entries", "AUTH_FAIL"),
        ("late near-match", "A" * 5_000 + "B", "A" * 49 + "B"),
        ("overlapping matches", "ABABABA", "ABA"),
    ]
    return [(name, len(text), len(pattern), *brute_force_match(text, pattern))
            for name, text, pattern in cases]


if __name__ == "__main__":
    for name, n, m, matches, comparisons in run():
        preview = matches if len(matches) <= 8 else matches[:3] + ["..."] + matches[-2:]
        print(f"{name:22} n={n:5} m={m:3} comparisons={comparisons:8} "
              f"matches={preview}")
