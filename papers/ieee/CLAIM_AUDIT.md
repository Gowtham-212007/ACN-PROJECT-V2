# Claim Audit (paper claims vs evidence)

| Claim | Evidence file | Status |
|---|---|---|
| RF on original features is best: macro-F1 0.722+-0.058, acc 0.952, MCC 0.894 | results/tables/T7, selected_model.json | Supported (selection on same CV: optimistic) |
| Original features beat every reduction for LR/DT/RF on macro-F1 | T7, stat_wilcoxon.csv | Supported |
| KNN shows no meaningful difference between spaces | T7, stat_friedman.csv (p=0.0099 Holm, small effects) | Supported with caution |
| Only SVM benefits from reduction (cosine KPCA-30) | T6, T10b | Supported |
| Linear KPCA = PCA (diff <= 0.011 macro-F1) | T5/T6 | Supported |
| Cosine vs PCA significant only for LR | stat_wilcoxon.csv | Supported |
| Accuracy 0.95 hides macro-F1 0.72; web attacks weakest | T8 | Supported |
| KPCA costs more time/memory (RF train 0.36-0.38 s vs 0.19 s; ~11.7 vs 1.7 MB) | T9c | Supported (single machine) |
| Results generalise to other days/datasets | none | **NOT claimed** |
| Results hold on the full 1.3M-row data | none | **NOT claimed** |
| p-values are exact | repeated CV is correlated | Stated as optimistic |
