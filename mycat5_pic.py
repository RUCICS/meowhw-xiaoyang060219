import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# 使用无头后端
matplotlib.use('Agg')  # 关键设置 - 使用非交互式后端

# 指定Noto Sans CJK字体文件
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
plt.rcParams["font.family"] = ["SimHei", matplotlib.font_manager.FontProperties(fname=font_path).get_name()]
# 实验数据
data = {
    'Buffer Size (bytes)': [4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304],
    'Transfer Rate (MB/s)': [6033.33, 9833.33, 17733.33, 25233.33, 19900.00, 21833.33, 22166.66, 23100.00, 21466.66, 14433.33, 14000.00]
}

df = pd.DataFrame(data)

# 绘制结果图表
plt.figure(figsize=(12, 8))
plt.plot(df['Buffer Size (bytes)'], df['Transfer Rate (MB/s)'], 'o-', linewidth=2, markersize=8, color='royalblue')

# 设置图表标题和标签
plt.title("缓冲区大小与传输速率关系", fontsize=16)
plt.xlabel("缓冲区大小 (字节)", fontsize=14)
plt.ylabel("传输速率 (MB/s)", fontsize=14)

# 设置对数坐标轴
plt.xscale('log', base=2)
plt.xticks([4096 * 2**i for i in range(0, 11)], 
           [f"{4096 * 2**i}" for i in range(0, 11)], rotation=45)

# 添加网格线
plt.grid(True, which="both", ls="--", alpha=0.5)

# 标记性能峰值
peak_idx = df['Transfer Rate (MB/s)'].idxmax()
peak_bs = df.loc[peak_idx, 'Buffer Size (bytes)']
peak_rate = df.loc[peak_idx, 'Transfer Rate (MB/s)']
plt.axvline(x=peak_bs, color='r', linestyle='--', alpha=0.7)
plt.axhline(y=peak_rate, color='r', linestyle='--', alpha=0.7)

# 标记性能拐点
threshold = peak_rate * 0.95  # 95%最大性能
optimal_row = df[df['Transfer Rate (MB/s)'] >= threshold].iloc[0]
plt.axvline(x=optimal_row['Buffer Size (bytes)'], color='g', linestyle='--', alpha=0.7)
plt.axhline(y=threshold, color='g', linestyle='--', alpha=0.7)

# 添加标记
plt.annotate(f"峰值性能: {peak_rate:.2f} MB/s\n@ {peak_bs} 字节",
             xy=(peak_bs, peak_rate),
             xytext=(peak_bs * 0.7, peak_rate * 0.9),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.annotate(f"最佳缓冲区大小: {optimal_row['Buffer Size (bytes)']} 字节\n"
             f"达到 {optimal_row['Transfer Rate (MB/s)']/peak_rate*100:.1f}% 峰值性能",
             xy=(optimal_row['Buffer Size (bytes)'], optimal_row['Transfer Rate (MB/s)']),
             xytext=(optimal_row['Buffer Size (bytes)'] * 1.5, peak_rate * 0.7),
             arrowprops=dict(facecolor='black', shrink=0.05))

# 保存图像到文件
plt.tight_layout()
plt.savefig('bs_performance.png', dpi=300)
print("图表已保存为 'bs_performance.png'")

# 计算最佳缓冲区大小和优化倍数
base_size = 4096
optimal_bs = optimal_row['Buffer Size (bytes)']
optimal_multiplier = optimal_bs // base_size

print(f"\n实验分析结论:")
print(f"1. 峰值传输速率: {peak_rate:.2f} MB/s @ {peak_bs} 字节")
print(f"2. 最佳缓冲区大小: {optimal_bs} 字节")
print(f"3. 相当于内存页大小({base_size}字节)的 {optimal_multiplier} 倍")
print(f"4. 达到峰值性能的 {optimal_row['Transfer Rate (MB/s)']/peak_rate*100:.1f}%")
print(f"\n在 mycat5.c 中使用以下定义:")
print(f"#define OPTIMAL_MULTIPLIER {optimal_multiplier}")
