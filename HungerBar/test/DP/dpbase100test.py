import argparse
import csv
import os
import random
import subprocess
import time

# ===============================
# 配置参数
# ===============================
INPUT_FILE = "input.txt"
DEFAULT_VALUE_MEAN = 100
DEFAULT_VALUE_NOISE = 20
OUTPUT_CSV = "dpbase100.csv"


# ===============================
# 生成随机数据数组，长度为 n
# 元素在 mean ± noise
# ===============================
def gen_data(n, mean=DEFAULT_VALUE_MEAN, noise=DEFAULT_VALUE_NOISE):
    arr = [max(1, mean + random.randint(-noise, noise)) for _ in range(n)]
    random.shuffle(arr)
    return arr


# ===============================
# 写入 input.txt
# ===============================
def write_input(arr):
    with open(INPUT_FILE, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")


# ===============================
# 运行 ./dp
# ===============================
def run_dp():
    if not os.path.exists("./dp"):
        raise FileNotFoundError("./dp not found")
    start = time.time()
    proc = subprocess.Popen(["./dp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    end = time.time()
    if proc.returncode != 0:
        print(stderr.decode())
        return None
    return end - start


# ===============================
# 运行 ./check
# ===============================
def run_check():
    if not os.path.exists("./check"):
        raise FileNotFoundError("./check not found")
    proc = subprocess.Popen(["./check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return b"yes" in stdout.lower() or b"true" in stdout.lower()


# ===============================
# 主程序
# ===============================
def main():
    parser = argparse.ArgumentParser(
        description="DP test with user-defined n and random sum"
    )
    parser.add_argument(
        "--n_list",
        type=int,
        nargs="+",
        required=True,
        help="List of n values to test, e.g., --n_list 50 100 150",
    )
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per n")
    parser.add_argument(
        "--output", type=str, default=OUTPUT_CSV, help="CSV output file"
    )
    args = parser.parse_args()

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "sum", "dp_time", "correct"])

        for n in args.n_list:
            for trial in range(args.trials):
                arr = gen_data(n)
                total_sum = sum(arr)
                write_input(arr)
                dp_time = run_dp()
                correct = run_check()
                print(
                    f"n={n}, sum={total_sum}, dp_time={dp_time:.6f}, correct={correct}"
                )
                writer.writerow([n, total_sum, dp_time, correct])


if __name__ == "__main__":
    main()
