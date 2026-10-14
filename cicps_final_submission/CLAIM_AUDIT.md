# CLAIM AUDIT
| Claim | Evidence | Status |
|---|---|---|
| 6,000-record class-stratified sample; Table 2 supports sum 6,000 | T8_per_class_best.csv (recomputed this pass) | verified |
| 189 model configs + 1 baseline = 190 x 15 = 2,850 fits | cv_results_20261006_184913.csv | verified |
| RF original acc 0.972, macro-F1 0.901 | cv_results (agg), selected_model.json | verified earlier + figure output |
| Nested 0.900+-0.022 | nested_summary.csv | verified earlier |
| Web brute force/XSS F1 0.53/0.59 | T8 | verified earlier |
| SVM advantage 0.076 -> 0.021 | T12_tuning | verified earlier |
| >200x KPCA fit time, ~37x whole-pipeline memory | T9c_runtime_compact | verified earlier |
| LR best-space diff 0.004, p_holm 0.021 (5-test family) | stat_best_reduced.csv: 0.004485, 0.020508 | verified |
| k-NN orig vs PCA-10 -0.001 | stat_wilcoxon.csv: -0.001189 (0.800498 vs 0.801687) | verified |
| 30-comparison family | stat_wilcoxon.csv, stats script | verified |
| Training-size robustness | not in results/v2 | removed from text (earlier pass) |
