import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# ===============================
# Define O(n) fitting function
# ===============================
def f_n(n, a, b):
    return a * n + b


# ===============================
# Read CSV data
# CSV fields: n,total_sum,dp_time,correct
# ===============================
ns = []
times = []

# 用于存储按n分组的数据
data_by_n = {}

with open("dp_fixedsum_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n_val = int(row["n"])
        time_val = float(row["dp_time"])

        ns.append(n_val)
        times.append(time_val)

        # 按n分组存储时间数据
        if n_val not in data_by_n:
            data_by_n[n_val] = []
        data_by_n[n_val].append(time_val)

ns = np.array(ns)
times = np.array(times)


# ===============================
# Generate statistics table by n
# ===============================
def generate_statistics_table(data_dict):
    """生成统计表格"""
    print("\n" + "=" * 80)
    print("Statistics Table by n")
    print("=" * 80)
    print(f"{'Index':<6} {'n':<10} {'mean':<12} {'min':<12} {'max':<12} {'var':<12}")
    print("-" * 80)

    # 按n排序
    sorted_n = sorted(data_dict.keys())

    table_data = []
    for idx, n_val in enumerate(sorted_n):
        times = data_dict[n_val]
        mean_val = np.mean(times)
        min_val = np.min(times)
        max_val = np.max(times)
        var_val = np.var(times)

        print(
            f"{idx:<6} {n_val:<10} {mean_val:<12.6f} {min_val:<12.6f} {max_val:<12.6f} {var_val:<12.6f}"
        )

        table_data.append(
            {
                "index": idx,
                "n": n_val,
                "mean": mean_val,
                "min": min_val,
                "max": max_val,
                "var": var_val,
            }
        )

    print("=" * 80)
    return table_data


# 生成并显示统计表格
stat_table = generate_statistics_table(data_by_n)

# ===============================
# Fit O(n)
# ===============================
popt, pcov = curve_fit(f_n, ns, times)
a, b = popt
print(f"\nO(n) fit parameters: a = {a:.6f}, b = {b:.6f}")
print(f"Fitted formula: T(n) = {a:.6f} * n + {b:.6f}")

# Compute MSE
mse = np.mean((f_n(ns, a, b) - times) ** 2)
print(f"O(n) fit MSE: {mse:.6e}")

# ===============================
# Plotting
# ===============================
plt.figure(figsize=(10, 6))
plt.scatter(ns, times, color="blue", label="Measured DP time")
plt.plot(ns, f_n(ns, a, b), color="red", linestyle="--", label="O(n) fit")
plt.xlabel("n")
plt.ylabel("DP time (seconds)")
plt.title("DP Algorithm Running Time vs n with O(n) Fit")
plt.legend()
plt.grid(True)
plt.savefig("dp_time_fit_en.png", dpi=200)
plt.show()


# ===============================
# Save statistics table to CSV
# ===============================
def save_statistics_to_csv(table_data, filename="dp_statistics_by_n.csv"):
    """将统计表格保存为CSV文件"""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["index", "n", "mean", "min", "max", "var"])
        # 写入数据
        for row in table_data:
            writer.writerow(
                [
                    row["index"],
                    row["n"],
                    f"{row['mean']:.6f}",
                    f"{row['min']:.6f}",
                    f"{row['max']:.6f}",
                    f"{row['var']:.6f}",
                ]
            )
    print(f"\nStatistics table saved to {filename}")


# 保存统计表格到CSV文件
save_statistics_to_csv(stat_table)
