# Literature Gap (only verified, real references; see `references.bib`)

- Kernel PCA for intrusion detection is widely reported with accuracy gains, but most studies (a) evaluate a single random split, (b) omit an original-feature baseline, (c) report accuracy/weighted metrics on imbalanced data, (d) do not test significance.
- CIC-IDS2017 has documented labelling and construction problems (Engelen et al.), so high numbers on random splits are not evidence of deployability.
- Gap addressed here: a controlled, leakage-free comparison (original vs PCA vs KPCA, same classifiers and folds, cost and statistics) on a small stratified sample.
- Gap NOT addressed: temporal/cross-dataset generalisation, full-data scale, hyper-parameter tuning, deep models.
- Novelty is modest and honest: a rigorous negative/qualified result, not a new algorithm.
