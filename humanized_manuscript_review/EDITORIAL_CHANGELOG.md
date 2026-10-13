# Editorial changelog (humanized_manuscript_review)

Base: `../springer_cicps_submission/main.tex` (15 pages, A4, official LNCS class v2.26). Left unchanged. All edits are scripted in `apply_revision.py`, which asserts that every replaced passage exists exactly once. Purpose: clearer, more specific, observation-first prose. Not to evade detectors; the AI-assistance disclosure is unchanged.

## Diagnosis
- Abstract: long, listed methods before findings, "matched" for LR/k-NN was true only at the best component count.
- Results 5.2/5.4/5.7: restated many table entries and mixed observations with test statistics in single paragraphs.
- Discussion: one untested sentence; no interpretation of why originals win or why the SVM differs.
- Related work: claimed "most report accuracy on one split" which not all sources support (Abdelaziz et al. use repeated CV).
- Section 5.9: said other studies' accuracies "show" that accuracy coexists with weak minority-class detection; they do not (only our per-class results do).

## Changes
| Section | Change | Reason |
|---|---|---|
| Abstract | Rewritten: question, scope, sample caveat, headline results, SVM exception, cost, limits. "At best matched" for LR/k-NN. Cost ratios stated as "more than 200 times" / "about 37 times". | Precision and consistency with the results. |
| Related work | Replaced the "most report accuracy on one split" claim with "among the studies we read, none pairs..."; added that our reading was not exhaustive and that the dataset papers bear on score trust, not on reduction. | Avoid an unsupported gap claim. |
| 5.1 | Observation first (majority baseline, RF accuracy vs macro-F1, class groups); Engelen explanation marked as untested here. | Clarity; no new claims. |
| 5.2 | Split into two paragraphs: (1) n=10 comparison, tests labelled screening evidence; (2) best-reduced-space comparison with its selection bias. | Separate observation, test, and caveat. |
| 5.3 | Merged heading and text into one sentence plus Fig. 2. | Space. |
| 5.5 (tuning) | Condensed k-NN/SVM detail; same numbers (0.668/0.791, 0.745/0.812, 0.076 to 0.021). | Readability. |
| 5.6-5.8 | Shorter wording; computational ratios defined (reducer fit time vs PCA; whole-pipeline traced memory vs PCA or no reduction). 64 TB kept as arithmetic only in 5.8. | Preserve benchmark definitions. |
| 5.9 | "These figures are not comparable"; only our own accuracy/F1 pair illustrates the accuracy issue. | Fix overreach. |
| Discussion | "Why accuracy misleads" shortened; new "Possible explanations (untested)" with three explicit hypotheses (tree axis-aligned splits, variance vs separability of rare classes, default RBF-SVM mismatch). | Labels hypotheses as hypotheses. |
| Limitations | Timing caveat merged here; closing paragraph rephrased. All six limitations retained. | No caveat weakened. |
| Conclusion | Answers RQ1-RQ5 directly, no new results. | As requested. |

## Not changed
Methods, equations (KPCA projection uses 1/sqrt(lambda), numerically checked against scikit-learn), tables, figures, bibliography, AI disclosure, placeholders.

## Additions requested after the first revision (apply_additions.py)
- Related work now has one short entry for each of the ten non-table papers (Ring; Sharafaldin; Engelen; Panigrahi and Borah; Abdulhammed; Kuang; Abdel-Rahman; Chavan and Alone; Arp; Apruzzese), grouped as dataset quality, dimensionality reduction, evaluation methodology. Each entry says what the paper contributes and how it relates to this study. The five 2025 studies stay in Table 1.
- New subsection "Accuracy of each algorithm across feature spaces" with Fig. 3 (`fig12_per_algorithm_accuracy`, built by `src/acn/make_per_algo_fig.py`): one panel per classifier, accuracy for PCA and three KPCA kernels at 5-30 components, dashed line = original features. The combined macro-F1 chart (Fig. 2) and the cross-study accuracy chart (now Fig. 4) remain.
- Result: 16 pages (one over the 15-page base limit). The call for papers allows up to two extra pages at INR 500 each.
