# Q4 pseudocode

## Conventional block multiplication

For 2 x 2 blocks, compute `C11=A11B11+A12B21`, `C12=A11B12+A12B22`, `C21=A21B11+A22B21`, and `C22=A21B12+A22B22`. This uses eight half-size products.

## Strassen

```text
STRASSEN(A, B)
    if n <= cutoff: return conventional multiply
    split A and B into four n/2 by n/2 blocks
    M1=(A11+A22)(B11+B22); M2=(A21+A22)B11
    M3=A11(B12-B22);       M4=A22(B21-B11)
    M5=(A11+A12)B22;       M6=(A21-A11)(B11+B12)
    M7=(A12-A22)(B21+B22)
    C11=M1+M4-M5+M7; C12=M3+M5
    C21=M2+M4;       C22=M1-M2+M3+M6
    join the four C blocks
```

Pad a non-power-of-two square matrix with zeros to the next power of two, then crop the product. `T(n)=7T(n/2)+Theta(n^2)=Theta(n^(log2 7))`, about `Theta(n^2.807)`; conventional multiplication is `Theta(n^3)`. The reference implementation also counts additions and uses a cutoff. Padding, recursion, temporary matrices, additions, cache effects, and memory can make conventional multiplication faster at small and medium sizes. Classical multiplication uses `Theta(n^2)` output space; recursive Strassen creates additional temporary matrices, up to `O(n^2)` live storage with careful release, and more in a straightforward language implementation.
