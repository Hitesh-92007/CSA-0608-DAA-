# CO1 AT1 Scalability Audit

This folder contains my CO1 Assessment Tool 1 work for the ShopSphere scalability audit.

## Question 1

- [Report and analysis](Question_1/Report/Report.md)
- [C++ source code](Question_1/Source_Code/scalability_audit.cpp)
- [Program output](Question_1/Report/program_output.txt)
- [Compiler log](Question_1/Report/compile_log.txt)
- [Evidence screenshots](Question_1/Report/Evidence/)

The report answers parts (a) through (g), explains the assumptions used for the operation-count estimates, and gives the redesign recommendation. The C++ program checks the M2 result at n = 1,024 and calculates the requested estimates for n = 1,000,000.

## Compile and run

From `Question_1/Source_Code`, compile with a C++17 compiler:

```text
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic scalability_audit.cpp -o scalability_audit
./scalability_audit
```

On Windows, run `scalability_audit.exe` after compiling. The captured run in the report was compiled with LLVM-MinGW's `g++` (Clang 23.1.1) and completed successfully.

## Before submission

Please review the calculations and the report yourself, then complete the signature and date in the conduct section only if the declaration is accurate under your course rules. This draft was prepared with coding and writing assistance.
