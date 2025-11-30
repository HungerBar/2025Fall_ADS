import argparse
import os
import random

# Default parameters
DEFAULT_VALUE_MEAN = 100
DEFAULT_VALUE_NOISE = 20


# Generate array whose sum is divisible by 3
def gen_data_div3(n):
    """
    Generate an array of n positive integers such that:
    1. Each element is roughly around [DEFAULT_VALUE_MEAN - DEFAULT_VALUE_NOISE, DEFAULT_VALUE_MEAN + DEFAULT_VALUE_NOISE].
    2. The sum of the array is divisible by 3.
    3. Elements are shuffled to remove obvious order.
    """
    arr = [
        max(
            1,
            DEFAULT_VALUE_MEAN
            + random.randint(-DEFAULT_VALUE_NOISE, DEFAULT_VALUE_NOISE),
        )
        for _ in range(n - 1)
    ]
    sum_so_far = sum(arr)
    remainder = sum_so_far % 3
    if remainder == 0:
        last_val = max(
            1,
            DEFAULT_VALUE_MEAN
            + random.randint(-DEFAULT_VALUE_NOISE, DEFAULT_VALUE_NOISE),
        )
    else:
        last_val = max(
            1,
            DEFAULT_VALUE_MEAN
            + random.randint(-DEFAULT_VALUE_NOISE, DEFAULT_VALUE_NOISE)
            + (3 - remainder),
        )
    arr.append(last_val)
    random.shuffle(arr)
    return arr


def write_input(arr, file_path):
    """
    Write array to file:
    n
    a1 a2 ... an
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate DP testcases with sum divisible by 3"
    )
    parser.add_argument(
        "--n_list",
        type=int,
        nargs="+",
        required=True,
        help="List of n values to generate, e.g., --n_list 50 100 150",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Number of testcases per n",
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
        for _ in range(args.trials):
            arr = gen_data_div3(n)
            filename = os.path.join(args.output_dir, f"dp3_{idx}.in")
            write_input(arr, filename)
            print(
                f"[OK] Generated {filename}: n={n}, sum={sum(arr)}, range=({min(arr)}, {max(arr)})"
            )
            idx += 1


if __name__ == "__main__":
    main()
