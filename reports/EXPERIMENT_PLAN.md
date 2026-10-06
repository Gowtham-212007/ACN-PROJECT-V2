# Experiment Plan (as executed)

Research questions: RQ1 does reduction help vs original features? RQ2 does KPCA beat PCA? RQ3 which kernel / component count? RQ4 cost? RQ5 are differences statistically supported?

| Stage | Experiment | Status |
|---|---|---|
| 1 | `run_cv.py --smoke`, `pytest` (3 tests) | done |
| 2 | Main grid: 21 spaces x 5 classifiers x {standard, balanced} x 15 folds | done (`results/raw/cv_results_20261006_174848.csv`) |
| 3 | Training-size sensitivity (`run_sizes.py`) | done |
| 3 | Runtime / memory / KPCA scaling (`run_runtime.py`) | done |
| 3 | Statistics (`stats_tests.py`) | done |
| 4 | Tables, figures, paper | done (`make_tables.py`, `make_figures.py`, `papers/ieee`) |
| B | Full-data / leakage-free sample (`prepare_raw.py`, `run_cv.py --data`) | **not run - raw data unavailable in sandbox** |
| C | Temporal (day-wise) split (`run_temporal.py`) | **not run on real data** |
| - | Hyper-parameter search, SMOTE | intentionally skipped (justification in paper Sec. IV) |

Primary criterion: macro-F1. Seed 42. Experiments with negligible expected value (extra kernels such as poly/sigmoid, deep models) were not run.
