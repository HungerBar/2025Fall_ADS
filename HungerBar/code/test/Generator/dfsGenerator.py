import argparse
import os
import random


# build difficult test data for DFS
def gen_hard_dfs_data(n, case_idx, maxv=2000, file_path="input.txt"):
    """
    * The numerical values are concentrated in a very narrow range `[maxv/3, maxv/2] ± 3`.
    * Shuffle the order to break the sorted-order pruning.
    * The differences between buckets are very small, which breaks the empty-bucket pruning.
    """
    base = [random.randint(maxv // 3, maxv // 2) for _ in range(n)]
    arr = [v + random.randint(-3, 3) for v in base]
    random.shuffle(arr)

    # check
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    print(
        f"[OK] 第{case_idx}个用例: n={n}, 路径={file_path}, 数值范围=({min(arr)}, {max(arr)})"
    )


def main():
    parser = argparse.ArgumentParser(
        description="生成 DFS 剪枝压力测试数据（dfsi.in 命名）"
    )

    parser.add_argument(
        "--ns",
        nargs="+",
        required=True,
        type=int,
        help="输入规模列表，例如：--ns 10 20 30",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="每个规模重复生成多少份（默认：1）",
    )
    parser.add_argument(
        "--output-dir", default="testcases", help="数据输出目录（默认：testcases）"
    )
    parser.add_argument(
        "--maxv", type=int, default=2000, help="数值最大值（默认：2000）"
    )

    args = parser.parse_args()

    global_case_idx = 1

    # repeat x
    for n in args.ns:
        for _ in range(args.repeat):

            file_name = f"dfs{global_case_idx}.in"
            file_path = os.path.join(args.output_dir, file_name)

            gen_hard_dfs_data(
                n=n,
                case_idx=global_case_idx,
                maxv=args.maxv,
                file_path=file_path,
            )

            global_case_idx += 1

    print(f"\n[完成] 所有 DFS 测试数据已生成到目录：{args.output_dir}")


if __name__ == "__main__":
    main()
