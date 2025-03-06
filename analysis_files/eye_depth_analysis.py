import numpy as np
import matplotlib.pyplot as plt

# Calculate precision step for R16F format
def fp16_precision(x):
    if x == 0:
        return 2**-24  # Smallest subnormal
    
    exponent = np.floor(np.log2(x))
    
    if exponent < -14:
        return 2**-24
    
    return 2**(exponent-10)

# Calculate precision step for R16Unorm format
def unorm16_precision(x):
    return 1/65535.0

# Calculate Linear Eye Z from perspective projection
def linear_eye_z(ndc_z, near, far):
    # Assuming reversed-Z NDC in [0,1] range
    # ndc_z is 0 at far plane and 1 at near plane
    return near * far / (far * ndc_z + near * (1.0 - ndc_z))

def main():
    # Typical near and far plane values for SSAO scenarios
    near = 0.1  # 10cm
    far_values = [50.0, 100.0, 200.0, 1000.0]  # 添加1000m的Far Plane
    
    plt.figure(figsize=(15, 14))  # 增加图表高度适应更多行
    
    # For each far plane value
    for i, far in enumerate(far_values):
        # Create 1000 evenly distributed points in normalized device coordinates
        ndc_z_values = np.linspace(0.0, 1.0, 1000)
        
        # Convert to Linear Eye Z
        eye_z_values = np.array([linear_eye_z(z, near, far) for z in ndc_z_values])
        
        # Get normalized eye z values (0-1 range)
        normalized_eye_z = eye_z_values / far
        
        # Calculate precision for both formats
        fp16_prec = np.array([fp16_precision(z) for z in normalized_eye_z])
        unorm16_prec = np.array([unorm16_precision(z) for z in normalized_eye_z])
        
        # Calculate precision ratio (Unorm16/FP16, >1 means FP16 is better)
        precision_ratio = unorm16_prec / fp16_prec
        
        # Plot Linear Eye Z distribution
        plt.subplot(4, 3, i*3+1)  # 修改布局为4行
        plt.plot(ndc_z_values, eye_z_values)
        plt.grid(True)
        plt.title(f'Linear Eye Z (Far={far}m)')
        plt.xlabel('NDC Z (0=far, 1=near)')
        plt.ylabel('Eye Space Z')
        
        # Plot precision values for normalized eye z
        plt.subplot(4, 3, i*3+2)  # 修改布局为4行
        plt.semilogy(eye_z_values, fp16_prec, 'b-', label='R16F')
        plt.semilogy(eye_z_values, unorm16_prec, 'r-', label='R16Unorm')
        plt.grid(True)
        plt.legend()
        plt.title(f'Precision Step vs. Eye Z (Far={far}m)')
        plt.xlabel('Eye Space Z')
        plt.ylabel('Precision Step (smaller is better)')
        
        # Plot precision ratio
        plt.subplot(4, 3, i*3+3)  # 修改布局为4行
        plt.semilogx(eye_z_values, precision_ratio)
        plt.axhline(y=1, color='k', linestyle='--')
        plt.grid(True)
        plt.title(f'Precision Ratio (Far={far}m)')
        plt.xlabel('Eye Space Z')
        plt.ylabel('Ratio (Unorm16/FP16)')
        
        # Calculate stats
        ssao_relevant_range = eye_z_values <= 10.0  # SSAO mostly cares about first 10m
        better_format_counts = {
            "R16F": np.sum(precision_ratio[ssao_relevant_range] > 1),
            "R16Unorm": np.sum(precision_ratio[ssao_relevant_range] <= 1)
        }
        
        total_relevant = np.sum(ssao_relevant_range)
        if total_relevant > 0:
            r16f_percentage = 100 * better_format_counts["R16F"] / total_relevant
            print(f"\nFor Far={far}m, in SSAO-relevant range (0-10m):")
            print(f"R16F better: {better_format_counts['R16F']} samples ({r16f_percentage:.1f}%)")
            print(f"R16Unorm better: {better_format_counts['R16Unorm']} samples ({100-r16f_percentage:.1f}%)")
    
    plt.tight_layout()
    plt.savefig('eye_depth_analysis_with_1000m.png', dpi=150)
    print("\nChart saved as 'eye_depth_analysis_with_1000m.png'")
    
    # Cross-over analysis
    print("\n--- Crossover Analysis ---")
    for far in far_values:
        # Generate more detailed sampling for crossover analysis
        ndc_z_values = np.linspace(0.0, 1.0, 10000)
        eye_z_values = np.array([linear_eye_z(z, near, far) for z in ndc_z_values])
        normalized_eye_z = eye_z_values / far
        
        fp16_prec = np.array([fp16_precision(z) for z in normalized_eye_z])
        unorm16_prec = np.array([unorm16_precision(z) for z in normalized_eye_z])
        precision_ratio = unorm16_prec / fp16_prec
        
        # Find crossover points (where precision ratio crosses 1.0)
        crossovers = []
        for i in range(1, len(precision_ratio)):
            if (precision_ratio[i-1] < 1 and precision_ratio[i] >= 1) or \
               (precision_ratio[i-1] >= 1 and precision_ratio[i] < 1):
                eye_z = eye_z_values[i]
                crossovers.append(eye_z)
        
        print(f"\nFor Far={far}m, precision crossover points (eye space):")
        if crossovers:
            for i, z in enumerate(crossovers):
                print(f"  Crossover {i+1}: Eye Z = {z:.3f}m")
                print(f"    - R16F better for Eye Z < {z:.3f}m")
                print(f"    - R16Unorm better for Eye Z > {z:.3f}m")
        else:
            print("  No crossover points found.")

if __name__ == "__main__":
    main() 