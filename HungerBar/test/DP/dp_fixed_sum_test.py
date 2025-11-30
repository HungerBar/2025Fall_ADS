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
    Optionally constrain values inside [min_val, max_val]
    """
    if max_val is None:
        max_val = total_sum - n + 1

    if n * min_val > total_sum or n * max_val < total_sum:
        raise ValueError("Impossible to generate values satisfying sum and bounds.")

    arr = [min_val] * n
    remaining = total_sum - n * min_val

    # Random distribution
    for i in range(n):
        if remaining <= 0:
            break
        add = min(remaining, max_val - arr[i])
        val = random.randint(0, add)
        arr[i] += val
        remaining -= val

    # Any leftovers
    while remaining > 0:
        i = random.randint(0, n - 1)
        if arr[i] < max_val:
            arr[i] += 1
            remaining -= 1

    random.shuffle(arr)

    # Write to file
    with open(file, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    assert sum(arr) == total_sum
    print(f"[OK] Generated: n={n}, sum={total_sum}, range=({min(arr)}, {max(arr)})")
    return arr


# =====================================================
#                     Run Programs
# =====================================================
def run_dp():
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
def plot_results(results_file, output_image="performance_plot_n.png"):
    data = defaultdict(list)

    with open(results_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            t = float(row["dp_time"])
            correct = row["correct"].lower() == "true"
            if correct:
                data[n].append(t)

    ns = sorted(data.keys())
    averages = [np.mean(data[x]) for x in ns]
    std_devs = [np.std(data[x]) for x in ns]

    plt.figure(figsize=(10, 6))
    plt.errorbar(
        ns,
        averages,
        yerr=std_devs,
        fmt="-o",
        markersize=6,
        capsize=4,
        label="Avg dp_time ± std",
    )
    plt.xlabel("n")
    plt.ylabel("dp_time (seconds)")
    plt.title("DP Performance vs n (total_sum fixed)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    print(f"[OK] Plot saved as {output_image}")

    print("\n=== Summary ===")
    for i, x in enumerate(ns):
        print(
            f"n={x}: {len(data[x])} tests, avg={averages[i]:.6f}, std={std_devs[i]:.6f}"
        )


# =====================================================
#                         Main
# =====================================================
def main():
    parser = argparse.ArgumentParser(
        description="DP performance tester with variable n and fixed total_sum"
    )
    parser.add_argument(
        "--ns", type=int, nargs="+", required=True, help="List of n values"
    )
    parser.add_argument("--total_sum", type=int, default=100000, help="Fixed total sum")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--output", type=str, default="dp_n_fixed_sum_results.csv")
    args = parser.parse_args()

    print(f"Fixed total_sum = {args.total_sum}")
    print(f"Testing n values = {args.ns}")

    if not os.path.exists("./dp"):
        print("[ERROR] ./dp not found")
        return

    # Write CSV header
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "total_sum", "dp_time", "correct"])

    for n in args.ns:
        print(f"\n=== Testing n={n} ===")
        times = []

        for trial in range(args.trials):
            print(f"Trial {trial+1}/{args.trials}: ", end="")
            try:
                gen_test_data_fixed_sum(n=n, total_sum=args.total_sum, file="input.txt")
            except Exception as e:
                print(f"Generation failed: {e}")
                continue

            dp_time, err = run_dp()
            if err:
                print(f"DP ERROR: {err}")
                continue

            correct, err2 = run_check()
            if err2:
                print(f"CHECK ERROR: {err2}")
                correct = False

            # Write CSV row
            with open(args.output, "a", newline="") as f:                writer = csv.writer(f)
                writer.writerow([n, args.total_sum, dp_time, correct])

            status = "PASS" if correct else "FAIL"
            print(f"Time={dp_time:.6f}s, Check={status}")

            if correct:
                times.append(dp_time)

        if times:
            print(
                f"n={n}: avg={np.mean(times):.6f}s, std={np.std(times):.6f}s ({len(times)} valid trials)"
            )

    plot_results(args.output)


if __name__ == "__main__":
    main()
