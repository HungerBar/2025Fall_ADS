import os
import random
import subprocess
from copy import deepcopy

N_SMALL = 100  # base set elements quantity
NUM_BASE_GROUPS = 20  # base set quantity
MIN_SELECTED_GROUPS = 10  # min base quantity 
NUM_LARGE_INPUTS = 10000

SMALL_MAX = 300  # base set max element
POWER_MIN = 1
POWER_MAX = 6

OUTPUT_DIR = "testcases"  # save directory


# generate small element
def gen_small_data(n=N_SMALL):
    return [random.randint(1, SMALL_MAX) for _ in range(n)]


def write_input(arr, filename):
    arr_shuffled = deepcopy(arr)
    random.shuffle(arr_shuffled)
    with open(filename, "w") as f:
        f.write(f"{len(arr_shuffled)}\n")
        f.write(" ".join(map(str, arr_shuffled)) + "\n")
    print(f"[OK] {filename}: n={len(arr_shuffled)}, sum={sum(arr_shuffled)}")


# run and check the base
def run_dp_then_check_correct():
    if not os.path.exists("./dp") or not os.path.exists("./check"):
        raise FileNotFoundError("./dp or ./check not found")

    subprocess.run(["./dp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc = subprocess.Popen(["./check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    output = stdout.decode().strip()
    return output == "Correct"


# generate the base
def generate_base_groups():
    base_groups = []
    print("=== 生成基础基组（保证可解） ===")
    for i in range(NUM_BASE_GROUPS):
        attempt = 0
        while True:
            attempt += 1
            arr = gen_small_data()
            # use check
            write_input(arr, "input.txt")
            if run_dp_then_check_correct():
                # 保存基础组文件
                filename = os.path.join(OUTPUT_DIR, f"base_{i+1}.txt")
                write_input(arr, filename)
                base_groups.append(arr)
                print(f"[Base {i+1}] 成功生成，尝试次数 {attempt}")
                break
            if attempt % 50 == 0:
                print(f"[Base {i+1}] 已尝试 {attempt} 次，继续中...")
    return base_groups


# combine the bases to build BIG input
def generate_large_inputs(base_groups):
    print(f"\n=== 生成 {NUM_LARGE_INPUTS} 个大输入 ===")
    large_inputs = []
    for idx in range(NUM_LARGE_INPUTS):
        num_sel = random.randint(MIN_SELECTED_GROUPS, NUM_BASE_GROUPS)
        selected = random.sample(range(NUM_BASE_GROUPS), num_sel)

        large_arr = []
        power_list = []
        for g in selected:
            power = random.randint(POWER_MIN, POWER_MAX)
            factor = random.randint(1, 7**power)
            scaled = [x * factor for x in base_groups[g]]
            large_arr.extend(scaled)
            power_list.append(power)

        filename = os.path.join(OUTPUT_DIR, f"sa1_{idx+1}.in")
        write_input(large_arr, filename)

        large_inputs.append((large_arr, selected, power_list))
    return large_inputs


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # generate bases
    base_groups = generate_base_groups()
    # generate Input
    _ = generate_large_inputs(base_groups)

    print("\n=== 所有测试集生成完毕 ===")
    print(f"测试集文件保存在 {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
