# Submission Readiness (v2.1, after final-fixes pass)

**Status: technically ready for a student/research conference or workshop once the author block is filled in (the one remaining blocker below); not a claim of acceptance.** Earlier "not publication-ready" verdicts referred to the items now resolved. Suitable target after the items below: workshop / student-track / regional conference. Not a claim of acceptance likelihood.

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


## Final-fixes pass (reviewer checklist)
1. *Wording*: "chronological/time-aware" replaced by "row-order robustness / proxy chronology" (head/tail and blocked splits) in paper, tables, captions; limitations state no true temporal drift is tested. Internal CSV identifiers keep the old split names for reproducibility.
2. *Sample*: stated explicitly (abstract, Sample paragraph, limitation 1) as class-stratified, floor of 100/class, NOT prevalence-preserving (benign 67.2% sample vs 83% pool).
3. *Bibliography*: all 17 entries re-checked against Crossref/publisher/arXiv pages; Ring (vol. 86, pp. 147-167, DOI) and Apruzzese (vol. 19, no. 4, pp. 5152-5169) completed; citing sentences checked. Unsupported/over-attributed statements fixed: "Fwd Header Length duplicate" no longer cited to Engelen; "99.6% with classifiers including random forest"; cross-dataset cite split; "78 features" attributed to the MachineLearningCVE files, not to Sharafaldin. Still unverifiable: Kuang et al. abstract (paywalled; only the title is relied on), per-classifier results of Abdulhammed et al.
4. *Authors*: **NOT done** - the real names/affiliations/emails were not supplied; the block still holds `[Author One]` placeholders and must be filled by the authors.
5. *Template*: compiled with the real IEEEtran.cls v1.8b (CTAN), 9 pages, no undefined references, no overfull boxes. Output: `paper_ieeetran.pdf`. (Needs `TEXINPUTS` pointing to IEEEtran if not installed; Overleaf has it.) Check the target venue's own template/page limit; abstract is 263 words (many venues cap at 200-250).
6. *Numerical consistency*: 232 automated checks, 0 failing; abstract numbers (accuracy, macro-F1, nested, penalties, runtime, memory) each matched to a checked value.
7. *Limitations*: kept as candid; only clarified (sample not prevalence-preserving; no true temporal drift).

## Venue (pending author decision) - checked 2026-10-07
Candidate found by search: IEEE ICMI 2027 (Computing and Machine Intelligence), Central Michigan University, 24-25 Apr 2027; submission deadline 15 Dec 2026; standard length 5 pages (extra pages $25/page); official IEEE conference template via Microsoft CMT; topics include "Intrusion, Malware, and Anomaly Detection"; accepted papers submitted for possible inclusion in IEEE Xplore; at least one author must register and present (source: https://www.icmiconf.com/author.html). Unverified: blind/non-blind review, current CFP changes. The current manuscript is 9 pages, so a 5-page version needs cuts (keep headline tables, nested/tuning, row-order, limitations; move rest to supplementary repo). Do not cut until the venue is chosen.

## Number audit (final)
232 recomputed claims, 0 failing; all 116 decimal numbers in the prose were additionally matched to values in the result CSVs, except 4 that come from elsewhere: 0.2% NaN share (raw profile), 2.5 M pool size, Python 3.13, and the cited 99.6% (Abdulhammed et al.).
