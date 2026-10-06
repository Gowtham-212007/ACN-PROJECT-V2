# Simulated Reviewer Critique (updated after hardening)

1. **Only 1,000 rows; 10-17 records per attack class.** Web-attack conclusions rest on 10-11 records. (Major, unfixable without raw data)
2. **No temporal / cross-dataset / held-out evaluation.** Random CV on CIC-IDS2017 can inflate scores. (Major)
3. **Residual pre-sampling imputation leak** in the cached sample. Disclosed; effect unmeasured. (Moderate)
4. **Selection optimism** - now quantified with nested CV (~0.008 macro-F1), but the nested estimate itself is noisy (2-3 records per rare class in inner folds). (Minor, mitigated)
5. **No hyper-parameter tuning**; SVM and RBF-KPCA conclusions are about default settings. (Moderate)
6. **Repeated-CV p-values are not independent**; nested p-values are unadjusted. (Minor, disclosed)
7. **Novelty limited**; no new method. (Moderate; framed as an empirical study)
8. **Literature coverage is thin** (17 refs, no systematic survey; some sources only partly re-read). (Moderate)
9. No modern/deep baselines; no comparison with published pipelines on equal splits. (Minor)
Verdict: not ready for a strong venue; plausible for a workshop/student-track venue after fixing items 1-3 where possible.
