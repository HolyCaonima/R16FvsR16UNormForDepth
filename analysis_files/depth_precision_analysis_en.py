import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Calculate precision step for R16F (distance between representable values)
def fp16_precision(x):
    if x == 0:
        return 2**-24  # Smallest subnormal number
    
    # Find nearest power of 2
    exponent = np.floor(np.log2(x))
    
    # If x is in subnormal range
    if exponent < -14:
        return 2**-24
    
    # Return precision step
    return 2**(exponent-10)

# Calculate precision step for R16Unorm
def unorm16_precision(x):
    return 1/65535.0

def main():
    print("Calculating precision difference between R16F and R16Unorm...")
    
    # Generate test points - use logarithmic scale to cover range from tiny values to 1
    x_values = np.logspace(-8, 0, 1000)  # From 10^-8 to 10^0 on log scale
    
    # Calculate precision at each point
    fp16_precision_values = [fp16_precision(x) for x in x_values]
    unorm16_precision_values = [unorm16_precision(x) for x in x_values]
    
    # Calculate precision ratio (Unorm16 relative to FP16, >1 means FP16 is better)
    precision_ratio = [unorm/fp for fp, unorm in zip(fp16_precision_values, unorm16_precision_values)]
    
    # Find crossover points where R16F and R16Unorm precision are equal
    crossover_indices = [i for i in range(1, len(precision_ratio)) 
                         if (precision_ratio[i-1] > 1 and precision_ratio[i] < 1) or 
                            (precision_ratio[i-1] < 1 and precision_ratio[i] > 1)]
    
    crossover_points = []
    for idx in crossover_indices:
        crossover_points.append(x_values[idx])
    
    if crossover_points:
        print(f"Precision crossover points: {', '.join([f'{x:.8f}' for x in crossover_points])}")
    
    # Create figure
    plt.figure(figsize=(12, 10))
    
    # 1. Plot precision (log-log scale)
    plt.subplot(3, 1, 1)
    plt.loglog(x_values, fp16_precision_values, 'b-', label='R16F Precision')
    plt.loglog(x_values, unorm16_precision_values, 'r-', label='R16Unorm Precision')
    plt.grid(True, which="both", ls="-")
    plt.ylabel('Precision Step (smaller is better)')
    plt.title('R16F vs R16Unorm Precision Step Comparison (Log Scale)')
    plt.legend()
    
    # 2. Plot precision (linear-log scale)
    plt.subplot(3, 1, 2)
    plt.semilogx(x_values, fp16_precision_values, 'b-', label='R16F Precision')
    plt.semilogx(x_values, unorm16_precision_values, 'r-', label='R16Unorm Precision')
    plt.grid(True, which="both", ls="-")
    plt.ylabel('Precision Step (smaller is better)')
    plt.title('R16F vs R16Unorm Precision Step Comparison (Semi-log Scale)')
    plt.legend()
    
    # 3. Plot ratio
    plt.subplot(3, 1, 3)
    plt.semilogx(x_values, precision_ratio, 'g-')
    plt.axhline(y=1, color='k', linestyle='--')
    
    # Mark crossover points
    for x in crossover_points:
        plt.axvline(x=x, color='r', linestyle='--', alpha=0.5)
        idx = np.abs(x_values - x).argmin()
        plt.text(x, precision_ratio[idx] * 1.1, f'{x:.6f}', 
                 rotation=90, verticalalignment='bottom')
    
    plt.grid(True, which="both", ls="-")
    plt.xlabel('Depth Value')
    plt.ylabel('Precision Ratio (R16Unorm step / R16F step)')
    plt.title('Precision Ratio: Values > 1 indicate R16F is more precise')
    
    # Add explanatory annotation
    plt.figtext(0.5, 0.01, 
                'Conclusion: In small value regions (approx < 0.03), R16F provides higher precision.\n'
                'This explains why R16F performs better for SSAO when focusing on near-object depth differences.',
                ha='center', fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    
    # Optimize layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('depth_precision_comparison_en.png', dpi=150)
    print("Chart saved as 'depth_precision_comparison_en.png'")
    
    # Print numerical comparison for key depth values
    print("\nPrecision comparison at key depth values:")
    key_depths = [0.0001, 0.001, 0.01, 0.1, 0.5]
    print(f"{'Depth':<10} {'R16F Precision':<15} {'R16Unorm Prec.':<15} {'Advantage':<10} {'Better Format'}")
    print("-" * 65)
    
    for depth in key_depths:
        fp_prec = fp16_precision(depth)
        unorm_prec = unorm16_precision(depth)
        ratio = unorm_prec / fp_prec
        better = "R16F" if ratio > 1 else "R16Unorm"
        print(f"{depth:<10.5f} {fp_prec:<15.10f} {unorm_prec:<15.10f} {ratio:<10.2f} {better}")

if __name__ == "__main__":
    main() 