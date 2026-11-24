# CO5 Assignment 5

**Search, Complexity and Approximation Engineering**  
Student: Hitesh C  
Register number: 192524005  
Course: CSA06 - Design and Analysis of Algorithms

This folder contains the Part A design and pseudocode, and the Part B source programs, test inputs, run outputs and consolidated report for CO5 Assignment 5.

## Contents

- `Source_Code/Task_B1_Graph_Colouring/` - instrumented backtracking; input-order and DSATUR vertex choices.
- `Source_Code/Task_B2_Adversarial_Search/` - same-size path and odd-wheel comparison; imports the B1 implementation.
- `Source_Code/Task_B3_Exact_vs_Approximation/` - exact subset enumeration and greedy set cover, test cases and scaling counts.
- `Source_Code/Task_B4_Bin_Packing/` - instrumented Next Fit placement and a small non-optimal example.
- Each task folder contains its test input JSON (where applicable) and `execution_output.txt` captured from the program run.
- `Report/CO5_Assignment_5_Report.pdf` - consolidated report with Part A, analysis, tests, outputs and full source listings.

## Run the programs

Use Python 3.10 or newer. From this folder, run:

```text
python Source_Code/Task_B1_Graph_Colouring/graph_colouring.py
python Source_Code/Task_B2_Adversarial_Search/compare_instances.py
python Source_Code/Task_B3_Exact_vs_Approximation/set_cover.py
python Source_Code/Task_B4_Bin_Packing/bin_packing.py
```

The numerical values for the number of colours and server capacity appear as symbols in the provided brief. To make the required experiments concrete, the report uses `k = 3` colours and bin capacity `C = 10`; these are documented as experimental choices, not values stated by the assignment.

The exact set-cover program is intentionally exponential and is run only on the small instances described in the report. The larger set-cover comparison records exact search effort through eight zones and compares it with greedy candidate scans.
