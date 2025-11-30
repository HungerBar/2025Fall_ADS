import csv

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit

# ===============================
# 1. 读取 CSV 数据
# ===============================
data_file = "DpBase100.csv"  # 替换为你的 CSV 文件路径

ns_all, sums_all, times_all = [], [], []

with open(data_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        ns_all.append(int(row["n"]))
        sums_all.append(int(row["sum"]))
        times_all.append(float(row["dp_time"]))

ns_all = np.array(ns_all)
sums_all = np.array(sums_all)
times_all = np.array(times_all)


# ===============================
# 2. 定义二元拟合函数 (n * sum^2)
# ===============================
def dp_model(xy, a, b):
    n, s = xy
    return a * n * (s**2) + b


# 拟合
popt, pcov = curve_fit(dp_model, (ns_all, sums_all), times_all)
a, b = popt

# 计算预测值和拟合优度指标
times_pred = dp_model((ns_all, sums_all), a, b)
ss_res = np.sum((times_all - times_pred) ** 2)
ss_tot = np.sum((times_all - np.mean(times_all)) ** 2)
r2 = 1 - (ss_res / ss_tot)
rmse = np.sqrt(np.mean((times_all - times_pred) ** 2))
mae = np.mean(np.abs(times_all - times_pred))

# ===============================
# 3. 创建新的布局设计
# ===============================
# 创建图形和子图布局
fig = plt.figure(figsize=(16, 10))

# 使用GridSpec创建更复杂的布局
gs = plt.GridSpec(
    2, 2, width_ratios=[1, 1.2], height_ratios=[1, 0.1], hspace=0.05, wspace=0.1
)

# 3D图占据主要区域
ax_3d = fig.add_subplot(gs[:, 0], projection="3d")

# 信息面板放在右侧
ax_info = fig.add_subplot(gs[0, 1])
ax_info.axis("off")  # 隐藏坐标轴

# 可选：添加残差图在右下角
# ax_residual = fig.add_subplot(gs[1, 1])
# ax_residual.axis('off')

# ===============================
# 4. 绘制3D散点图和拟合曲面
# ===============================
# 散点图
sc = ax_3d.scatter(
    ns_all,
    sums_all,
    times_all,
    c=times_all,
    cmap="plasma",
    s=40,
    alpha=0.8,
    depthshade=True,
)

# 曲面拟合
n_lin = np.linspace(ns_all.min(), ns_all.max(), 30)
s_lin = np.linspace(sums_all.min(), sums_all.max(), 30)
N, S = np.meshgrid(n_lin, s_lin)
T_fit = dp_model((N, S), a, b)

# 绘制拟合曲面
surf = ax_3d.plot_surface(
    N, S, T_fit, cmap="viridis", alpha=0.6, rstride=1, cstride=1, antialiased=True
)

# 设置3D图标签和标题
ax_3d.set_xlabel("n", fontsize=12, labelpad=10)
ax_3d.set_ylabel("sum", fontsize=12, labelpad=10)
ax_3d.set_zlabel("Time (seconds)", fontsize=12, labelpad=10)
ax_3d.set_title("3D Visualization of DP Algorithm Performance", fontsize=14, pad=20)

# 设置更好的视角
ax_3d.view_init(elev=25, azim=45)

# 添加颜色条
cbar = plt.colorbar(sc, ax=ax_3d, shrink=0.6, aspect=20, pad=0.1)
cbar.set_label("Time (seconds)", fontsize=11)

# ===============================
# 5. 设计信息面板
# ===============================
# 创建专业的信息面板布局
info_text = f"""
FITTED MODEL
T = a·n·sum² + b

PARAMETERS
a = {a:.2e}
b = {b:.2e}

GOODNESS-OF-FIT
R² = {r2:.4f}
RMSE = {rmse:.4f} s
MAE = {mae:.4f} s

DATASET
N = {len(ns_all)} data points
n ∈ [{ns_all.min()}, {ns_all.max()}]
sum ∈ [{sums_all.min()}, {sums_all.max()}]
"""

# 添加信息面板文本
ax_info.text(
    0.05,
    0.95,
    info_text,
    transform=ax_info.transAxes,
    fontfamily="sans-serif",
    fontsize=11,
    verticalalignment="top",
    linespacing=1.8,
    bbox=dict(
        boxstyle="round,pad=0.8",
        facecolor="whitesmoke",
        alpha=0.9,
        edgecolor="gray",
        linewidth=1,
    ),
)

# 添加图例说明
legend_elements = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="blue",
        markersize=8,
        label="Actual Data Points",
    ),
    Patch(facecolor="green", alpha=0.6, label="Fitted Surface\n(O(n·sum²))"),
]

ax_info.legend(
    handles=legend_elements,
    loc="lower left",
    bbox_to_anchor=(0.05, 0.05),
    framealpha=0.9,
    facecolor="white",
    edgecolor="black",
)

# ===============================
# 6. 可选：添加残差分析面板
# ===============================
# 如果需要残差分析，可以取消注释以下代码
"""
ax_residual = fig.add_subplot(gs[1, 1])
residuals = times_all - times_pred
ax_residual.scatter(times_pred, residuals, alpha=0.6, color='red')
ax_residual.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax_residual.set_xlabel('Predicted Time (s)')
ax_residual.set_ylabel('Residuals')
ax_residual.set_title('Residual Analysis', fontsize=12)
ax_residual.grid(True, alpha=0.3)
"""

# ===============================
# 7. 添加整体标题和美化
# ===============================
fig.suptitle(
    "Dynamic Programming Algorithm Complexity Analysis",
    fontsize=16,
    fontweight="bold",
    y=0.98,
)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig(
    "dp_analysis_improved_layout.png", dpi=300, bbox_inches="tight", facecolor="white"
)

plt.show()

# ===============================
# 8. 控制台输出详细信息
# ===============================
print("\n" + "=" * 70)
print("DYNAMIC PROGRAMMING ALGORITHM ANALYSIS".center(70))
print("=" * 70)
print(f"Model: T = {a:.2e}·n·sum² + {b:.2e}")
print(
    f"Dataset: {len(ns_all)} points, n∈[{ns_all.min()},{ns_all.max()}], sum∈[{sums_all.min()},{sums_all.max()}]"
)
print(f"Goodness-of-fit: R²={r2:.4f}, RMSE={rmse:.4f}s, MAE={mae:.4f}s")
print("=" * 70)
