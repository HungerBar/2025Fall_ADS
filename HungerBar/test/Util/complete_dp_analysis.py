import argparse
import csv
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


# ===========================================================
#                Load and Aggregate CSV Data
# ===========================================================
def load_data(csv_files):
    results = defaultdict(list)

    for file in csv_files:
        print(f"[INFO] Reading {file}")
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                n = int(row["n"])
                t = float(row["dp_time"])
                correct = row["correct"].strip().lower() in ("1", "true", "yes")

                if correct:
                    results[n].append(t)

    return results


# ===========================================================
#          Fit power-law T(n) = a * n^k using log-log
# ===========================================================
def fit_complexity(ns, ts):
    log_n = np.log(ns)
    log_t = np.log(ts)

    # Fit log(t) = log(a) + k log(n)
    coeff = np.polyfit(log_n, log_t, 1)
    k = coeff[0]  # exponent
    a = np.exp(coeff[1])  # coefficient

    print("\n===== Complexity Fit Result =====")
    print(f"Fitted model: T(n) ≈ {a:.5e} * n^{k:.3f}")
    return a, k


# ===========================================================
#                        Plotting
# ===========================================================
def plot_results(results, output="dp_n_analysis.png"):
    ns = sorted(results.keys())
    avg_times = [np.mean(results[n]) for n in ns]
    std_times = [np.std(results[n]) for n in ns]

    # Fit complexity T = a n^k
    a, k = fit_complexity(np.array(ns), np.array(avg_times))

    # Prepare fitted curve
    fitted_ts = a * np.power(ns, k)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.errorbar(
        ns,
        avg_times,
        yerr=std_times,
        fmt="o",
        capsize=4,
        label="Average dp_time (± std dev)",
    )

    plt.plot(
        ns,
        fitted_ts,
        "-",
        linewidth=2,
        label=f"Fitted complexity: T(n) ≈ {a:.2e} · n^{k:.2f}",
    )

    plt.xlabel("n")
    plt.ylabel("dp_time (seconds)")
    plt.title("DP Algorithm Performance vs n")
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"[OK] Plot saved to: {output}")

    # Print summary
    print("\n===== Summary =====")
    for i, n in enumerate(ns):
        print(
            f"n={n}: samples={len(results[n])}, avg={avg_times[i]:.6f}s, std={std_times[i]:.6f}s"
        )


# ===========================================================
#                           Main
# ===========================================================
def main():
    parser = argparse.ArgumentParser(description="DP Algorithm Complexity Analysis")
    parser.add_argument("--csv", nargs="+", required=True, help="CSV files")
    parser.add_argument("--out", default="dp_n_analysis.png", help="Output image file")
    args = parser.parse_args()

    results = load_data(args.csv)
    plot_results(results, args.out)


if __name__ == "__main__":
    main()
