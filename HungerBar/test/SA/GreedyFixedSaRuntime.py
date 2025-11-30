import csv
import os
import random
import subprocess
from datetime import datetime

# =============================================
# 配置参数
# =============================================
NUM_GUARANTEED_INPUTS = 100  # 生成测试用例数量
N_LARGE = 1000  # 数组长度
NUM_BUCKETS = 3  # 桶数量
MIN_VALUE = 1
MAX_VALUE = 10**6
K_MAX = 10  # SA 最大重启次数
OUTPUT_CSV = "sa_guaranteed_solution_test.csv"


# =============================================
# 数据生成函数（严格保证有解）
# =============================================


def gen_guaranteed_solution_data(n=N_LARGE, num_buckets=NUM_BUCKETS):
    """
    生成可以被 num_buckets 桶平衡的数组。
    保证每个数字在 [MIN_VALUE, MAX_VALUE] 范围内
    严格保证总和可被 num_buckets 整除
    """
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
        # 严格保证 correction 不越界
        if correction < MIN_VALUE:
            correction = MIN_VALUE
        elif correction > MAX_VALUE:
            correction = MAX_VALUE
        bucket_sums[i] += correction
        bucket_elements[i].append(correction)
        arr.append(correction)

    # 打乱数组
    random.shuffle(arr)

    # 最后检查总和是否可被 num_buckets 整除
    total_sum = sum(arr)
    if total_sum % num_buckets != 0:
        # 做微调：把最后 num_buckets 个元素调整成桶平衡
        remainder = total_sum % num_buckets
        arr[-1] -= remainder
        # 再保证元素仍在 [MIN_VALUE, MAX_VALUE] 范围
        if arr[-1] < MIN_VALUE:
            arr[-1] = MIN_VALUE
        elif arr[-1] > MAX_VALUE:
            arr[-1] = MAX_VALUE

    # 最终断言保证可以三分
    assert sum(arr) % num_buckets == 0

    return arr, target_sum


# =============================================
# 工具函数
# =============================================
def write_input(arr, filename="input.txt"):
    with open(filename, "w") as f:
        f.write(f"{len(arr)}\n")
        f.write(" ".join(map(str, arr)) + "\n")


def run_sa():
    result = subprocess.run(
        ["./sa_greedy.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.returncode


def run_check_correct():
    try:
        proc = subprocess.Popen(
            ["./check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = proc.communicate(timeout=30)
        output = stdout.strip()
        return output == "Correct", output
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_single_instance(instance_id):
    """生成一个测试用例并运行SA，最多尝试 K_MAX 次"""
    arr, target_sum = gen_guaranteed_solution_data()
    write_input(arr, "input.txt")

    first_success = -1
    success_flag = False
    for k in range(1, K_MAX + 1):
        sa_result = run_sa()
        if sa_result != 0:
            continue
        ok, _ = run_check_correct()
        if ok:
            first_success = k
            success_flag = True
            break

    return {
        "instance_id": instance_id,
        "array_length": len(arr),
        "target_sum": target_sum,
        "min_value": min(arr),
        "max_value": max(arr),
        "average_value": sum(arr) / len(arr),
        "first_success_restart": first_success,
        "success_flag": success_flag,
    }


def write_single_result(result, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                [
                    "instance_id",
                    "array_length",
                    "target_sum",
                    "min_value",
                    "max_value",
                    "average_value",
                    "first_success_restart",
                    "success_flag",
                    "timestamp",
                ]
            )
        writer.writerow(
            [
                result["instance_id"],
                result["array_length"],
                result["target_sum"],
                result["min_value"],
                result["max_value"],
                result["average_value"],
                result["first_success_restart"],
                result["success_flag"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )


# =============================================
# 主流程
# =============================================
def main():
    print(f"=== 开始生成并测试 {NUM_GUARANTEED_INPUTS} 个实例 ===")
    os.makedirs(
        os.path.dirname(OUTPUT_CSV) if os.path.dirname(OUTPUT_CSV) else ".",
        exist_ok=True,
    )

    for instance_id in range(NUM_GUARANTEED_INPUTS):
        try:
            result = test_single_instance(instance_id)
            write_single_result(result, OUTPUT_CSV)
            print(
                f"实例 {instance_id + 1}: "
                f"{'成功' if result['success_flag'] else '失败'}, "
                f"首次成功重启: {result['first_success_restart']}"
            )
        except Exception as e:
            print(f"实例 {instance_id + 1} 出错: {e}")


if __name__ == "__main__":
    main()
