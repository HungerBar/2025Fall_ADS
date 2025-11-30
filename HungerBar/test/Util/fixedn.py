import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# ==============================
# 1. 读取数据
# ==============================
df = pd.read_csv("dp_fixedn_results.csv")  # 替换为你的 CSV 文件路径

# 只保留正确解
df = df[df["correct"] == True]

# ==============================
# 2. 聚合统计
# ==============================
# 计算每个 total_sum 对应的平均时间、最小、最大和方差
summary = (
    df.groupby("total_sum")["dp_time"].agg(["mean", "min", "max", "var"]).reset_index()
)
print(summary)


# ==============================
# 3. 时间复杂度拟合
# ==============================
# 常见复杂度模型
def f_linear(s, a, b):
    return a * s + b


def f_nlogn(s, a, b):
    return a * s * np.log2(s) + b


def f_n2(s, a, b):
    return a * s**2 + b


models = {"O(n)": f_linear, "O(n log n)": f_nlogn, "O(n^2)": f_n2}

x = summary["total_sum"].values
y = summary["mean"].values

best_model = None
best_params = None
best_mse = float("inf")

for name, fn in models.items():
    try:
        popt, _ = curve_fit(fn, x, y)
        mse = np.mean((fn(x, *popt) - y) ** 2)
        print(f"{name} MSE: {mse:.6e}")
        if mse < best_mse:
            best_mse = mse
            best_model = name
            best_params = popt
    except Exception as e:
        print(f"{name} fit error: {e}")

print(f"\nBest fit: {best_model} with params {best_params}")

# ==============================
# 4. 可视化
# ==============================
plt.figure(figsize=(10, 6))
plt.errorbar(
    summary["total_sum"],
    summary["mean"],
    yerr=np.sqrt(summary["var"]),
    fmt="o",
    label="DP mean ± std",
)
# 绘制拟合曲线
if best_model is not None:
    s_fit = np.linspace(x.min(), x.max(), 500)
    plt.plot(
        s_fit,
        models[best_model](s_fit, *best_params),
        "-",
        label=f"Fitted {best_model}",
    )

plt.xlabel("Total Sum")
plt.ylabel("DP Time (s)")
plt.title("DP Time vs Total Sum")
plt.legend()
plt.grid(True)
plt.savefig("dp_time_vs_sum.png", dpi=200)
plt.show()
