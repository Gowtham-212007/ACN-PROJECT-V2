# Claim verification

Authoritative sources: `../results/v2/tables/*.csv`, `../results/v2/raw/*`, `../springer_cicps_submission/claim_check_results.csv` (about 190 automated checks, all pass at last run), unit tests (3 pass).

| Headline claim | Evidence | Status |
|---|---|---|
| RF original: accuracy 0.972 +- 0.004, macro-F1 0.901 +- 0.020 | cv_results (claim_check: 0.9722/0.0044; 0.9009/0.0200) | Verified |
| Nested macro-F1 0.900 +- 0.022 | nested_naive_vs_nested.json: 0.9003 +- 0.0220; optimism 0.0006 | Verified |
| Web brute force F1 0.53, XSS 0.59 | T8_per_class_best.csv: 0.5291, 0.5888 | Verified |
| KPCA reducer fit 5.47 s vs PCA 0.0247 s (221x) | T9c_runtime_compact.csv, n=4,800 train | Verified |
| Traced memory 363 MB vs 9.8 MB (37x) | T9c: whole-pipeline traced peak, KPCA vs original/PCA-10 | Verified. Different definition from T9b (reducer only: about 770x time, 116x memory); the paper uses the T9c definition and says "whole pipeline". Not a discrepancy. |
| SVM cosine-KPCA advantage 0.076 -> 0.021 after tuning | T12_tuning(_both).csv: 0.0761, 0.0206 | Verified; five outer folds only (stated) |
| 23 of 30 Holm p<0.05; Friedman p_holm <= 2.7e-9 | stat_wilcoxon.csv, stat_friedman.csv | Verified (screening only) |
| KPCA projection K_new alpha / sqrt(lambda) | Numerical test vs sklearn KernelPCA.transform: max diff 7e-16 (1/lambda: 0.22) | Verified |
| All numbers in prose unchanged by this revision | Script compared numeric tokens old vs new PDF text: removed/added tokens were only the rewording noted in the changelog (0.003 gap range derived from table 4 values +0.000/-0.002/+0.003) | Verified |
| Page count / template | 15 pages, A4, llncs.cls v2.26 | Verified by compilation; conference template choice (LNCS vs LNNS) unconfirmed |
| References | Abdulhammed, Engelen, Panigrahi, Waghmode, Abdel-Rahman abstracts checked this session; 2025 values for Patil, Abdelaziz, Xu&Liu, Emirmahmutoglu&Atay checked earlier from fetched pages; classic references not re-fetched | Partly verified |
| Originality / AI score | Not measured by an accredited tool | Unverified. No plagiarism-free or detector claim is made. |

## Added items
| Claim | Evidence | Status |
|---|---|---|
| For LR, k-NN, DT, RF none of 20 reduced configs exceeds original accuracy; closest k-NN cosine-30 0.9339 vs 0.9341 | results/v2 cv_results aggregated (standard class weights), recomputed by make_per_algo_fig | Verified |
| SVM: original 0.906; cosine KPCA at 15, 20, 30 comps above it; best 0.924 | same | Verified |
| Descriptions of the ten papers | Abdulhammed, Engelen, Panigrahi, Abdel-Rahman abstracts fetched this session; Ring, Sharafaldin, Arp, Apruzzese, Kuang, Chavan described from titles/abstracts previously checked or from title only (Kuang: KPCA+SVM+GA from the title; predates CIC-IDS2017 by dates) | Partly verified; Kuang's dataset and Ring/Sharafaldin/Arp/Apruzzese details not re-fetched |
