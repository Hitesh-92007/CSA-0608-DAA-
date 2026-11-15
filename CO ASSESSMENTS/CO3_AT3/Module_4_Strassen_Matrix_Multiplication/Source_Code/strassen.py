"""Classical and Strassen multiplication for square matrices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

Matrix = Sequence[Sequence[int | float]]


@dataclass
class MatrixStats:
    scalar_multiplications: int = 0
    scalar_additions: int = 0
    recursive_calls: int = 0


def _validate_square_pair(a: Matrix, b: Matrix) -> int:
    n = len(a)
    if len(b) != n:
        raise ValueError("matrices must have the same number of rows")
    if any(len(row) != n for row in a) or any(len(row) != n for row in b):
        raise ValueError("this implementation accepts square matrices only")
    return n


def classical_multiply(a: Matrix, b: Matrix,
                       stats: MatrixStats | None = None) -> list[list[int | float]]:
    """Conventional cubic multiplication; counts scalar arithmetic operations."""
    n = _validate_square_pair(a, b)
    if stats is None:
        stats = MatrixStats()
    if n == 0:
        return []
    result: list[list[int | float]] = [[0 for _ in range(n)] for _ in range(n)]
    for row in range(n):
        for col in range(n):
            total = a[row][0] * b[0][col]
            stats.scalar_multiplications += 1
            for inner in range(1, n):
                total += a[row][inner] * b[inner][col]
                stats.scalar_multiplications += 1
                stats.scalar_additions += 1
            result[row][col] = total
    return result


def _add(a: list[list[int | float]], b: list[list[int | float]],
         stats: MatrixStats) -> list[list[int | float]]:
    n = len(a)
    stats.scalar_additions += n * n
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def _subtract(a: list[list[int | float]], b: list[list[int | float]],
              stats: MatrixStats) -> list[list[int | float]]:
    n = len(a)
    stats.scalar_additions += n * n
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def _split(matrix: list[list[int | float]]) -> tuple[
        list[list[int | float]], list[list[int | float]],
        list[list[int | float]], list[list[int | float]]]:
    half = len(matrix) // 2
    top_left = [row[:half] for row in matrix[:half]]
    top_right = [row[half:] for row in matrix[:half]]
    bottom_left = [row[:half] for row in matrix[half:]]
    bottom_right = [row[half:] for row in matrix[half:]]
    return top_left, top_right, bottom_left, bottom_right


def _strassen_power_of_two(a: list[list[int | float]],
                           b: list[list[int | float]], cutoff: int,
                           stats: MatrixStats) -> list[list[int | float]]:
    n = len(a)
    stats.recursive_calls += 1
    if n <= cutoff:
        return classical_multiply(a, b, stats)

    a11, a12, a21, a22 = _split(a)
    b11, b12, b21, b22 = _split(b)

    p1 = _strassen_power_of_two(_add(a11, a22, stats), _add(b11, b22, stats), cutoff, stats)
    p2 = _strassen_power_of_two(_add(a21, a22, stats), b11, cutoff, stats)
    p3 = _strassen_power_of_two(a11, _subtract(b12, b22, stats), cutoff, stats)
    p4 = _strassen_power_of_two(a22, _subtract(b21, b11, stats), cutoff, stats)
    p5 = _strassen_power_of_two(_add(a11, a12, stats), b22, cutoff, stats)
    p6 = _strassen_power_of_two(_subtract(a21, a11, stats), _add(b11, b12, stats), cutoff, stats)
    p7 = _strassen_power_of_two(_subtract(a12, a22, stats), _add(b21, b22, stats), cutoff, stats)

    c11 = _add(_subtract(_add(p1, p4, stats), p5, stats), p7, stats)
    c12 = _add(p3, p5, stats)
    c21 = _add(p2, p4, stats)
    c22 = _add(_add(_subtract(p1, p2, stats), p3, stats), p6, stats)
    upper = [c11[i] + c12[i] for i in range(n // 2)]
    lower = [c21[i] + c22[i] for i in range(n // 2)]
    return upper + lower


def strassen_multiply(a: Matrix, b: Matrix, *, cutoff: int = 64,
                      stats: MatrixStats | None = None) -> list[list[int | float]]:
    """Multiply square matrices, padding/cropping and using classical leaves.

    `cutoff` selects the largest subproblem solved classically. A low cutoff
    demonstrates pure Strassen recurrence; a measured larger cutoff is usually
    more practical because matrix additions and temporary allocations cost time.
    """
    n = _validate_square_pair(a, b)
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    if stats is None:
        stats = MatrixStats()
    if n == 0:
        return []

    padded_n = 1 << (n - 1).bit_length()
    if padded_n == n and n <= cutoff:
        return classical_multiply(a, b, stats)
    padded_a = [list(row) + [0] * (padded_n - n) for row in a]
    padded_b = [list(row) + [0] * (padded_n - n) for row in b]
    for _ in range(padded_n - n):
        padded_a.append([0] * padded_n)
        padded_b.append([0] * padded_n)
    result = _strassen_power_of_two(padded_a, padded_b, cutoff, stats)
    return [row[:n] for row in result[:n]]


if __name__ == "__main__":
    matrix_a = [[1, 7], [3, 5]]
    matrix_b = [[1, 3], [7, 5]]
    conventional_stats = MatrixStats()
    strassen_stats = MatrixStats()
    conventional = classical_multiply(matrix_a, matrix_b, conventional_stats)
    strassen = strassen_multiply(matrix_a, matrix_b, cutoff=1, stats=strassen_stats)
    print("Classical result:", conventional)
    print("Strassen result:", strassen)
    print("Classical scalar multiplications:", conventional_stats.scalar_multiplications)
    print("Strassen scalar multiplications:", strassen_stats.scalar_multiplications)
    print("Strassen scalar additions/subtractions:", strassen_stats.scalar_additions)
