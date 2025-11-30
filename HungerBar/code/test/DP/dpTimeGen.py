import argparse
import os
import random

# ===============================
# 配置参数
# ===============================
DEFAULT_VALUE_MEAN = 100
DEFAULT_VALUE_NOISE = 20


# ===============================
# 生成随机数据数组，长度为 n
# 元素在 mean ± noise
# ===============================
def gen_data(n, mean=DEFAULT_VALUE_MEAN, noise=DEFAULT_VALUE_NOISE):
    arr = [max(1, mean + random.randint(-noise, noise)) for _ in range(n)]
    random.shuffle(arr)
    return arr


# ===============================
# 写入指定文件
# ===============================
def write_input(arr, file):
    with open(file, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")


# ===============================
# 主程序
# ===============================
def main():
    parser = argparse.ArgumentParser(description="Generate DP testcases only")
    parser.add_argument(
        "--n_list",
        type=int,
        nargs="+",
        required=True,
        help="List of n values to generate, e.g., --n_list 50 100 150",
    )
    parser.add_argument(
        "--trials", type=int, default=1, help="Number of testcases per n"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="testcases",
        help="Directory to save testcases",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    idx = 1
    for n in args.n_list:
        for trial in range(args.trials):
            arr = gen_data(n)
            filename = os.path.join(args.output_dir, f"dp3_{idx}.in")
            write_input(arr, filename)
            print(
                f"[OK] Generated {filename}: n={n}, sum={sum(arr)}, range=({min(arr)}, {max(arr)})"
            )
            idx += 1


if __name__ == "__main__":
    main()
