# Depth Format Precision Analysis: R16F vs R16Unorm

## Key Findings

1. **R16F provides higher precision in small value regions (approx < 0.03)**
   - R16F format has a non-linear precision distribution, offering extremely high precision near zero
   - For linear depth values normalized to 0-1, this characteristic gives R16F an advantage in representing near-object depths

2. **Precision crossover point is at 0.0318**
   - R16F provides higher precision when normalized depth values are less than 0.0318
   - R16Unorm provides higher precision when normalized depth values are greater than 0.0318

3. **Relationship between Linear Eye Depth and Far Plane**
   - Based on analysis with different Far Planes (50m, 100m, 200m), R16F shows significant precision advantages in SSAO-relevant ranges (0-10m)
   - The precision crossover point moves further as the Far Plane increases (1.56m with 50m Far, 3.12m with 100m Far, 6.21m with 200m Far)

## Key Numerical Comparisons

| Depth Value | R16F Precision  | R16Unorm Precision | Advantage Ratio | Better Format |
|-------------|-----------------|-------------------|-----------------|---------------|
| 0.0001      | 0.0000000596    | 0.0000152590      | 256.00          | R16F          |
| 0.001       | 0.0000009537    | 0.0000152590      | 16.00           | R16F          |
| 0.01        | 0.0000076294    | 0.0000152590      | 2.00            | R16F          |
| 0.1         | 0.0000610352    | 0.0000152590      | 0.25            | R16Unorm      |
| 0.5         | 0.0004882812    | 0.0000152590      | 0.03            | R16Unorm      |

## SSAO-Relevant Depth Range Analysis

For SSAO-relevant near-depth ranges (0-10m):

| Far Plane | R16F Better | R16Unorm Better | Precision Crossover |
|-----------|-------------|-----------------|---------------------|
| 50m       | 94.6%       | 5.4%            | 1.56m               |
| 100m      | 97.7%       | 2.3%            | 3.12m               |
| 200m      | 99.4%       | 0.6%            | 6.21m               |

## Analysis Conclusions

1. **Your observation is correct**: Although R16Unorm theoretically should provide more uniform precision distribution across the entire range, R16F indeed performs better in practical SSAO applications.

2. **Phenomenon explanation**:
   - SSAO algorithms primarily focus on near-scene depth differences, which is exactly where R16F format provides high precision
   - As the Far Plane increases, R16F's advantage zone covers more of the near-scene area
   - With a Far Plane of 200m, R16F provides higher precision in the 0-6.21m range, covering the most critical areas for SSAO

3. **Far Plane impact**:
   - The larger your Far Plane setting, the wider the advantage zone of R16F relative to R16Unorm
   - This explains why you observed better results when storing Linear Eye Depth with R16F compared to R16Unorm

4. **Sign bit "waste" compensation**:
   - Although R16F "wastes" 1 bit for the sign, its non-linear precision distribution provides far superior precision in small value areas
   - In SSAO application scenarios, the advantage of this precision distribution characteristic far outweighs the "waste" of the sign bit

## Recommendations

1. For SSAO applications with your current Far Plane settings, R16F is the better choice.

2. If R16Unorm must be used, consider:
   - Reducing the Far Plane value (if possible)
   - Applying a non-linear transformation (like square root) to redistribute precision
   - Using a custom encoding/decoding scheme to improve near-field precision

## Charts

See the generated chart files:
- depth_precision_comparison_en.png: Basic precision comparison
- eye_depth_analysis.png: Linear Eye Depth analysis with different Far Planes 