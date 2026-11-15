"""Q3: decimal-digit schoolbook multiplication and Karatsuba multiplication."""
from __future__ import annotations


def schoolbook_multiply(a: int, b: int, stats: dict[str, int] | None = None) -> int:
    sign = -1 if (a < 0) != (b < 0) else 1
    x, y = str(abs(a)), str(abs(b))
    if x == "0" or y == "0":
        return 0
    xd, yd = [int(c) for c in x[::-1]], [int(c) for c in y[::-1]]
    result = [0] * (len(xd) + len(yd))
    for i, da in enumerate(xd):
        for j, db in enumerate(yd):
            result[i + j] += da * db
            if stats is not None:
                stats["digit_multiplications"] += 1
    for k in range(len(result) - 1):
        carry, result[k] = divmod(result[k], 10)
        result[k + 1] += carry
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return sign * int("".join(map(str, result[::-1])))


def karatsuba_multiply(a: int, b: int, threshold_digits: int = 24,
                       stats: dict[str, int] | None = None) -> int:
    if threshold_digits < 1:
        raise ValueError("threshold_digits must be positive")
    sign = -1 if (a < 0) != (b < 0) else 1
    x, y = abs(a), abs(b)
    own = stats if stats is not None else {"digit_multiplications": 0, "recursive_calls": 0, "max_depth": 0}

    def rec(left: int, right: int, depth: int) -> int:
        own["recursive_calls"] += 1
        own["max_depth"] = max(own["max_depth"], depth)
        if left == 0 or right == 0:
            return 0
        digits = max(len(str(left)), len(str(right)))
        if digits <= threshold_digits:
            return schoolbook_multiply(left, right, own)
        split = digits // 2
        base = 10 ** split
        high_l, low_l = divmod(left, base)
        high_r, low_r = divmod(right, base)
        z0 = rec(low_l, low_r, depth + 1)
        z2 = rec(high_l, high_r, depth + 1)
        z1 = rec(low_l + high_l, low_r + high_r, depth + 1) - z0 - z2
        return z2 * base * base + z1 * base + z0

    return sign * rec(x, y, 1)


def demo() -> str:
    a, b = 12345678901234567890, 98765432109876543210
    counts = {"digit_multiplications": 0, "recursive_calls": 0, "max_depth": 0}
    school = schoolbook_multiply(a, b)
    kara = karatsuba_multiply(a, b, threshold_digits=3, stats=counts)
    return "\n".join([
        f"A = {a}", f"B = {b}", f"Product = {kara}",
        f"Schoolbook matches Karatsuba: {school == kara}",
        f"Schoolbook digit multiplications: {len(str(a)) * len(str(b))}",
        f"Karatsuba base digit multiplications: {counts['digit_multiplications']}",
        f"Karatsuba recursive calls: {counts['recursive_calls']}, maximum depth: {counts['max_depth']}",
    ])


if __name__ == "__main__":
    print(demo())
