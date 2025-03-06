# R16F vs R16Unorm for Depth Storage

This repository contains a comprehensive analysis of precision differences between R16F and R16Unorm formats when storing Linear Eye Depth, with a particular focus on SSAO (Screen Space Ambient Occlusion) applications.

## Key Findings

1. **R16F provides higher precision in small value regions (approx < 0.03)**
   - For normalized depth values less than 0.0318, R16F offers superior precision
   - This advantage is critical for SSAO which primarily focuses on near-depth differences

2. **Far Plane impact is significant**
   - Analysis with 50m, 100m, 200m, and 1000m Far Plane settings shows R16F's advantage increases with Far Plane distance
   - With a 1000m Far Plane, R16F has 100% precision advantage in the entire SSAO-relevant range (0-10m)
   - Precision crossover points: 1.56m (50m Far), 3.12m (100m Far), 6.21m (200m Far), 30.30m (1000m Far)

3. **R16F outperforms despite "wasting" the sign bit**
   - R16F's non-linear precision distribution provides up to 256x higher precision near zero
   - This more than compensates for the theoretical disadvantage of using 1 bit for sign

## Repository Contents

### Python Scripts
- `depth_precision_analysis.py` - Basic comparison of R16F vs R16Unorm precision
- `depth_precision_analysis_en.py` - English version of basic comparison
- `eye_depth_analysis.py` - Analysis of Linear Eye Depth with various Far Plane settings
- `generate_summary_report.py` - Comprehensive analysis and report generation

### Analysis Reports
- `depth_precision_report.md` and `depth_precision_report_en.md` - Initial analysis reports
- `depth_precision_report_with_1000m.md` and `depth_precision_report_with_1000m_en.md` - Updated reports including 1000m Far Plane
- `depth_format_analysis_report.html` - HTML report of initial findings
- `depth_format_analysis_report_with_1000m.html` - HTML report including 1000m Far Plane analysis

### Visualization Charts
- `depth_precision_comparison.png` and `depth_precision_comparison_en.png` - Basic precision comparison
- `eye_depth_analysis.png` - Linear Eye Depth analysis with standard Far Planes
- `eye_depth_analysis_with_1000m.png` - Linear Eye Depth analysis including 1000m Far Plane
- `depth_precision_summary.png` - Comprehensive results visualization
- `depth_precision_summary_with_1000m.png` - Comprehensive results including 1000m Far Plane

### Dependencies
- `requirements.txt` - Python dependencies for running the analysis scripts

## Conclusion

For SSAO applications, especially with larger Far Plane settings (200m+), R16F format provides significantly better precision for depth storage than R16Unorm, despite theoretical arguments to the contrary. With a 1000m Far Plane, the advantage is undisputed across all SSAO-relevant depth ranges. 