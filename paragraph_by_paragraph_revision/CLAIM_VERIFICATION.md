# Claim verification
| Claim | Source | Status |
|---|---|---|
| RF original acc 0.972+-0.004, macro-F1 0.901+-0.020 | results/v2 cv_results / T4, earlier claim_check | verified earlier, unchanged |
| Nested 0.900+-0.022 | results/v2/nested_summary.csv | verified earlier |
| Web brute force / XSS F1 0.53 / 0.59 | T8_per_class_best | verified earlier |
| SVM cosine-KPCA advantage 0.076 -> 0.021 | T12_tuning | verified earlier |
| KPCA fit 5.47 s vs PCA 0.0247 s (>200x, n=4,800); traced memory 363 vs 9.8 MB (~37x, whole pipeline) | T9/T9c | verified earlier; reducer-only T9b ratios differ by definition |
| 2,850 fits = 190 configs x 15 folds incl. 1 majority-class baseline | cv_results_20261006_184913.csv (checked this round: 2,850 rows; DUMMY = 1 config) | verified |
| "Smaller training sets" robustness | no such experiment in results/v2 | UNSUPPORTED - removed from text |
| Reference descriptions (Ring, Sharafaldin, Arp, Apruzzese, Engelen, Panigrahi, Abdulhammed, Waghmode, Abdel-Rahman) | abstracts read earlier | verified at abstract level |
| Kuang | Crossref metadata only; abstract unreadable | metadata-level only |
| Table 1 values (Patil, Abdelaziz, Xu & Liu, Emirmahmutoglu, Waghmode) | publisher/arXiv pages earlier | verified earlier; not re-fetched this round |
Not checked this round: full bibliography formatting, plagiarism/AI-detector scores (none certified).
| Emirmahmutoglu FPA+RF accuracy | Springer page fetched: abstract only (0.99987 labelled F1), results/conclusion not reached; reviewer reports 99.987 % vs 99.9965 % | UNRESOLVED - both shown in table, lower plotted |
