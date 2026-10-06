# Research Changelog (branch `research-ieee`)

- Added `src/acn/` package: config, data, models, features, evaluation, run_cv, run_sizes, run_runtime, stats_tests, make_tables, make_figures, prepare_raw, run_temporal.
- Replaced single-split evaluation with repeated stratified 5-fold (x3); preprocessing and reduction fitted on training folds only.
- Added original-feature, PCA, KPCA (linear/RBF/cosine) x {5,10,15,20,30} spaces; SVM and RF added to LR/KNN/DT.
- Added macro-F1, balanced accuracy, MCC, per-class metrics, majority baseline, balanced class weights.
- Added Friedman / Wilcoxon-Holm tests, cost benchmarks, 10 tables, 9 figures.
- Added IEEE manuscript (`papers/ieee/paper.tex`), reference generator and verified bibliography.
- Added review documents (CLAIM_AUDIT, REVIEWER_CRITIQUE, REVISION_PLAN, LITERATURE_GAP).
- Original files (README, prepare_data.py, make_scripts.py, 45 scripts, logs) left unmodified.
