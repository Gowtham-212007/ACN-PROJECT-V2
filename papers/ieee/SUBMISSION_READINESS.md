# Submission Readiness

**Status: NOT publication-ready.** The paper is internally consistent and honest about its limits, but the remaining methodological objections (tiny sample, residual leakage, no external validation) are *not* resolved. Realistic target after the "must fix" items: a workshop / student-track / regional conference.

## Must fix before submission
1. **Residual leakage.** Download CIC-IDS2017, run `prepare_raw.py` (train-only imputation, sampling after splitting where needed), rerun `run_cv.py --data`, `run_nested.py`, `stats_tests.py`, `analyze_nested.py`, `make_tables.py`, `make_figures.py`; update the paper numbers and re-run `check_claims.py` until 0 failures. (Not possible in the sandbox: raw data not downloadable.)
2. **Sample size.** Use more records (several thousand; with approximate/Nystroem KPCA if needed) so rare classes have enough test records. At 10-17 records per attack class the per-class claims are fragile.
3. **External validation.** Run at least one temporal split (`run_temporal.py`, unexecuted on real data) and ideally a second dataset. Without this the paper must keep "random splits of one sample only".
4. **Authors and template.** Fill in the author block; compile with the real `IEEEtran.cls` (the repo preview used a layout shim); fix any resulting overfull boxes; confirm page limit and abstract length (current abstract is long, ~270 words).
5. **Re-read the unverified sources** listed in CLAIM_AUDIT.md section B (Arp et al., Ring et al., Kuang et al. abstract, classic-reference page numbers) and confirm each sentence that cites them.

## Strongly recommended
1. Small nested hyper-parameter search (SVM C/gamma, KNN k, RF depth) so the SVM/RBF-KPCA conclusions are not about defaults only.
2. Use the corrected CIC-IDS2017 release (Engelen et al.) as a robustness check.
3. Expand related work with a verified, systematic set of KPCA/PCA-for-IDS papers; only then can the paper say anything about how common weak evaluation practice is.
4. Run an approximate KPCA (Nystroem) and measure, rather than extrapolate, scaling.
5. Report fold-level paired effect sizes with Nadeau-Bengio corrected variance.
6. Measure how many values were imputed in the cached sample, to bound the residual leak.

## Optional future work
- Deep baselines / autoencoders; supervised reduction (LDA); robust scaling.
- Multi-seed repeats of the whole pipeline; calibration and per-class threshold analysis.
- Wall-clock deployment latency on target hardware.
- Cross-dataset study (UNSW-NB15, CSE-CIC-IDS2018).

## Evidence summary
- Headline: highest observed macro-F1 = RF on original features, 0.722+-0.058 (same-CV) / 0.715+-0.044 (nested); accuracy 0.952; web-attack F1 0.21-0.50.
- Qualified finding kept: original >= PCA/KPCA for DT, RF (clear), LR (modest, p=0.055 nested), KNN unchanged, SVM exception (cosine KPCA-30 + balanced weights).
- Cost: KPCA ~7x memory, ~10x reducer fit time at n=800; 14 TB = theoretical estimate.
