import argparse
import os
import random


# =====================================================
#              Test Data Generation
# =====================================================
def gen_test_data_fixed_sum(n, total_sum, min_val=1, max_val=None, file="input.txt"):
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
    print(
        f"[OK] Generated {file}: n={n}, sum={total_sum}, range=({min(arr)}, {max(arr)})"
    )
    return arr


# =====================================================
#                         Main
# =====================================================
def main():
    parser = argparse.ArgumentParser(description="Generate DP testcases only")
    parser.add_argument(
        "--ns", type=int, nargs="+", required=True, help="List of n values"
    )
    parser.add_argument("--total_sum", type=int, default=100000, help="Fixed total sum")
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
    for n in args.ns:
        for trial in range(args.trials):
            filename = os.path.join(args.output_dir, f"dp2_{idx}.in")
            try:
                gen_test_data_fixed_sum(n=n, total_sum=args.total_sum, file=filename)
            except Exception as e:
                print(f"[ERROR] Failed for n={n}, trial={trial+1}: {e}")
            idx += 1


if __name__ == "__main__":
    main()
