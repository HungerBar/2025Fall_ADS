import csv

INPUT_CSV = "sa_guaranteed_solution_test.csv"

total_instances = 0
fail_count = 0
success_restart_sum = 0
success_count = 0

with open(INPUT_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_instances += 1
        success_flag = row["success_flag"].strip().lower() == "true"
        if not success_flag:
            fail_count += 1
        else:
            first_restart = int(row["first_success_restart"])
            success_restart_sum += first_restart
            success_count += 1

# 输出结果
print(f"总实例数: {total_instances}")
print(f"失败实例数: {fail_count}")
if success_count > 0:
    avg_restart = success_restart_sum / success_count
    print(f"成功实例平均首次重启次数: {avg_restart:.2f}")
else:
    print("没有成功的实例")
