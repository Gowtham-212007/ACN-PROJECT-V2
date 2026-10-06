# Revision Plan

1. Download raw CIC-IDS2017; run `prepare_raw.py`; rerun grid with larger n (e.g. 5-10k) using Nystrom/incremental KPCA for scale.
2. Run `run_temporal.py` (train Tue/Wed, test Thu) and report class-restricted results.
3. Add nested CV or a held-out test set once classes have enough records.
4. Add small, documented hyper-parameter search per classifier (nested).
5. Add a second dataset (e.g. UNSW-NB15) for cross-dataset generalisation.
6. Fill in authors, compile with real IEEEtran, re-verify every number via CLAIM_AUDIT.md.
