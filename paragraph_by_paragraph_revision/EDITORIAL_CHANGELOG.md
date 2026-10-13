# Editorial changelog (paragraph_by_paragraph_revision)
Base: humanized_manuscript_review/main.tex (16 pages). Edits are applied by `apply_edits.py` (each replaced text matched exactly once).
1. Abstract: memory ratio now says "whole-pipeline traced memory was about 37 times higher" (keeps the definition distinct from the reducer-only scaling run).
2. Introduction: "one of the most used" -> "widely used" (no count supports a ranking).
3. RQ5, Discussion and Conclusion: removed "smaller training sets / training sizes". `results/v2` has no training-size experiment (n_train is 4,800 in every cv_results row), so the claim was unsupported.
4. Related work: Ring entry no longer claims we use the survey to place the dataset; the "four papers" sentence now names what they bear on; duplicated "not exhaustive" sentence removed.
5. Setup: 2,850 fits explained as 190 configurations x 15 folds, including the majority-class baseline.
6. Row-order paragraph: "They assume" -> "Both checks assume".
7. Fig. 11 caption: states the bars are not a like-for-like ranking; figure retained (faculty checklist).
8. Carried over from earlier rounds: Patil et al. "PCA-based feature selection", softened abstract claim on prior studies, IEEE Xplore access statement, Kuang wording.
Not changed: equations, tables' numbers, figures, bibliography, experimental data.
