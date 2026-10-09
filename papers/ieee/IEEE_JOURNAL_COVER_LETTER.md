**Draft cover letter - IEEE Access** (to be completed and signed by the corresponding author)

Dear Editor,

Please consider our manuscript, "Does Dimensionality Reduction Help Classical Intrusion Detection? Original Features versus PCA and Kernel PCA on a De-duplicated CIC-IDS2017 Sample", for publication in IEEE Access.

**Question.** Kernel PCA and PCA are often used before classical classifiers in network intrusion detection, but gains are usually reported as accuracy on a single split and without a no-reduction baseline. We ask whether reduction helps at all on CIC-IDS2017 once the evaluation is made class-aware and leakage-controlled.

**Contribution.** This is an empirical comparison, not a new algorithm. On a 6,000-record, class-stratified sample drawn from all eight CIC-IDS2017 files after exact-duplicate removal, we compare original features, PCA and kernel PCA (linear, RBF, cosine; 5-30 components) across five classifiers, with training-fold-only preprocessing, repeated and nested cross-validation, a small nested hyper-parameter search, two row-order robustness checks, per-class analysis and a runtime/memory measurement.

**Findings.** A random forest on the original features had the highest observed macro-F1 (0.901 +- 0.020; nested 0.900 +- 0.022). Original features were clearly better than PCA/KPCA for decision tree and random forest and about equal for logistic regression and k-NN; the only benefit of reduction, for the RBF-SVM, shrank from 0.076 to 0.021 after tuning. Accuracy (0.972) hid poor and mutually confused detection of two web-attack classes (F1 0.53 and 0.59). Exact KPCA cost over 200 times more fit time and about 37 times more traced memory than PCA at n = 4,800.

**Limitations (stated in the paper).** One dataset and one class-stratified, not prevalence-preserving sample; very small support for some classes; no cross-dataset evaluation; limited tuning; exact de-duplication does not remove near-duplicate or session-level leakage; the CSVs have no timestamps, so the row-order checks are proxy-chronology checks, not verified temporal validation. We make no state-of-the-art, real-time or production-ready claim.

**Suitability.** IEEE Access publishes original research across IEEE fields of interest and covers computational intelligence and communications/security topics; we believe a carefully qualified empirical study with released code fits that scope. [Editors to judge; no acceptance is assumed.]

**Declarations (to be completed only by the authors if true):** [originality / not under consideration elsewhere]; [competing interests]; [funding]; AI-assistance is disclosed in the Acknowledgment. Suggested reviewers: [optional].

Sincerely,
[NAME, AFFILIATION, E-MAIL, ORCID - TO BE FILLED]
