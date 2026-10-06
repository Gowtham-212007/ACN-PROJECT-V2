# Research Audit of the original ACN-PROJECT-V2

Scope: the repository as received (README, `prepare_data.py`, `make_scripts.py`, 45 generated scripts, `results/`). Nothing below was assumed; every item was read from the code.

| # | Finding | Severity | Evidence | Resolution |
|---|---------|----------|----------|------------|
| 1 | **Single 80/20, 60/40, 40/60 hold-out split, seed 42** – no repeats, no variance | High | `make_scripts.py` L46 | Repeated stratified 5-fold x3 (15 paired folds) |
| 2 | **Kernel is confounded with component count** (rbf->5, linear->10, cosine->15) | High | `KPCA` list in `make_scripts.py` | Full grid: 3 kernels x {5,10,15,20,30} + matched n=10 |
| 3 | **No original-feature baseline, no PCA baseline** | High | no such scripts | Added `orig`, `pca-n` spaces |
| 4 | **Linear KPCA is PCA** – presented as a distinct method | Medium | identical eigenproblem; our results confirm (diff <= 0.011 macro-F1) | Reported as PCA-equivalent |
| 5 | **Imputation on the full data before sampling** (mean imputer fitted on all 1.3M rows) | Medium (mild leakage) | `prepare_data.py` L25 | Cannot be undone from cached sample; imputer re-fitted per training fold, residual documented as a limitation; `prepare_raw.py` provides a leakage-free path |
| 6 | **Weighted metrics only**; accuracy dominated by BENIGN (71.8%) | High | `average="weighted"` | Added macro-F1, balanced accuracy, MCC, per-class report, majority baseline |
| 7 | **Only 1000-row sample**; 10-row minority classes; test sets of 200-600 | High | `N_SAMPLES=1000` | Kept (KPCA is O(n^2)); disclosed; training-size sensitivity added |
| 8 | **No hyper-parameter justification**, no class weighting | Medium | fixed constructors | Fixed, documented defaults; balanced class-weight variant evaluated; tuning deliberately omitted; nested CV for *configuration selection* later proved feasible (3-fold inner on 800 records) and was added (`run_nested.py`), though inner folds are very small |
| 9 | **No statistics** | High | none | Friedman, Wilcoxon + Holm, rank-biserial effect size |
| 10 | **No cost analysis** | Medium | none | fit/train/inference time, tracemalloc peak, KPCA scaling |
| 11 | **Random split, no temporal/cross-dataset test** | High | all scripts | Not fixable with the cached sample (no timestamps); `run_temporal.py` written, **unexecuted on real data** |
| 12 | README suggests RF + linear KPCA is best | High | README | Contradicted: original features win on macro-F1 for LR/DT/RF |
| 13 | CIC-IDS2017 known artifacts (duplicate rows, Fwd-header-length duplicate column, labelling errors, Engelen et al. 2021) | Medium | literature | Disclosed; not corrected (raw data unavailable here) |
| 14 | Raw data not in repo and gated behind a form | Blocker for full reproduction | repo tree | Documented in RUN_EXPERIMENTS.md |

No target-label leakage into features was found. Scaler and reducer were already train-only in the original scripts.
