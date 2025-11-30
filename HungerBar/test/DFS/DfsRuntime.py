import argparse
import csv
import random
import subprocess
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# ============================================================
# 1. 生成更难剪枝的 DFS 测试数据
# ============================================================
def gen_hard_dfs_data(n, maxv=2000, file="input.txt"):
    """
    尽量破坏 DFS 的降序排序 & 空桶剪枝。
    """
    base = [random.randint(maxv // 3, maxv // 2) for _ in range(n)]
    arr = [v + random.randint(-3, 3) for v in base]
    random.shuffle(arr)

    with open(file, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    print(f"[OK] Hard DFS data: n={n}, range=({min(arr)}, {max(arr)})")


# ============================================================
# 2. 运行算法 + check
# ============================================================
def run_algorithm_with_check(exe_path, input_file="input.txt"):
    """返回 (时间, check输出)"""
    # 运行算法
    start = time.time()
    try:
        subprocess.run(exe_path, shell=True, check=True)
    except subprocess.CalledProcessError:
        return None, "Runtime Error"
    end = time.time()
    elapsed = end - start

    # 运行 check
    try:
        proc = subprocess.run("./check", capture_output=True, text=True)
        check_output = proc.stdout.strip()
    except Exception as e:
        check_output = f"Check Error: {e}"

    return elapsed, check_output


# ============================================================
# 3. 复杂度函数
# ============================================================
def f_const(n, a, b):
    return a


def f_log(n, a, b):
    return a * np.log2(n) + b


def f_n(n, a, b):
    return a * n + b


def f_nlogn(n, a, b):
    return a * n * np.log2(n) + b


def f_n2(n, a, b):
    return a * (n**2) + b


def f_2n(n, a, b):
    return a * (2 ** (n / 10)) + b  # 缩放避免爆炸


models = {
    "O(1)": f_const,
    "O(log n)": f_log,
    "O(n)": f_n,
    "O(n log n)": f_nlogn,
    "O(n²)": f_n2,
    "O(2ⁿ)": f_2n,
}


# ============================================================
# 4. 复杂度拟合
# ============================================================
def fit_complexity(ns, ts):
    ns = np.array(ns, dtype=float)
    ts = np.array(ts, dtype=float)

    best_name = None
    best_err = float("inf")

    for name, fn in models.items():
        try:
            popt, _ = curve_fit(fn, ns, ts, maxfev=50000)
            mse = np.mean((fn(ns, *popt) - ts) ** 2)
            if mse < best_err:
                best_err = mse
                best_name = name
        except:
            continue

    return best_name, best_err


# ============================================================
# 5. 绘图
# ============================================================
def plot_times(ns, results, algs, out_png="time_plot.png"):
    plt.figure(figsize=(10, 6))
    for alg in algs:
        plt.plot(ns, results[alg], marker="o", label=alg)

    plt.xlabel("n")
    plt.ylabel("Time (sec)")
    plt.title("Algorithm Running Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(out_png, dpi=200)
    print(f"[OK] Plot saved: {out_png}")


# ============================================================
# 6. 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--algs", nargs="+", required=True, help="Example: --algs ./dfs ./dp ./sa"
    )

    parser.add_argument(
        "--ns", nargs="+", required=True, type=int, help="Example: --ns 10 20 30 40"
    )

    parser.add_argument("--outcsv", default="results.csv")
    parser.add_argument("--outpng", default="time_plot.png")
    parser.add_argument("--input", default="input.txt")

    args = parser.parse_args()

    algs = args.algs
    ns = args.ns

    # 用于绘图
    results_time = {alg: [] for alg in algs}

    # CSV 写入
    fcsv = open(args.outcsv, "w", newline="")
    writer = csv.writer(fcsv)
    header = ["n"]
    for alg in algs:
        header.append(f"{alg}_time")
        header.append(f"{alg}_check")
    writer.writerow(header)

    # 主测试循环
    for n in ns:
        print(f"\n==== Testing n = {n} ====")

        # 难数据
        gen_hard_dfs_data(n, file=args.input)

        row = [n]

        for alg in algs:
            t, chk = run_algorithm_with_check(alg)
            results_time[alg].append(t)
            row.append(t)
            row.append(chk)

            print(f"{alg}: time = {t:.6f}, check = {chk}")

        writer.writerow(row)

    fcsv.close()
    print(f"[OK] CSV saved: {args.outcsv}")

    # 绘图
    plot_times(ns, results_time, algs, out_png=args.outpng)

    # 拟合复杂度
    print("\n===== Complexity Fitting =====")
    for alg in algs:
        best, err = fit_complexity(ns, results_time[alg])
        print(f"{alg}: Best fit = {best}, MSE={err:.6e}")


if __name__ == "__main__":
    main()
