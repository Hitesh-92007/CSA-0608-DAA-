"""Q4: conventional and Strassen square-matrix multiplication."""
from __future__ import annotations

from typing import Sequence

Matrix = list[list[int]]


def _validate(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> int:
    n = len(a)
    if n == 0 or len(b) != n or any(len(row) != n for row in a) or any(len(row) != n for row in b):
        raise ValueError("A and B must be non-empty square matrices of the same size")
    return n


def conventional(a: Matrix, b: Matrix, stats: dict[str, int] | None = None) -> Matrix:
    n = _validate(a, b)
    count = stats if stats is not None else {"multiplications": 0, "additions": 0}
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                c[i][j] += a[i][k] * b[k][j]
                count["multiplications"] += 1
                if k:
                    count["additions"] += 1
    return c


def strassen(a: Matrix, b: Matrix, cutoff: int = 16,
             stats: dict[str, int] | None = None) -> Matrix:
    n = _validate(a, b)
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    count = stats if stats is not None else {"multiplications": 0, "additions": 0, "recursive_calls": 0}
    size = 1
    while size < n:
        size *= 2
    ap = [row + [0] * (size - n) for row in a] + [[0] * size for _ in range(size - n)]
    bp = [row + [0] * (size - n) for row in b] + [[0] * size for _ in range(size - n)]

    def add(x: Matrix, y: Matrix, subtract: bool = False) -> Matrix:
        count["additions"] += len(x) * len(x)
        if subtract:
            return [[x[i][j] - y[i][j] for j in range(len(x))] for i in range(len(x))]
        return [[x[i][j] + y[i][j] for j in range(len(x))] for i in range(len(x))]

    def classic(x: Matrix, y: Matrix) -> Matrix:
        n0 = len(x)
        out = [[0] * n0 for _ in range(n0)]
        for i in range(n0):
            for k in range(n0):
                for j in range(n0):
                    out[i][j] += x[i][k] * y[k][j]
                    count["multiplications"] += 1
                    if k:
                        count["additions"] += 1
        return out

    def rec(x: Matrix, y: Matrix) -> Matrix:
        count["recursive_calls"] = count.get("recursive_calls", 0) + 1
        n0 = len(x)
        if n0 <= cutoff:
            return classic(x, y)
        half = n0 // 2
        a11 = [row[:half] for row in x[:half]]; a12 = [row[half:] for row in x[:half]]
        a21 = [row[:half] for row in x[half:]]; a22 = [row[half:] for row in x[half:]]
        b11 = [row[:half] for row in y[:half]]; b12 = [row[half:] for row in y[:half]]
        b21 = [row[:half] for row in y[half:]]; b22 = [row[half:] for row in y[half:]]
        m1 = rec(add(a11, a22), add(b11, b22))
        m2 = rec(add(a21, a22), b11)
        m3 = rec(a11, add(b12, b22, True))
        m4 = rec(a22, add(b21, b11, True))
        m5 = rec(add(a11, a12), b22)
        m6 = rec(add(a21, a11, True), add(b11, b12))
        m7 = rec(add(a12, a22, True), add(b21, b22))
        c11 = add(add(add(m1, m4), m5, True), m7)
        c12 = add(m3, m5)
        c21 = add(m2, m4)
        c22 = add(add(add(m1, m2, True), m3), m6)
        count["additions"] += n0 * n0
        return [c11[i] + c12[i] for i in range(half)] + [c21[i] + c22[i] for i in range(half)]

    padded = rec(ap, bp)
    return [row[:n] for row in padded[:n]]


def demo() -> str:
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    classic_stats = {"multiplications": 0, "additions": 0}
    strassen_stats = {"multiplications": 0, "additions": 0, "recursive_calls": 0}
    c1 = conventional(a, b, classic_stats)
    c2 = strassen(a, b, cutoff=1, stats=strassen_stats)
    return "\n".join([
        f"A = {a}", f"B = {b}", f"A x B = {c2}",
        f"Strassen equals conventional: {c1 == c2}",
        f"Conventional scalar multiplications: {classic_stats['multiplications']}",
        f"Strassen scalar multiplications: {strassen_stats['multiplications']}",
        f"Strassen scalar additions/subtractions: {strassen_stats['additions']}",
        f"Padding: 3x3 matrix padded to {1 << (len(a)-1).bit_length()}x{1 << (len(a)-1).bit_length()} then cropped.",
    ])


if __name__ == "__main__":
    print(demo())
