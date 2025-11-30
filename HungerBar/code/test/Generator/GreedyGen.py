import csv
import os
import random
from datetime import datetime

# =============================================
# 配置参数
# =============================================
NUM_GUARANTEED_INPUTS = 1000  # 测试用例数量
N_LARGE = 1000  # 数组长度
NUM_BUCKETS = 3  # 桶数量
MIN_VALUE = 1
MAX_VALUE = 10**6
OUTPUT_DIR = "testcases"
OUTPUT_CSV = "guaranteed_inputs.csv"


# =============================================
# 数据生成函数（保证有解）
# =============================================
def gen_guaranteed_solution_data(n=N_LARGE, num_buckets=NUM_BUCKETS):
    """生成可以被 num_buckets 平衡的数组"""
    if n < num_buckets:
        raise ValueError("数组长度必须 >= 桶数量")

    arr = []
    bucket_sums = [0] * num_buckets
    bucket_elements = [[] for _ in range(num_buckets)]

    # 随机生成目标桶和
    min_target = MIN_VALUE * (n // num_buckets)
    max_target = MAX_VALUE * (n // num_buckets)
    target_sum = random.randint(min_target, max_target)

    # 每个桶目标和
    bucket_targets = [target_sum] * num_buckets

    # 生成 n - num_buckets 个随机数
    for _ in range(n - num_buckets):
        min_index = bucket_sums.index(min(bucket_sums))
        remaining_numbers = n - len(arr) - num_buckets
        remaining_sum = bucket_targets[min_index] - bucket_sums[min_index]

        lower = max(MIN_VALUE, remaining_sum - remaining_numbers * MAX_VALUE)
        upper = min(MAX_VALUE, remaining_sum - remaining_numbers * MIN_VALUE)
        if lower > upper:
            lower, upper = MIN_VALUE, MAX_VALUE

        num = random.randint(lower, upper)
        bucket_sums[min_index] += num
        bucket_elements[min_index].append(num)
        arr.append(num)

    # 补齐每个桶，使桶和等于 target_sum
    for i in range(num_buckets):
        correction = bucket_targets[i] - bucket_sums[i]
        correction = max(MIN_VALUE, min(MAX_VALUE, correction))
        bucket_sums[i] += correction
        bucket_elements[i].append(correction)
        arr.append(correction)

    # 打乱数组
    random.shuffle(arr)

    # 最后检查总和是否可被 num_buckets 整除
    total_sum = sum(arr)
    remainder = total_sum % num_buckets
    if remainder != 0:
        arr[-1] -= remainder
        arr[-1] = max(MIN_VALUE, min(MAX_VALUE, arr[-1]))

    assert sum(arr) % num_buckets == 0
    return arr, target_sum


# =============================================
# 写入 input_i.txt
# =============================================
def write_input(arr, idx):
    filename = os.path.join(OUTPUT_DIR, f"sa_{idx+1}.in")
    with open(filename, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")
    return filename


# =============================================
# 主流程
# =============================================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

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
                print(f"[OK] 生成实例 {i+1}: 文件 {filename}")
            except Exception as e:
                print(f"[ERROR] 生成实例 {i+1} 出错: {e}")


if __name__ == "__main__":
    main()
