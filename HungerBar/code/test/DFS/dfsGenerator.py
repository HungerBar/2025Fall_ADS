import argparse
import os
import random


# ============================================================
# 生成更难剪枝的 DFS 测试数据
# ============================================================
def gen_hard_dfs_data(n, case_idx, maxv=2000, file_path="input.txt"):
    """
    尽量破坏 DFS 的降序排序 & 空桶剪枝，生成测试数据并保存到指定路径。
    case_idx: 用例序号（第几个用例）
    """
    base = [random.randint(maxv // 3, maxv // 2) for _ in range(n)]
    arr = [v + random.randint(-3, 3) for v in base]
    random.shuffle(arr)

    # 确保父目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    print(
        f"[OK] 第{case_idx}个用例: n={n}, 路径={file_path}, 数值范围=({min(arr)}, {max(arr)})"
    )


# ============================================================
# 主流程（仅生成测试数据）
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="生成DFS测试数据到testcases目录（按序号命名）"
    )

    parser.add_argument(
        "--ns",
        nargs="+",
        required=True,
        type=int,
        help="输入规模列表，例：--ns 10 20 30",
    )
    parser.add_argument(
        "--output-dir", default="testcases", help="数据输出目录（默认：testcases）"
    )
    parser.add_argument(
        "--maxv", type=int, default=2000, help="数值最大值（默认：2000）"
    )

    args = parser.parse_args()

    # 按序号生成文件（input1.txt、input2.txt...）
    for case_idx, n in enumerate(args.ns, start=1):
        file_name = f"dfs{case_idx}.in"  # 用例序号作为文件名后缀
        file_path = os.path.join(args.output_dir, file_name)
        gen_hard_dfs_data(n, case_idx, maxv=args.maxv, file_path=file_path)

    print(f"\n[完成] 所有数据已生成到 {args.output_dir} 目录！")


if __name__ == "__main__":
    main()
