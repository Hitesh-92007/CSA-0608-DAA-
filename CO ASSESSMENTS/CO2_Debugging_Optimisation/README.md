# CO2 Debugging and Optimisation

**Student:** Hitesh C  
**Register number:** 192524005  
**Course:** CSA06 - Design and Analysis of Algorithms  
**Assessment:** CO2 Debugging and Optimisation Task (50 marks)

This folder contains the original SentinelOps functions, a minimally corrected version, the optimized module, pseudocode, tests, experiments, evidence, and report.

## Folder layout

```text
CO2_Debugging_Optimisation/
├── Pseudocode/
├── Source_Code/
├── Report/
├── Supporting_Files/
└── README.md
```

## Run the programs

Use Python 3.10 or later. Run these commands from this folder:

```powershell
python Source_Code/reproduce_original.py
python Source_Code/stepwise_debug.py
python Source_Code/test_harness.py
python Source_Code/run_experiments.py
python Supporting_Files/create_charts.py
```

The algorithms and tests use only the Python standard library. Regenerating the PNG charts additionally requires Pillow. `run_experiments.py` writes the generated 8,000-point dataset and CSV results under `Supporting_Files/` using fixed seed `20261026`.

## Main files

| File | Purpose |
|---|---|
| `Source_Code/original_module.py` | Original functions copied from the supplied question. |
| `Source_Code/reproduce_original.py` | Expected-versus-actual output for the original test data. |
| `Source_Code/corrected_module.py` | Minimal correctness fixes that keep the original algorithm choices. |
| `Source_Code/optimized_module.py` | Final stable sort, indexed blocklist, KMP matcher, and divide-and-conquer closest pair. |
| `Source_Code/test_harness.py` | Sample, boundary, and randomized equivalence tests. |
| `Source_Code/stepwise_debug.py` | Re-tests after each function is corrected. |
| `Source_Code/run_experiments.py` | Reproducible sorting and closest-pair measurements. |
| `Pseudocode/corrected_algorithms.md` | Pseudocode for the four corrected algorithms. |
| `Pseudocode/optimized_algorithms.md` | Pseudocode for the four optimized algorithms. |
| `Report/Report.pdf` | Complete report with analysis, charts, and evidence captures. |
| `Report/Report.md` | Same report in Markdown form. |

## Experiment range note

The question document asks for three batch sizes “between” but the endpoints are missing in the supplied file. Its scenario specifies 8,000 login events per day, so the measurements use 1,000, 4,000, and 8,000 events. This interpretation is also stated in the report.

## Evidence and submission

The `Supporting_Files/evidence/` images capture source or output files open in Notepad. Output text files are actual Python run logs produced in this workspace; the images are not live terminal screenshots or proof of an individual in-class run. The report identifies this clearly.

The question requests submission of only the GitHub repository link through Google Classroom. Submit the link to this `CO2_Debugging_Optimisation` folder. The code and report were prepared with AI assistance; review the algorithms and course rules before submitting and be ready to explain the work.
