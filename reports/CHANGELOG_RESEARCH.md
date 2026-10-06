# Research Changelog (branch `research-ieee`)

- Added `src/acn/` package: config, data, models, features, evaluation, run_cv, run_sizes, run_runtime, stats_tests, make_tables, make_figures, prepare_raw, run_temporal.
- Replaced single-split evaluation with repeated stratified 5-fold (x3); preprocessing and reduction fitted on training folds only.
- Added original-feature, PCA, KPCA (linear/RBF/cosine) x {5,10,15,20,30} spaces; SVM and RF added to LR/KNN/DT.
- Added macro-F1, balanced accuracy, MCC, per-class metrics, majority baseline, balanced class weights.
- Added Friedman / Wilcoxon-Holm tests, cost benchmarks, 10 tables, 9 figures.
- Added IEEE manuscript (`papers/ieee/paper.tex`), reference generator and verified bibliography.
- Added review documents (CLAIM_AUDIT, REVIEWER_CRITIQUE, REVISION_PLAN, LITERATURE_GAP).
- Original files (README, prepare_data.py, make_scripts.py, 45 scripts, logs) left unmodified.

## Methodological hardening pass
- Title and abstract no longer claim leakage-controlled evaluation; residual pre-sampling imputation leak stated as a limitation (Sec. III, IX).
- "Strongest/best model" replaced by "highest observed macro-F1 among the evaluated configurations".
- Added nested cross-validation (`run_nested.py`, `analyze_nested.py`, Table 5): nested macro-F1 0.715+-0.044 vs 0.722 same-CV (optimism ~0.008). LR advantage of original features is only modest (+0.019, p=0.055) once selection is nested; DT/RF clear; KNN none; SVM exception survives (needs cosine-KPCA-30 + balanced weights).
- Number audit (`check_claims.py`, 104 checks, 0 failing) corrected: linear-KPCA vs PCA gap (<=0.011 -> up to 0.014 for RF with balanced weights), "kernel mattered more than components" (true for KNN/DT/RF only), accuracy-macro-F1 gap (0.23, not 0.24), memory scaling wording (log-log slope 1.9; timing exponent not claimed).
- Citation audit: all 17 bibliographic records re-verified or flagged (see CLAIM_AUDIT.md); claims about Apruzzese, Chicco, Dem\v{s}ar, Arp and "many studies omit baselines" softened to what the sources support.
- 14 TB figure labelled as theoretical arithmetic (n^2 x 8 bytes), not a measurement.
- Limitations section rewritten (7 numbered limitations).
