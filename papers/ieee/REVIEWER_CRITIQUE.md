# Simulated Reviewer Critique (self-assessment)

1. **Only 1000 rows**; 10-17 records per attack class; conclusions about web attacks are fragile. (Major)
2. **No temporal or cross-dataset evaluation**; random CV on CIC-IDS2017 is known to inflate results. (Major)
3. **Model selected and scored on the same CV** - optimistic. (Moderate)
4. **No hyper-parameter tuning**; SVM/LR may be under-fit, which could explain why reduction "helps" SVM. (Moderate)
5. **Sample imputed on full data** before sampling - mild leakage. (Minor)
6. **Repeated-CV p-values** violate independence (Nadeau-Bengio). (Minor, disclosed)
7. **Novelty is limited**: no new method. (Moderate; framed as empirical study)
8. No deep-learning or modern baselines; no comparison to published IDS pipelines on equal splits. (Minor)
Verdict if submitted now: major revision / likely reject at a strong venue; plausible at a workshop or student-track venue.
