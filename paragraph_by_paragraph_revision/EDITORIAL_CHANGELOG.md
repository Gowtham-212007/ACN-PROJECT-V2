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

## 14 Oct 2026 (after external audit)
- Emirmahmutoglu & Atay (FPA+RF, CSE-CIC-IDS2018): an external reviewer reports the source gives 99.987 % (results) and 99.9965 % (conclusion). My own fetch of the Springer page showed only the abstract (0.99987, labelled F1) and was truncated before the results/conclusion, so I could NOT confirm which is accuracy. Table now states "99.987--99.9965 % (source gives both)"; Fig. 11 plots the lower value (99.987) with 3-decimal label; running text says 97.75--99.99 %; caption notes the lower value is plotted. Authors should open the paper's results table and state one value.
- Methods: "the nested analysis removes that bias" -> "addresses this bias by scoring the selection on unseen outer folds".
- Kept "PCA-based feature selection" for Patil et al. (source's own label; checklist asked for it). Reviewer suggests "PCA (20 components)"; I could not confirm which is correct from the source, so the author should decide.
- Trimmed three sentences and narrowed figs 10-12 to hold 16 pages.

## 14 Oct 2026 – voice pass
Rephrased ~11 sentences (introduction opening and problem statement, per-class gap sentence, "why accuracy misleads", hypothesis (i), limitations lead-in, scope statement, conclusion opening/closing, two results phrasings) for natural flow. Numbers, citations, equations and limitations unchanged. Not a detector-evasion exercise; the AI-assistance disclosure is retained and no detector score is claimed. Remaining sentences were already rewritten in earlier plain-language passes.
