import argparse
import csv
import os
import shutil
import subprocess
import time


# ============================================================
# 1. 从 /testcases 读取数据并复制到 input.txt
# ============================================================
def load_testcase(i, testcase_dir="testcases", input_file="input.txt"):
    """
    从 /testcases 读取 dfs_i.in 并复制为 input.txt。
    返回 n（数组长度）。
    """
    src = os.path.join(testcase_dir, f"dfs{i}.in")
    if not os.path.exists(src):
        raise FileNotFoundError(f"测试文件不存在: {src}")

    shutil.copy(src, input_file)
    print(f"[OK] Loaded testcase: {src} → {input_file}")

    with open(src, "r") as f:
        n = int(f.readline().strip())
    return n


# ============================================================
# 2. 运行算法 + check
# ============================================================
def run_algorithm_with_check(exe_path, input_file="input.txt"):
    """
    返回 (运行时间, check 输出)
    """
    start = time.time()
    try:
        subprocess.run(exe_path, shell=True, check=True)
    except subprocess.CalledProcessError:
        return float("inf"), "Runtime Error"
    end = time.time()

    elapsed = end - start

    # run ./check
    try:
        proc = subprocess.run("./check", capture_output=True, text=True)
        check_output = proc.stdout.strip()
    except Exception as e:
        check_output = f"Check Error: {e}"

    return elapsed, check_output


# ============================================================
# 3. 主流程（按 testcases/dfs_i.in 顺序执行）
# ============================================================
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--algs", nargs="+", required=True, help="Example: --algs ./dfs ./dp ./sa"
    )

    parser.add_argument(
        "--k",
        type=int,
        default=None,
        help="原始功能：测试从 dfs1.in 到 dfs_k.in（包含 k）",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="新功能：测试用例起始编号（包含），默认不使用",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="新功能：测试用例结束编号（包含），与 --start 配合使用",
    )

    parser.add_argument("--testdir", default="testcases")
    parser.add_argument("--outcsv", default="results.csv")
    parser.add_argument("--input", default="input.txt")

    args = parser.parse_args()

    algs = args.algs

    # 生成测试编号列表
    if args.start is not None and args.end is not None:
        test_indices = list(range(args.start, args.end + 1))
    elif args.k is not None:
        test_indices = list(range(1, args.k + 1))  # 从 1 开始，包含 k
    else:
        raise ValueError("请提供 --k 或 --start 和 --end 作为测试范围")

    # 打开 CSV
    with open(args.outcsv, "w", newline="") as fcsv:
        writer = csv.writer(fcsv)

        # CSV 标题
        header = ["n"]
        for alg in algs:
            header.append(f"{alg}_time")
            header.append(f"{alg}_check")
        writer.writerow(header)

        # 主循环
        for idx in test_indices:
            print(f"\n==== Testing testcase dfs{idx}.in ====")

            # 加载测试集
            n = load_testcase(idx, testcase_dir=args.testdir, input_file=args.input)
            row = [n]

            # 每个算法执行
            for alg in algs:
                t, chk = run_algorithm_with_check(alg)
                row.append(t)
                row.append(chk)
                print(f"{alg}: time = {t:.6f}, check = {chk}")

            writer.writerow(row)

    print(f"\n[OK] CSV saved: {args.outcsv}")


if __name__ == "__main__":
    main()
