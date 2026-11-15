# Q3 pseudocode

```text
KARATSUBA(x, y)
    if either operand is zero: return 0
    if max(number of digits in x, number of digits in y) <= threshold:
        return SCHOOLBOOK(x, y)
    m = floor(max digit length / 2); base = 10^m
    x = xHigh * base + xLow
    y = yHigh * base + yLow
    z0 = KARATSUBA(xLow, yLow)
    z2 = KARATSUBA(xHigh, yHigh)
    z1 = KARATSUBA(xLow + xHigh, yLow + yHigh) - z0 - z2
    return z2*base^2 + z1*base + z0
```

The cross term is recovered by subtraction, reducing four half-size recursive products to three. `T(n)=3T(n/2)+Theta(n)` so `T(n)=Theta(n^(log2 3))`, about `Theta(n^1.585)`. Schoolbook multiplication takes `Theta(n^2)`. Karatsuba's additions, slicing/conversion, recursion, and base-case threshold create overhead; the practical crossover is measured rather than assumed. Auxiliary space depends on representation; this decimal-string reference uses recursive integer temporaries and conversion storage, up to `O(n log n)` in the simple implementation.
