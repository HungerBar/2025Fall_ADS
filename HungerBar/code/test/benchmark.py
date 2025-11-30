import argparse
import csv
import os
import subprocess
import time
import fnmatch  

# Configuration
TESTCASE_DIR = "../../testcases"
INPUT_EXT = ".in"   
OUTPUT_EXT = ".out"

# Core Logic
def run_solver(exe_path, test_id):
    """
    Returns execution time in seconds, or None on failure.
    """
    cmd = [exe_path, "-test", str(test_id)]
    
    start = time.time()
    try:
        # capture_output suppresses stdout/stderr to keep console clean
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        print(f"[Error] Executable not found: {exe_path}")
        return None
        
    end = time.time()
    return end - start

# Helpers
def get_n_from_file(filepath):
    """
    Reads the first number from the input file (usually N) for logging.
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read().split()
            if content:
                return int(content[0])
    except Exception:
        return None
    return None

def get_test_ids_from_args(ids_arg_list, input_ext):
    """
    Parses user arguments to generate the final list of Test IDs.
    Supports keywords like 'scan' or wildcards like 'dp_*'.
    """
    if not os.path.exists(TESTCASE_DIR):
        print(f"[ERROR] Directory '{TESTCASE_DIR}' not found.")
        return []
        
    # Get all base IDs from the directory first
    all_file_ids = [
        f[:-len(input_ext)] for f in os.listdir(TESTCASE_DIR) if f.endswith(input_ext)
    ]
    
    final_ids = set()
    
    for pattern in ids_arg_list:
        # Handle 'scan' or global wildcard
        if pattern.lower() == 'scan' or pattern == '*':
            final_ids.update(all_file_ids)
            continue

        # Handle specific patterns (e.g., 'test_??', 'dp*')
        if '*' in pattern or '?' in pattern:
            matched_ids = fnmatch.filter(all_file_ids, pattern)
            final_ids.update(matched_ids)
        else:
            # Assume exact ID; check existence to avoid runtime errors later
            if pattern in all_file_ids:
                final_ids.add(pattern)
            else:
                print(f"[INFO] Ignoring manual ID '{pattern}'. File not found.")

    return sorted(list(final_ids))

def main():
    parser = argparse.ArgumentParser(description="Automated Benchmark System")
    parser.add_argument("--algs", nargs="+", required=True, help="List of solver executables")
    # args.ns is a list of strings to support patterns
    parser.add_argument("--ns", nargs="+", required=True, help="List of Test IDs (supports patterns like 'dp1_*' or 'scan')")
    parser.add_argument("--outcsv", default="results.csv")
    
    args = parser.parse_args()

    # Resolve test IDs
    test_ids = get_test_ids_from_args(args.ns, INPUT_EXT)
    
    if not test_ids:
        print("[ERROR] No valid test cases found based on input patterns.")
        return

    # Setup CSV
    fcsv = open(args.outcsv, "w", newline="")
    writer = csv.writer(fcsv)
    
    header = ["TestID", "N"]
    for alg in args.algs:
        header.append(f"{os.path.basename(alg)}_Time")
    writer.writerow(header)

    print(f"Starting Benchmark...")
    print(f"Solvers: {args.algs}")
    print(f"Testing {len(test_ids)} total cases.")

    # Console table header
    header_line = "{:<12} {:<8}".format("TestID", "N")
    for alg in args.algs:
        header_line += " {:<12}".format(f"{os.path.basename(alg)}_Time")
    print("-" * len(header_line))
    print(header_line)
    print("-" * len(header_line))

    for test_id in test_ids:
        input_file = os.path.join(TESTCASE_DIR, f"{test_id}{INPUT_EXT}")
        
        # Grab N for context
        current_n = get_n_from_file(input_file)
        n_str = str(current_n) if current_n is not None else "N/A"
        
        output_row = "{:<12} {:<8}".format(test_id, n_str)

        # Run solvers for console output
        for alg in args.algs:
            t = run_solver(alg, test_id)
            if t is None:
                output_row += " {:<12}".format("Error")
            else:
                output_row += " {:<12.6f}".format(t)

        print(output_row)
        
        # Write to CSV
        csv_row = [test_id, n_str]
        
        # Inefficient, but keeps the flow simple. Optimize later if needed.
        for alg in args.algs:
            t = run_solver(alg, test_id)
            if t is None:
                csv_row.append("Error")
            else:
                csv_row.append(f"{t:.6f}")
        
        writer.writerow(csv_row)

    fcsv.close()
    print("-" * len(header_line))
    print(f"[Done] Benchmark finished. Results saved to results.csv")

if __name__ == "__main__":
    main()