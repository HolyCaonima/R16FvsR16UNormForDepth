import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# 计算R16F的精度步长(相邻可表示值之间的差值)
def fp16_precision(x):
    if x == 0:
        return 2**-24  # 最小的亚规格化数
    
    # 找到最接近的2的幂
    exponent = np.floor(np.log2(x))
    
    # 如果x在亚规格化范围内
    if exponent < -14:
        return 2**-24
    
    # 返回精度步长
    return 2**(exponent-10)

# 计算R16Unorm的精度步长
def unorm16_precision(x):
    return 1/65535.0

def main():
    print("计算R16F和R16Unorm精度差异...")
    
    # 生成测试点 - 使用对数尺度覆盖从极小值到1的范围
    x_values = np.logspace(-8, 0, 1000)  # 从10^-8到10^0的对数刻度
    
    # 计算每个点的精度
    fp16_precision_values = [fp16_precision(x) for x in x_values]
    unorm16_precision_values = [unorm16_precision(x) for x in x_values]
    
    # 计算精度比率 (Unorm16相对于FP16的比率，>1表示FP16更好)
    precision_ratio = [unorm/fp for fp, unorm in zip(fp16_precision_values, unorm16_precision_values)]
    
    # 查找R16F和R16Unorm精度相等的交叉点
    crossover_indices = [i for i in range(1, len(precision_ratio)) 
                         if (precision_ratio[i-1] > 1 and precision_ratio[i] < 1) or 
                            (precision_ratio[i-1] < 1 and precision_ratio[i] > 1)]
    
    crossover_points = []
    for idx in crossover_indices:
        crossover_points.append(x_values[idx])
    
    if crossover_points:
        print(f"精度交叉点: {', '.join([f'{x:.8f}' for x in crossover_points])}")
    
    # 创建图表
    plt.figure(figsize=(12, 10))
    
    # 1. 绘制精度图 (对数-对数尺度)
    plt.subplot(3, 1, 1)
    plt.loglog(x_values, fp16_precision_values, 'b-', label='R16F精度')
    plt.loglog(x_values, unorm16_precision_values, 'r-', label='R16Unorm精度')
    plt.grid(True, which="both", ls="-")
    plt.ylabel('精度步长 (越小越好)')
    plt.title('R16F vs R16Unorm 精度步长比较 (对数尺度)')
    plt.legend()
    
    # 2. 绘制精度图 (线性-对数尺度)
    plt.subplot(3, 1, 2)
    plt.semilogx(x_values, fp16_precision_values, 'b-', label='R16F精度')
    plt.semilogx(x_values, unorm16_precision_values, 'r-', label='R16Unorm精度')
    plt.grid(True, which="both", ls="-")
    plt.ylabel('精度步长 (越小越好)')
    plt.title('R16F vs R16Unorm 精度步长比较 (半对数尺度)')
    plt.legend()
    
    # 3. 绘制比率图
    plt.subplot(3, 1, 3)
    plt.semilogx(x_values, precision_ratio, 'g-')
    plt.axhline(y=1, color='k', linestyle='--')
    
    # 标记交叉点
    for x in crossover_points:
        plt.axvline(x=x, color='r', linestyle='--', alpha=0.5)
        idx = np.abs(x_values - x).argmin()
        plt.text(x, precision_ratio[idx] * 1.1, f'{x:.6f}', 
                 rotation=90, verticalalignment='bottom')
    
    plt.grid(True, which="both", ls="-")
    plt.xlabel('深度值')
    plt.ylabel('精度比率 (R16Unorm步长/R16F步长)')
    plt.title('精度比率: 值>1表示R16F比R16Unorm更精确')
    
    # 添加注释解释
    plt.figtext(0.5, 0.01, 
                '结论: 在较小值区域 (约<0.01), R16F提供更高精度\n'
                '这解释了为什么在SSAO中, 聚焦于近处物体的深度差异时, R16F效果更好',
                ha='center', fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    
    # 优化布局
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('depth_precision_comparison.png', dpi=150)
    print("图表已保存为 'depth_precision_comparison.png'")
    plt.show()
    
    # 打印关键区域的数值比较
    print("\n关键深度值区域精度比较:")
    key_depths = [0.0001, 0.001, 0.01, 0.1, 0.5]
    print(f"{'深度值':<10} {'R16F精度':<15} {'R16Unorm精度':<15} {'优势比率':<10} {'更好格式'}")
    print("-" * 65)
    
    for depth in key_depths:
        fp_prec = fp16_precision(depth)
        unorm_prec = unorm16_precision(depth)
        ratio = unorm_prec / fp_prec
        better = "R16F" if ratio > 1 else "R16Unorm"
        print(f"{depth:<10.5f} {fp_prec:<15.10f} {unorm_prec:<15.10f} {ratio:<10.2f} {better}")

if __name__ == "__main__":
    main() 