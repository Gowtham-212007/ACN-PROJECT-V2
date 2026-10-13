# Reproducibility
- Data: CIC-IDS2017 `MachineLearningCVE` (8 CSV files, not redistributed). Place them as described in `../RUN_EXPERIMENTS.md`.
- Environment: Python 3.13, scikit-learn 1.9, NumPy 2.5, SciPy 1.18, pandas, matplotlib; 2-vCPU / 7 GB VM (see `../requirements.txt`).
- Commands (from repo root; see `../RUN_EXPERIMENTS.md` for the exact sequence): sampling (`src/acn/prepare_raw.py`), main grid (`run_cv.py`, ~28 min), nested CV (`run_nested.py`, ~64 min), tuning (`run_tuning.py`, ~16 min), runtime (`run_runtime.py`, `run_sizes.py`), row-order checks (`run_temporal.py`, `run_blocked.py`), tables/figures (`make_tables.py`, `analyze_extra.py`, `make_figures.py`, `make_springer_figs.py`), claim check (`check_claims.py`).
- This session did NOT re-run the experiments (raw data and cached results already existed); it re-ran table/figure generation and `check_claims` (232 checks, 0 failing).
- Known limitations: one 6,000-record class-stratified (not prevalence-preserving) sample; one dataset; row-order checks are proxy chronology; folds share training data so p-values are screening only.
