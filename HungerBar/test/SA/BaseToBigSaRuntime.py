import csv
import random
import subprocess
from copy import deepcopy

# =============================================
# 配置参数（可调整）
# =============================================
N_SMALL = 100  # 小规模基数组长度
NUM_BASE_GROUPS = 20  # 基础组数量
MIN_SELECTED_GROUPS = 10  # large array 最少选多少组
NUM_LARGE_INPUTS = 100  # 大输入数量

SMALL_MAX = 300  # 小基组元素最大值
POWER_MIN = 1
POWER_MAX = 6
K_MAX = 10  # SA 最大重启次数

OUTPUT_CSV = "sa_restart_distribution.csv"


# =============================================
# 工具函数
# =============================================
def gen_small_data(n=N_SMALL):
    """生成小测试组"""
    return [random.randint(1, SMALL_MAX) for _ in range(n)]


def write_input(arr, filename="input.txt"):
    """
    写入 input.txt 或 inputi.txt，第一行写长度，第二行写打乱后的数组
    并打印第一行长度
    """
    arr_shuffled = arr.copy()
    random.shuffle(arr_shuffled)
    with open(filename, "w") as f:
        f.write(f"{len(arr_shuffled)}\n")
        f.write(" ".join(map(str, arr_shuffled)) + "\n")
    print(f"{filename} 第一行（长度）: {len(arr_shuffled)}")


def run_sa():
    """运行 SA，但不打印 stdout/stderr"""
    subprocess.run(["./sa"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def run_check_correct():
    """运行 ./check 并打印输出"""
    proc = subprocess.Popen(["./check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    output = stdout.decode().strip()
    err_output = stderr.decode().strip()

    print("=== ./check 输出 ===")
    print(output)
    if err_output:
        print("=== ./check 错误输出 ===")
        print(err_output)

    return output == "Correct", output


def run_dp_then_check_correct():
    """运行 DP 检查"""
    subprocess.run(["./dp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    correct, _ = run_check_correct()
    return correct


# =============================================
# 阶段 1：生成基础测试组
# =============================================
def generate_base_groups():
    base_groups = []
    print("=== 生成基础基组（保证 DP 可解） ===")
    for i in range(NUM_BASE_GROUPS):
        attempt = 0
        while True:
            attempt += 1
            arr = gen_small_data()
            # 保存独立文件 input1.txt ~ input20.txt
            write_input(arr, f"input{i+1}.txt")
            # 用于 DP 检查的临时文件 input.txt
            write_input(arr, "input.txt")
            if run_dp_then_check_correct():
                base_groups.append(deepcopy(arr))
                print(f"[Base {i+1}] 成功生成，尝试次数 {attempt}")
                break
            if attempt % 50 == 0:
                print(f"[Base {i+1}] 已尝试 {attempt} 次，继续中...")
    return base_groups


# =============================================
# 阶段 2：生成 large inputs
# =============================================
def generate_large_inputs(base_groups):
    print(f"\n=== 开始生成 {NUM_LARGE_INPUTS} 个大输入 ===")
    large_inputs = []
    for idx in range(NUM_LARGE_INPUTS):
        num_sel = random.randint(MIN_SELECTED_GROUPS, NUM_BASE_GROUPS)
        selected = random.sample(range(NUM_BASE_GROUPS), num_sel)

        large_arr = []
        power_list = []

        for g in selected:
            power = random.randint(POWER_MIN, POWER_MAX)
            factor = random.randint(
                1, 7**power
            )  # 随机倍数            power_list.append(power)
            scaled = [x * factor for x in base_groups[g]]
            large_arr.extend(scaled)

        random.shuffle(large_arr)
        large_inputs.append((large_arr, selected, power_list))

        if (idx + 1) % 100 == 0:
            print(f"  已生成 {idx+1}/{NUM_LARGE_INPUTS} 个")

    return large_inputs


# =============================================
# 阶段 3：SA 重启测试
# =============================================
def test_sa_restart_distribution(large_inputs):
    print("\n=== SA 重启测试开始 ===")
    results = []

    for i, (arr, selected_groups, power_list) in enumerate(large_inputs):
        write_input(arr, "input.txt")  # 每次覆盖 input.txt
        first_success = -1
        success_flag = False

        for k in range(1, K_MAX + 1):
            run_sa()  # 不打印输出
            ok, _ = run_check_correct()
            if ok:
                first_success = k
                success_flag = True
                break

        results.append([i, selected_groups, power_list, first_success, success_flag])

        if (i + 1) % 100 == 0:
            print(f"  测试进度：{i+1}/{NUM_LARGE_INPUTS}")

    return results


# =============================================
# 阶段 4：写入 CSV
# =============================================
def write_results(results):
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "instance_id",
                "selected_groups",
                "power_list",
                "first_success_restart",
                "success_flag",
            ]
        )
        writer.writerows(results)
    print(f"\n=== 所有结果已写入 {OUTPUT_CSV} ===")


# =============================================
# 主流程
# =============================================
def main():
    base_groups = generate_base_groups()
    large_inputs = generate_large_inputs(base_groups)
    results = test_sa_restart_distribution(large_inputs)
    write_results(results)


if __name__ == "__main__":
    main()
