import csv
import os
import random
from datetime import datetime

NUM_GUARANTEED_INPUTS = 1000  # Number of test cases to generate
N_LARGE = 1000  # Array length
NUM_BUCKETS = 3  # Number of buckets (partitions)
MIN_VALUE = 1
MAX_VALUE = 10**6
OUTPUT_DIR = "testcases"
OUTPUT_CSV = "guaranteed_inputs.csv"


# Data generation function (guaranteed solution)
def gen_guaranteed_solution_data(n=N_LARGE, num_buckets=NUM_BUCKETS):
    """
    Generate an array that can be evenly partitioned into `num_buckets` buckets.

    Logic:
    1. Randomly determine a target sum for each bucket.
    2. Distribute n - num_buckets elements among the buckets randomly.
    3. Add correction elements to each bucket to reach the target sum.
    4. Shuffle the array to remove obvious order.
    5. Ensure total sum is divisible by `num_buckets`.

    Returns:
        arr (list[int]): Generated array
        target_sum (int): Target sum for each bucket
    """
    if n < num_buckets:
        raise ValueError("Array length must be >= number of buckets")

    arr = []
    bucket_sums = [0] * num_buckets
    bucket_elements = [[] for _ in range(num_buckets)]

    # Randomly generate target sum for each bucket
    min_target = MIN_VALUE * (n // num_buckets)
    max_target = MAX_VALUE * (n // num_buckets)
    target_sum = random.randint(min_target, max_target)

    # Each bucket's target sum
    bucket_targets = [target_sum] * num_buckets

    # Generate n - num_buckets random numbers and distribute to buckets
    for _ in range(n - num_buckets):
        # Choose the bucket with the smallest current sum
        min_index = bucket_sums.index(min(bucket_sums))
        remaining_numbers = n - len(arr) - num_buckets
        remaining_sum = bucket_targets[min_index] - bucket_sums[min_index]

        # Compute feasible range for the next number
        lower = max(MIN_VALUE, remaining_sum - remaining_numbers * MAX_VALUE)
        upper = min(MAX_VALUE, remaining_sum - remaining_numbers * MIN_VALUE)
        if lower > upper:
            lower, upper = MIN_VALUE, MAX_VALUE

        num = random.randint(lower, upper)
        bucket_sums[min_index] += num
        bucket_elements[min_index].append(num)
        arr.append(num)

    # Add correction elements to reach target sum in each bucket
    for i in range(num_buckets):
        correction = bucket_targets[i] - bucket_sums[i]
        correction = max(MIN_VALUE, min(MAX_VALUE, correction))
        bucket_sums[i] += correction
        bucket_elements[i].append(correction)
        arr.append(correction)

    # Shuffle the array to remove ordering
    random.shuffle(arr)

    # Ensure total sum is divisible by num_buckets
    total_sum = sum(arr)
    remainder = total_sum % num_buckets
    if remainder != 0:
        arr[-1] -= remainder
        arr[-1] = max(MIN_VALUE, min(MAX_VALUE, arr[-1]))

    # Safety check
    assert sum(arr) % num_buckets == 0
    return arr, target_sum


def write_input(arr, idx):
    filename = os.path.join(OUTPUT_DIR, f"sa_{idx+1}.in")
    with open(filename, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")
    return filename


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Open CSV to record metadata for all test cases
    with open(OUTPUT_CSV, "w", newline="") as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(
            [
                "instance_id",
                "array_length",
                "target_sum",
                "min_value",
                "max_value",
                "average_value",
                "filename",
                "timestamp",
            ]
        )

        for i in range(NUM_GUARANTEED_INPUTS):
            try:
                arr, target_sum = gen_guaranteed_solution_data()
                filename = write_input(arr, i)
                # Write metadata to CSV
                writer.writerow(
                    [
                        i,
                        len(arr),
                        target_sum,
                        min(arr),
                        max(arr),
                        sum(arr) / len(arr),
                        filename,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                )
                print(f"[OK] Generated instance {i+1}: file {filename}")
            except Exception as e:
                print(f"[ERROR] Failed to generate instance {i+1}: {e}")


if __name__ == "__main__":
    main()
