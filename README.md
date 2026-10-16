# ACN-PROJECT-V2: PCA and Kernel PCA versus original features for intrusion detection (CIC-IDS2017)

Code, data sample and results behind the paper "An Experimental Evaluation of Classification Algorithms for Intrusion Detection Systems".

## Verify the paper
```bash
pip install -r requirements.txt
export ACN_RUN=v2
python -m src.acn.check_claims   # recomputes every number quoted in the paper from the per-fold results
```
See `RUN_EXPERIMENTS.md` for the full re-run.

## Contents
- `src/acn/`: pipeline (fold-wise imputation, scaling, PCA/KPCA, five classifiers), repeated and nested CV, tuning, row-order checks, statistics, cost benchmark, table and figure scripts, claim checker.
- `data/sample_raw6000.npz` and `.manifest.json`: the 6,000-record class-stratified sample (seed 0, at least 100 records per class, 15 classes, 78 features) drawn from the eight CIC-IDS2017 MachineLearningCVE files after exact-duplicate removal (2,830,743 to 2,522,362 flows).
- `results/v2/`: per-fold results, tables, statistics and figures.
- `v1_course_project/`: the earlier 1,000-row, 45-experiment course project, archived; not used by the paper.
- `tests/`: sanity checks. `requirements.txt`: Python 3.13, scikit-learn 1.9.

## Headline result
A random forest on the original 78 features scored highest: macro-F1 0.901 +/- 0.020, accuracy 0.972 +/- 0.004 (nested estimate 0.900 +/- 0.022). PCA and KPCA did not help except for the default RBF-SVM (cosine KPCA), whose advantage shrank from 0.076 to 0.021 after tuning.

## Limits
One dataset, one sample, proxy chronology only, limited tuning. The raw CIC-IDS2017 files are not included; get them from the Canadian Institute for Cybersecurity.
