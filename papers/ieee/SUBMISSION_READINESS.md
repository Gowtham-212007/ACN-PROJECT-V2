# Submission Readiness (v2, raw-data evidence)

**Status: NOT publication-ready; stronger than v1.** Suitable target after the items below: workshop / student-track / regional conference. Not a claim of acceptance likelihood.

## Resolved by the v2 run (raw CIC-IDS2017, 2,830,743 flows, 8 files)
- Pre-sampling imputation leakage removed (no imputation before sampling; fold-wise fitting). De-duplicated 308,381 exact duplicates first.
- Sample 6,000 records (floor 100/class, 15 classes) instead of 1,000.
- Nested CV, small nested hyper-parameter search (SVM C/gamma, KNN k, RF depth), two time-aware checks, 232 automated claim checks, 0 failing.
- v1 results archived (`papers/ieee/archive/`, `results/` v1 paths); v2 under `results/v2/`.

## Still blocking
1. **Sample, not full data.** Exact KPCA limited to n=6,000; rare classes have 11-36 raw records (Heartbleed 11, Infiltration 36, SQLi 21); per-class claims for them are fragile.
2. **No true temporal validation.** Raw files have no timestamps; each attack family sits on one day, so day-wise splits are impossible. Within-file chronological/blocked splits assume row order = capture order (unverified).
3. **One dataset.** No cross-dataset or corrected-release (Engelen et al.) check.
4. **Limited tuning.** Small grid, 4 spaces, 5 outer folds; KPCA kernel parameters (gamma) not tuned beyond the default/cosine.
5. **Template/authors.** Compiled with a preview shim, not real IEEEtran; author block empty; confirm page/abstract limits (10 pages preview).
6. **Sources.** Re-read the sources listed in CLAIM_AUDIT.md section B.
7. Repeated-CV p-values are optimistic (Nadeau-Bengio); nested results are the primary evidence.

## Evidence summary
- Best observed: RF on original features, macro-F1 0.901+-0.020 (accuracy 0.972, MCC 0.948); nested 0.900+-0.022.
- Original >= PCA/KPCA for DT, RF (0.06-0.09 nested), ~equal LR/KNN; SVM exception shrinks under tuning (0.076 -> 0.021).
- Chronological split lowers macro-F1 0.07-0.24, ranking kept.
- KPCA cost: fit 5.5 s vs 0.02 s, ~37x traced memory at n=4,800; 64 TB full-data figure is theoretical arithmetic.
