import argparse
import csv
import os
import random
import subprocess
import time
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


# =====================================================
#              Test Data Generation
# =====================================================
def gen_test_data_fixed_sum(n, total_sum, min_val=1, max_val=None, file="input.txt"):
    """
    Generate n positive integers whose sum equals total_sum
    Optionally, each number is in [min_val, max_val]
    """
    if max_val is None:
        max_val = total_sum - n + 1  # max possible if min_val=1

    if n * min_val > total_sum or n * max_val < total_sum:
        raise ValueError("Impossible to generate numbers with given sum and bounds.")

    # Start with n minimum values
    arr = [min_val] * n
    remaining = total_sum - n * min_val

    # Randomly distribute remaining sum
    for i in range(n):
        if remaining <= 0:
            break
        add = min(remaining, max_val - arr[i])
        val = random.randint(0, add)
        arr[i] += val
        remaining -= val

    # Distribute any remaining sum
    while remaining > 0:
        i = random.randint(0, n - 1)
        if arr[i] < max_val:
            arr[i] += 1
            remaining -= 1

    random.shuffle(arr)

    # Write to input file
    with open(file, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    actual_sum = sum(arr)
    assert actual_sum == total_sum, f"Sum mismatch: {actual_sum} != {total_sum}"
    print(
        f"[OK] Test data generated: n={n}, sum={total_sum}, range=({min(arr)}, {max(arr)})"
    )
    return arr


# =====================================================
#                     Run Programs
# =====================================================
def run_dp():
    """Run ./dp and return time taken (seconds)"""
    if not os.path.exists("./dp"):
        return None, "./dp not found"

    start = time.time()
    try:
        proc = subprocess.Popen(
            ["./dp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        end = time.time()

        if proc.returncode != 0:
            return None, f"dp exited with code {proc.returncode}"
        return end - start, None
    except Exception as e:
        return None, f"Error running dp: {str(e)}"


def run_check():
    """Run ./check to verify correctness"""
    if not os.path.exists("./check"):
        return None, "./check not found"

    try:
        proc = subprocess.Popen(
            ["./check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            return False, f"check failed with code {proc.returncode}"
        return True, None
    except Exception as e:
        return False, f"Error running check: {str(e)}"


# =====================================================
#              Plotting Function
# =====================================================
def plot_results(results_file, output_image="performance_plot.png"):
    """Read CSV and plot average time ± std dev vs total_sum"""
    data = defaultdict(list)
    with open(results_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_sum = int(row["total_sum"])
            data[total_sum].append(float(row["dp_time"]))

    sums = sorted(data.keys())
    averages = [np.mean(data[s]) for s in sums]
    std_devs = [np.std(data[s]) for s in sums]

    plt.figure(figsize=(10, 6))
    plt.errorbar(
        sums,
        averages,
        yerr=std_devs,
        fmt="-o",
        linewidth=2,
        markersize=6,
        capsize=4,
        label="Average time ± std dev",
    )
    plt.xlabel("Total Sum")
    plt.ylabel("Execution Time (seconds)")
    plt.title("DP Algorithm Performance vs Total Sum")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    print(f"[OK] Performance plot saved as {output_image}")

    print("\n=== Performance Summary ===")
    for i, s in enumerate(sums):
        print(
            f"total_sum={s}: {len(data[s])} tests, avg={averages[i]:.6f}s, std={std_devs[i]:.6f}s"
        )


# =====================================================
#                         Main
# =====================================================
def main():
    parser = argparse.ArgumentParser(
        description="DP performance tester with fixed n and total_sum"
    )
    parser.add_argument("--n", type=int, required=True, help="Number of items")
    parser.add_argument(
        "--sums", type=int, nargs="+", required=True, help="Total sums to test"
    )
    parser.add_argument(
        "--trials", type=int, default=3, help="Number of trials per total_sum"
    )
    parser.add_argument(
        "--output", type=str, default="dp_fixed_sum_results.csv", help="CSV output file"
    )
    args = parser.parse_args()

    print(f"Fixed input size: n={args.n}")
    print(f"Total sums to test: {args.sums}, Trials per sum: {args.trials}")

    if not os.path.exists("./dp"):
        print("[ERROR] ./dp executable not found")
        return

    # Initialize CSV
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "total_sum", "dp_time", "correct"])

    for total_sum in args.sums:
        print(f"\n=== Testing total_sum={total_sum} ===")
        times = []

        for trial in range(args.trials):
            print(f"Trial {trial+1}/{args.trials}: ", end="")
            try:
                gen_test_data_fixed_sum(n=args.n, total_sum=total_sum, file="input.txt")
            except Exception as e:
                print(f"Data generation failed: {e}")
                continue

            dp_time, error = run_dp()
            if error:
                print(f"DP execution failed: {error}")
                continue

            correct, check_error = run_check()
            if check_error:
                print(f"Check failed: {check_error}")
                correct = False

            # Write results
            with open(args.output, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([args.n, total_sum, dp_time, correct])

            status = "PASS" if correct else "FAIL"
            print(f"Time: {dp_time:.6f}s, Check: {status}")

            if correct:
                times.append(dp_time)

        if times:
            avg_time = np.mean(times)
            std_time = np.std(times) if len(times) > 1 else 0
            print(f"total_sum={total_sum}: avg_time={avg_time:.6f}s ± {std_time:.6f}s")

    # Plot results
    plot_results(args.output)


if __name__ == "__main__":
    main()
