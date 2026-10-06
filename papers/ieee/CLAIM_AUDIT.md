# Claim Audit (re-run after the hardening pass)

All numerical claims are recomputed from raw result files by `python -m src.acn.check_claims`
(output: `results/tables/claim_check.csv`; **104 checks, 0 failing**). Nested-CV numbers come from `results/raw/nested_*.csv`.

## A. Numerical claims (abstract, results, discussion, conclusion)
| Claim | Source | Status |
|---|---|---|
| RF/original: acc 0.952+-0.010, macro-F1 0.722+-0.058, MCC 0.894+-0.022, W-F1 0.947, bAcc 0.717 | cv_results | verified |
| Majority baseline acc 0.718, macro-F1 0.076, MCC 0 | cv_results | verified |
| Nested macro-F1 0.715+-0.044 (acc 0.945, MCC 0.880); optimism 0.008; orig config chosen in 15/15 outer folds | nested_* | verified |
| Accuracy-macro-F1 gap 0.23 | cv_results | verified (earlier draft said 0.24: **corrected**) |
| 17 of 30 Holm-significant; orig better in all significant comparisons involving it; RBF worse than PCA for LR,SVM,DT,RF; cosine vs PCA significant only for LR | stat_wilcoxon | verified |
| Best-reduced comparison: orig wins LR/DT/RF (Holm p<0.01); KNN n.s.; SVM cosine-30 0.388->0.510 (p_Holm 0.0003, all 15 folds) | stat_best_reduced | verified (same-CV, optimistic - stated) |
| Nested: DT +0.077, RF +0.071 (p<=0.002), LR +0.019 (p=0.055), KNN +0.010 (p=0.28), SVM -0.049 (reduced better, p<0.001) | nested_summary | verified; LR claim is **weaker than same-CV** and is worded as modest/non-significant |
| Linear KPCA vs PCA: identical for KNN/SVM, <=0.001 LR, <=0.011 DT, <=0.015 RF | cv_results | verified (earlier "<=0.011 overall" was **wrong; corrected**) |
| Kernel spread > component spread for KNN, DT, RF; not for LR, SVM | cv_results | verified (earlier "most classifiers" was an **overstatement; corrected**) |
| Web-attack F1 0.21-0.50 on 10-11 records; slow-DoS recall 0.57-0.71; 5 classes F1>=0.96 | T8 | verified |
| KPCA fit 0.09-0.12 s vs PCA 0.01 s; DT 0.016->0.09-0.10; RF train 0.21->0.36-0.38; RF infer 0.007->0.014-0.016; memory 11.7 vs 1.7 MB (x7) | runtime csv | verified (single machine) |
| Memory 3.1/6.4/11.0/16.8 MB at n=400/600/800/1000, slope ~1.9 | kpca_scaling | verified; "quadratic" now "roughly"; timing exponent not claimed |
| 14 TB | arithmetic 1,308,978^2 x 8 B = 13.7 TB | **theoretical estimate**, labelled as such; 1.3 M flows taken from the project README, not recomputed |
| Orig highest mean macro-F1 at 400/600/800 training records for LR,SVM,DT,RF | size_results | verified |

## B. Citation audit (sources opened and read on 2026-10-06 unless noted)
| Key | Claim in paper | Verdict |
|---|---|---|
| sharafaldin2018 | CIC-IDS2017 introduced there; ICISSP 2018 pp.108-116 | well-known; bibliographic data not re-opened this pass |
| ring2019 | survey of NIDS datasets and their suitability | supported (title/abstract level; bibliographic data not re-opened) |
| engelen2021 | TCP-appendix artefacts ~a quarter of flows (25.9%), attacks without malicious payload, shortcut learning, corrected dataset released; SPW 2021 pp.7-12, DOI | **verified** against full text and imec record |
| panigrahi2018 | describes shortcomings of CICIDS2017 and presents a combined dataset; IJET 7(3.24) 479-482 | **verified** against publisher abstract |
| abdulhammed2019 | AE and PCA on CICIDS2017, 81 -> 10 features, 99.6% accuracy, RF/BN/LDA/QDA | **verified** against MDPI abstract |
| kuang2014 | hybrid KPCA+SVM+GA for intrusion detection; Appl. Soft Comput. 18:178-184 | bibliographic data **verified** (Crossref); only the title was available, so the paper makes no claim beyond the title |
| apruzzese2022 | cross-evaluation framework (XeNIDS) over several datasets, potential and risks | **verified** (abstract); earlier wording ("show that cross-dataset evaluation reveals ...") **softened** |
| arp2022 | pitfalls in ML for security can lead to unrealistic performance | title/venue known; wording reduced to "can lead to"; full text not re-read this pass |
| chicco2020 | MCC advantages (binary) | scope **corrected**: cited for binary case; multi-class MCC is the scikit-learn generalisation |
| demsar2006 | non-parametric tests for comparing classifiers | scope **corrected**: designed for multiple data sets; caveat added |
| nadeau2003 | CV-based inference has variance/dependence problems | used only for the independence caveat |
| scholkopf1998, cortes1995, cover1967, quinlan1986, breiman2001, pedregosa2011 | method attributions | standard references, used only to name the methods |
| (removed) | "many studies omit the no-reduction baseline" | **unsupported by any cited source - removed** |

Not verified this pass: Arp et al. full text, Ring et al. full text, Kuang et al. abstract, page numbers of the classic references. Re-check before submission.

## C. Claims deliberately NOT made
Generalisation to other days/datasets; full-data results; state-of-the-art, real-time or deployable performance; leakage-free evaluation; that KPCA is useful in general.


---
## v2 addendum (raw-data run)
`ACN_RUN=v2 python -m src.acn.check_claims` recomputes 232 numeric claims from `results/v2`; **0 failing**. Fixes made in this pass: Infiltration F1 text 0.88 -> 0.875; kernel-matrix size stated in decimal MB (4800^2*8/1e6 = 184). The v1 checks remain in `src/acn/check_claims_v1.py`. Sections A/B above (citation audit) were not re-verified in v2; unverified sources remain unverified. Not covered by the checker: prose interpretations and the row-order assumption.
