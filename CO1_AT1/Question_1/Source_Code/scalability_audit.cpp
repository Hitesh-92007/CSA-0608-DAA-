#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

using Count = std::uint64_t;
constexpr long double OPERATIONS_PER_SECOND = 100'000'000.0L;

Count duplicateComparisons(Count n) {
    return n * (n - 1) / 2;
}

Count auditOperations(Count n) {
    Count total = 0;
    for (Count window = 1; window < n; window *= 2) {
        total += window;
        if (window > UINT64_MAX / 2) break;
    }
    return total;
}

Count nextPowerOfTwo(Count n) {
    Count power = 1;
    while (power < n) power *= 2;
    return power;
}

unsigned log2OfPowerOfTwo(Count n) {
    unsigned levels = 0;
    while (n > 1) {
        n /= 2;
        ++levels;
    }
    return levels;
}

Count binarySearchWorstComparisons(Count n) {
    Count comparisons = 1;
    while (n > 1) {
        n /= 2;
        ++comparisons;
    }
    return comparisons;
}

std::string withCommas(Count value) {
    std::string digits = std::to_string(value);
    for (int pos = static_cast<int>(digits.size()) - 3; pos > 0; pos -= 3) {
        digits.insert(static_cast<std::size_t>(pos), ",");
    }
    return digits;
}

std::string humanDuration(long double seconds) {
    if (seconds >= 3600.0L) {
        const auto hours = static_cast<Count>(seconds / 3600.0L);
        seconds -= hours * 3600.0L;
        const auto minutes = static_cast<Count>(seconds / 60.0L);
        seconds -= minutes * 60.0L;
        std::ostringstream out;
        out << hours << " h " << minutes << " min " << std::fixed
            << std::setprecision(3) << seconds << " s";
        return out.str();
    }
    if (seconds >= 60.0L) {
        const auto minutes = static_cast<Count>(seconds / 60.0L);
        seconds -= minutes * 60.0L;
        std::ostringstream out;
        out << minutes << " min " << std::fixed << std::setprecision(3)
            << seconds << " s";
        return out.str();
    }
    std::ostringstream out;
    out << std::scientific << std::setprecision(3) << seconds << " s";
    return out.str();
}

void printRow(const std::string& module, Count operations) {
    const long double seconds = operations / OPERATIONS_PER_SECOND;
    std::cout << std::left << std::setw(25) << module << std::right
              << std::setw(20) << withCommas(operations) << "  "
              << humanDuration(seconds) << '\n';
}

int main() {
    constexpr Count n = 1'000'000;
    constexpr Count auditCheckN = 1'024;
    const Count paddedN = nextPowerOfTwo(n);
    const unsigned levels = log2OfPowerOfTwo(paddedN);

    const Count m1 = duplicateComparisons(n);
    const Count m2 = auditOperations(n);
    const Count s2Worst = binarySearchWorstComparisons(n);

    // T(1)=1; the recursive estimates use a power-of-two input size.
    const Count m4Current = 2 * paddedN * paddedN - paddedN;
    const Count m4Proposed = paddedN * (levels + 1);
    const Count m5 = paddedN * (levels * (levels + 1) / 2 + 1);

    std::cout << "CSA06 CO1 AT1 - ShopSphere Scalability Audit\n";
    std::cout << "Student: Hitesh | Register No.: 192524005\n";
    std::cout << "Rate: 100,000,000 basic operations per second\n";
    std::cout << "Recursive estimates: next power of two = " << withCommas(paddedN)
              << " (" << levels << " levels); base case T(1)=1\n\n";

    std::cout << "M2 verification at n = " << withCommas(auditCheckN)
              << ": " << withCommas(auditOperations(auditCheckN))
              << " Audit operations (expected 1,023)\n";
    std::cout << "M2 at n = " << withCommas(n) << ": " << withCommas(m2)
              << " Audit operations\n\n";

    std::cout << std::left << std::setw(25) << "Module / design" << std::right
              << std::setw(20) << "Operation units" << "  Estimated time\n";
    std::cout << std::string(72, '-') << '\n';
    printRow("M1 duplicate detector", m1);
    printRow("M2 rate limiter", m2);
    printRow("S2 binary search (worst)", s2Worst);
    printRow("M4 current design", m4Current);
    printRow("M4 proposed design", m4Proposed);
    printRow("M5 sales analytics", m5);

    const long double s1Average = 0.5L * ((n + 1) / 2.0L) + 0.5L * n;
    std::cout << "\nS1 average at n=1,000,000 and p=0.5: " << std::fixed
              << std::setprecision(2) << s1Average << " comparisons\n";
    std::cout << "10-minute decision: M1 and current M4 exceed the window.\n";
    std::cout << "Program completed successfully.\n";
    return 0;
}
