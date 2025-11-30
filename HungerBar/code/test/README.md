
# Automated Benchmark & Robustness Testing Scripts

This directory contains Python scripts designed to automate the testing, timing, and analysis of the 3-Partition Problem solvers (`dfs`, `dp`, `sa`).

## 📂 Directory Structure Requirement

The scripts assume the following directory structure. If your structure is different, you may need to adjust the `TESTCASE_DIR` constant inside the Python scripts.

```text
Project_Root/
├── testcases/             # Folder containing .in input files
│   └── *.in
├── src/                   # Folder containing compiled executables
│   ├── dfs.exe            # (or ./dfs on Linux/Mac)
│   ├── dp.exe
│   ├── sa.exe
└── test/                  # Folder containing these Python scripts
    ├── Generator
    ├── benchmark.py
    └── sa_restart_benchmark.py
````

-----

## 1\. General Performance Benchmark (`benchmark.py`)

This script runs specified solvers on selected test cases, measures execution time, and saves the results to a CSV file. It is useful for generating data for performance graphs (e.g., Time vs N).

### Usage

```bash
python benchmark.py --algs <solvers> --ns <test_ids> [options]
```

### Parameters

| Parameter | Required | Description |
| :--- | :---: | :--- |
| `--algs` | Yes | List of solver executable paths (e.g., `../src/dfs.exe ../src/dp.exe`). |
| `--ns` | Yes | List of Test IDs to run. Supports: <br> 1. **Specific IDs**: `1 2 3` <br> 2. **Wildcards**: `dp1_*` or `test_?` <br> 3. **Scan Mode**: `scan` (runs all `.in` files in the directory). |
| `--outcsv` | No | Path to the output CSV file. Default: `results.csv`. |

### Examples

**1. Run DFS on all files starting with "dp1\_" (Standard Mode):**

```bash
python benchmark.py \
  --algs ../src/dfs.exe \
  --ns dp1_* \
  --outcsv dfs_report.csv
```

**2. Run DP on specific test cases:**

```bash
python benchmark.py \
  --algs ../src/dp.exe \
  --ns 10 20 30 \
  --outcsv dp_report.csv
```

-----

## 2\. SA Robustness Test (`sa_restart_benchmark.py`)

This script is specifically designed for **Simulated Annealing (SA)**. It tests the algorithm's reliability by counting how many **restarts** are needed to find a solution for known solvable inputs.

It runs the SA solver repeatedly (up to `K_MAX=10` times) for each test case until it outputs "yes".

### Usage

```bash
python sa_restart_benchmark.py --ns <test_ids> [options]
```

### Parameters

| Parameter | Required | Description |
| :--- | :---: | :--- |
| `--ns` | Yes | List of Test IDs to run. Supports specific IDs, wildcards (`sa_*`), or `scan`. |
| `--outcsv` | No | Path to the output CSV file. Default: `sa_restart_distribution.csv`. |

### Examples

**1. Test robustness on specific SA test cases:**

```bash
python sa_restart_benchmark.py --ns sa_1 sa_2 sa_3 --outcsv sa_analysis.csv
```

**2. Batch test using wildcards:**

```bash
python sa_restart_benchmark.py --ns sa_*
```

### Output CSV Format

The script generates a CSV with the following columns:

  * `instance_id`: The filename of the test case.
  * `first_success_restart`: The iteration number (1-10) where SA successfully found a solution. `-1` if failed after all retries.
  * `success_flag`: `True` if a solution was found, `False` otherwise.

-----

## Troubleshooting

  * **[Error] Executable not found**: Check if the paths provided in `--algs` are correct relative to where you are running the python script. On Windows, ensure you include `.exe`.
  * **[Error] Directory not found**: Open the python scripts and check if `TESTCASE_DIR` (default `../../testcases`) matches your actual folder structure.
  * **CSV not updating**: The `sa_restart_benchmark.py` writes to CSV in real-time (append mode), so you can view results while the script is running. `benchmark.py` writes row by row as well.

<!-- end list -->
