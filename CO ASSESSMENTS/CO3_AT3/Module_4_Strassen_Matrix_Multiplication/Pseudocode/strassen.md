# Module 4 pseudocode: Strassen matrix multiplication

For equally sized square matrices, split each matrix into four equal quadrants:

```text
STRASSEN(A, B, cutoff)
    if size(A) <= cutoff
        return CLASSICAL-MULTIPLY(A, B)
    split A into A11, A12, A21, A22
    split B into B11, B12, B21, B22

    M1 = STRASSEN(A11 + A22, B11 + B22, cutoff)
    M2 = STRASSEN(A21 + A22, B11,        cutoff)
    M3 = STRASSEN(A11,        B12 - B22, cutoff)
    M4 = STRASSEN(A22,        B21 - B11, cutoff)
    M5 = STRASSEN(A11 + A12, B22,        cutoff)
    M6 = STRASSEN(A21 - A11, B11 + B12, cutoff)
    M7 = STRASSEN(A12 - A22, B21 + B22, cutoff)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    return JOIN(C11, C12, C21, C22)
```

The executable pads a non-power-of-two square matrix to the next power of two, then crops the result. A configurable cutoff uses conventional multiplication for small submatrices.
