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

## Re-audit 2026-10-13 (reviewer points)
- KPCA projection: manuscript already used 1/sqrt(lambda). Verified numerically (RBF kernel, random data) against sklearn KernelPCA.transform: max abs diff 7e-16 with 1/sqrt(lambda); 0.22 with 1/lambda. Text now defines 1_n (entries 1/n), unit-norm alpha_k and the new-sample kernel. Code: src/acn/features.py uses sklearn KernelPCA unchanged.
- Wilcoxon/Holm: stat_wilcoxon.csv, 23 of 30 with p_holm<0.05 (matches). Friedman: stat_friedman.csv, statistics 46.77-57.64 (spaces), 51.89-58.08 (classifiers), max p_holm 2.63e-9 (text: <=2.7e-9). Best-reduced: LR p_holm 0.0205, DT/RF/SVM 0.000305 (text 0.021, 0.0003). Wording changed from "significant" to "Holm-adjusted p<0.05 (screening only)".
- Nested: nested_summary.csv/json: 0.9003+-0.0220, same-CV max 0.9009, optimism 0.0006 (text "about 0.001"); selection RF 11, DT 4; deltas DT +0.093, RF +0.062, LR +0.004 (p 0.010), kNN +0.002, SVM -0.060 all match.
- Runtime: T9c RF pipeline, n=4,800: KPCA reducer fit 5.47 s vs PCA-10 0.0247 s = 221x (text ">200x"); peak traced memory 363.4 vs 9.8 MB (original) = 37x (the 37x is vs the original-feature pipeline; vs PCA-10 9.75 MB it is the same). A separate scaling run (T9b, reducer alone) gives larger ratios (770x time, 116x memory) because it excludes the classifier/pipeline baseline; the text uses the T9c definition.
- Some balanced-accuracy numbers were removed from the prose to meet the 15-page limit; they remain in the repository tables.
- Reference results (2025 studies): numbers checked against the fetched pages earlier (Waghmode 99.5 %, Patil 99.98 %, Xu&Liu MLP 0.9775, Emirmahmutoglu&Atay 0.999965, Abdelaziz weighted-F1 99.8 %/macro-F1 93.31 %). Abdel-Rahman 2026 and Chavan & Alone are cited qualitatively only (no number). Not re-fetched in this pass.
- Template/rules: official llncs.cls v2.26 and call-for-papers page checked 2026-10 (15 pages + up to 2 extra); the organisers have not confirmed LNCS vs LNNS or Springer approval; ask them (ORGANIZER_EMAIL.txt).

## Line-by-line pass 2026-10-13 (second)
- All ~190 automated checks in claim_check_results.csv pass; 3 unit tests pass (shared reducer == sklearn Pipeline; linear KPCA == PCA; no test rows in train). Main grid = 2,850 rows in cv_results (190 configs x 15 folds), logs: main 28.0 min, nested 64.0 min, tuning 16.5 min.
- Fixed wording: abstract "matched ... for LR and k-NN" now "at the best component count" (at n=10 LR original 0.736 vs PCA 0.506); head/tail sentence now restricted to DT, RF, LR (k-NN and SVM penalties are not larger for reduced spaces); Fig. 3 label 99.9965 (was rounded to 100.00); text range 97.75-99.9965 %.
- Literature re-verified from sources: Abdulhammed (AE+PCA, 81->10, 99.6 %, MDPI abstract); Engelen (25.9 % TCP appendices; attempts without payload relabelled; web brute force/XSS mostly no forward data; corrected release); Panigrahi & Borah (shortcomings + combined dataset; IJET 7(3.24) 479-482); Waghmode (exhaustive feature selection, quantum-inspired LS-SVM, 99.3/99.5/93.3 %); Abdel-Rahman 2026 abstract says FI-AE outperformed "previous dimensionality reduction techniques" on NSL-KDD, UNSW-NB15, CIC-IDS2017 -- NOT specifically PCA; text corrected.
- Not re-fetched this pass: Patil, Abdelaziz, Xu&Liu, Emirmahmutoglu&Atay, Chavan&Alone values (checked in the earlier pass); classic references (Breiman, Cortes, Cover&Hart, Demsar, Nadeau&Bengio, Quinlan, Scholkopf, Pedregosa, Chicco, Kuang, Sharafaldin, Ring, Arp, Apruzzese) checked from memory of standard citation data, not re-fetched.
- Earlier variants (IEEE Access/COMPSAC/A4 .tex/.pdf) still contain the old abstract and head/tail wording; only the Springer paper is the submission candidate.

## Page size check 2026-10-13
- Previous PDF was US Letter (612x792 pt) because llncs.cls sets only the text block (12.2 x 19.3 cm) and not the paper size; pdfTeX defaulted to Letter. Neither the CICPS call-for-papers page nor Springer's conference-proceedings-guidelines page states a paper size (final books are printed at 155 x 235 mm by the publisher).
- Rebuilt as A4 (595.3 x 841.9 pt) via \AtBeginDocument{\pdfpagewidth=210mm \pdfpageheight=297mm}. Text block, pagination (15 pages) and content unchanged. A4 is a convention choice, not a stated requirement: confirm with the organisers (ORGANIZER_EMAIL.txt).
