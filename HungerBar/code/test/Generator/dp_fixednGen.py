import argparse
import os
import random


# =====================================================
#              Test Data Generation
# =====================================================
def gen_test_data_fixed_sum(n, total_sum, min_val=1, max_val=None, file="input.txt"):
    """
    Generate n positive integers whose sum equals total_sum
    Optionally, each number is in [min_val, max_val]
    """
    if max_val is None:
        max_val = total_sum - n + 1  # max possible if min_val=1

    if n * min_val > total_sum or n * max_val < total_sum:
        raise ValueError("Impossible to generate numbers with given sum and bounds.")

    # Start with n minimum values
    arr = [min_val] * n
    remaining = total_sum - n * min_val

    # Randomly distribute remaining sum
    for i in range(n):
        if remaining <= 0:
            break
        add = min(remaining, max_val - arr[i])
        val = random.randint(0, add)
        arr[i] += val
        remaining -= val

    # Distribute any remaining sum
    while remaining > 0:
        i = random.randint(0, n - 1)
        if arr[i] < max_val:
            arr[i] += 1
            remaining -= 1

    random.shuffle(arr)

    # Write to input file
    with open(file, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, arr)) + "\n")

    actual_sum = sum(arr)
    assert actual_sum == total_sum, f"Sum mismatch: {actual_sum} != {total_sum}"
    print(
        f"[OK] Test data generated: {file}, n={n}, sum={total_sum}, range=({min(arr)}, {max(arr)})"
    )
    return arr


# =====================================================
#                         Main
# =====================================================
def main():
    parser = argparse.ArgumentParser(
        description="Generate test cases with fixed n and total_sum"
    )
    parser.add_argument("--n", type=int, required=True, help="Number of items")
    parser.add_argument(
        "--sums", type=int, nargs="+", required=True, help="Total sums to generate"
    )
    parser.add_argument(
        "--trials", type=int, default=1, help="Number of test cases per total_sum"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="testcases",
        help="Directory to save test cases",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    idx = 1
    for total_sum in args.sums:
        for trial in range(args.trials):
            filename = os.path.join(args.output_dir, f"dp1_{idx}.in")
            try:
                gen_test_data_fixed_sum(n=args.n, total_sum=total_sum, file=filename)
            except Exception as e:
                print(f"[ERROR] Data generation failed for total_sum={total_sum}: {e}")
            idx += 1


if __name__ == "__main__":
    main()
