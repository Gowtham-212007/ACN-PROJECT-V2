# Claim audit (Springer manuscript)
Sources: `claim_check_results.csv` (232 automated checks of text numbers against result CSVs; **0 failing**, re-run 2026-10-13 with `ACN_RUN=v2 python -m src.acn.check_claims`) and manual checks below.

| Claim | Evidence | Method | Status |
|---|---|---|---|
| RF, original features: acc 0.972±0.004, macro-F1 0.901±0.020, MCC 0.948 | results/v2/tables T7, claim_check.csv | automated | verified |
| Nested macro-F1 0.900±0.022 | results/v2/tables/nested_summary.csv | automated | verified |
| Web-attack F1 0.53 / 0.59 | T8_per_class_best.csv | automated | verified |
| KPCA fit >200x PCA, ~37x traced memory at n=4,800 | T9_runtime.csv | automated | verified |
| SVM reduction advantage 0.076 -> 0.021 after tuning | T12_tuning_both.csv | automated; Table 4 now compares like with like | verified |
| 698 conflicting-label feature groups in the pool, none in the 6,000 sample | data manifest; sample checked directly (0 duplicated feature vectors) | script run 2026-10-09 | verified |
| Friedman: statistics 46.8–58.1, Holm p ≤ 2.7e-9 | stat_friedman.csv | manual | verified |
| Literature table: Waghmode 2025 (CIC-IDS-2017 acc 99.5 %) | nature.com/articles/s41598-025-95621-7 (read 2026-10-13) | page read | verified from page; author list truncated on page ("et al.") |
| Patil 2025 (ET+IG 99.98 %, PCA 99.58–99.96 %, 70/30) | informatica.si PDF (read) | page read | verified |
| Abdelaziz 2025 (weighted-F1 99.8 %, macro-F1 93.31 %, 26 features) | link.springer.com/article/10.1007/s10922-024-09874-0 | abstract read; page itself also calls 99.8 % "accuracy" (noted) | verified (abstract) |
| Xu & Liu 2025 (MLP acc 0.9775) | arxiv.org/abs/2506.19877 v2 | page read | verified; arXiv preprint, not peer-reviewed venue |
| Emirmahmutoğlu & Atay 2025 (CSE-CIC-IDS2018 0.999965) | link.springer.com/article/10.1007/s12083-025-01947-4 | conclusion read; first 100k of 101.7k chars | verified (not CIC-IDS2017) |
| Abdel-Rahman 2026 outperforms PCA (3 datasets) | nature.com/articles/s41598-026-36695-9 | text read; result tables not rendered, numbers not used | qualitative only |
| Chavan & Alone 2025 "high accuracy" | ijcaonline.org page | abstract read; no number stated | verified |
| Earlier-work claims (Ring, Sharafaldin, Engelen, Panigrahi, Abdulhammed, Kuang, Arp, Apruzzese) | papers/ieee/FINAL_REFERENCE_AUDIT.md | prior audit | partly read: Kuang full text, Abdulhammed results, Nadeau–Bengio journal version NOT read |

Not verified: any IEEE Xplore paper (IEEE pages were not retrievable from this environment). No cross-paper accuracy comparison is presented as a ranking.
