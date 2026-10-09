# Literature Gap (only references that exist; see CLAIM_AUDIT.md section B for what was verified)

- Cited work on dimensionality reduction for CIC-IDS2017 / intrusion detection (Abdulhammed et al.; Kuang et al.) reports PCA/auto-encoder or KPCA+SVM pipelines. We did **not** survey the field, so we make **no claim** about how common single splits, missing baselines or accuracy-only reporting are across the literature.
- Cited evaluation-practice work (Arp et al.; Apruzzese et al.; Engelen et al.; Panigrahi and Borah) motivates why random-split accuracy on CIC-IDS2017 should be treated with caution.
- Gap addressed: a controlled comparison of original features vs PCA vs KPCA (three kernels, five component counts) with identical folds, class-aware metrics, cost and a nested-CV check of selection optimism, on a small sample.
- Gap NOT addressed: temporal/cross-dataset generalisation, full-data scale, hyper-parameter tuning, deep or approximate-kernel models, systematic survey of prior KPCA-IDS results.
- Contribution is a rigorous qualified/negative result, not a new algorithm.
