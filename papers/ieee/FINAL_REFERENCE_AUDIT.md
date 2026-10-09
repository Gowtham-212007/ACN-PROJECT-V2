# Final Reference Audit (IEEE Access manuscript)
Date: 2026-10-09. Method: Crossref/publisher/arXiv/USENIX/JMLR pages; full text read where marked. "Metadata" = authors, title, venue, year, volume/issue, pages/article no., DOI.

| # | Key | Metadata | What was actually read | Citing statements | Verdict |
|---|---|---|---|---|---|
| 1 | ring2019 | verified (Comput. Secur. 86:147-167, doi:10.1016/j.cose.2019.06.005) | arXiv abstract page | datasets survey; 15 properties | supported |
| 2 | sharafaldin2018 | verified (ICISSP, pp.108-116, doi:10.5220/0006639801080116) | publisher metadata | dataset introduced; used for dataset provider | supported. "78 features" is attributed to the MachineLearningCVE files, not to this paper |
| 3 | engelen2021 | verified (SPW 2021, pp.7-12) | **full text** (KU Leuven) | appendix artefacts ~25%, attempted flows, corrected release, web brute-force/XSS without forward payload | supported (wording paraphrased) |
| 4 | panigrahi2018 | verified (IJET 7(3.24):479-482, doi:10.14419/ijet.v7i3.24.22797) | publisher abstract | shortcomings + combined dataset | supported; "labelling/flow-construction" is covered by Engelen, Panigrahi only for "shortcomings" |
| 5 | arp2022 | verified (USENIX Sec. 2022, pp.3971-3988) | **full text** | pitfalls -> unrealistic performance | supported |
| 6 | abdulhammed2019 | verified (Electronics 8(3):322) | MDPI page, ~92% (abstract, method; **Results/Conclusion not read**) | auto-encoder + PCA, 81->10 features, ~99.6% accuracy, classifiers RF/BN/LDA/QDA | Sentence reworded to what the abstract supports; 99.6% is **not** attributed to RF or to a single method. Per-classifier results still unverified |
| 7 | scholkopf1998 | verified (Neural Comput. 10(5):1299-1319) | Crossref | KPCA definition | supported (does not cover cosine kernel/sklearn defaults; not claimed) |
| 8 | kuang2014 | verified (Appl. Soft Comput. 18:178-184, doi:10.1016/j.asoc.2014.01.028) | **abstract and full text NOT accessible** (ScienceDirect 403); secondary survey (arXiv 2209.05579 Sec. 4.1): KPCA as SVM preprocessor, GA tunes SVM parameters | "KPCA combined with SVM for intrusion detection"; "hybrid model combining KPCA, an SVM and a genetic algorithm" | claims kept minimal (title-level); supported by title + secondary survey only. Not claimed: dataset, GA role |
| 9 | apruzzese2022 | verified (IEEE TNSM 19(4):5152-5169, doi:10.1109/TNSM.2022.3157344) | abstract (via earlier check); an arXiv lookup this session hit the wrong paper and was discarded | cross-evaluation framework | supported at abstract level |
| 10 | pedregosa2011 | verified (JMLR 12:2825-2830) | JMLR page | scikit-learn | supported |
| 11-15 | cortes1995, cover1967, quinlan1986, breiman2001, chicco2020 | verified via Crossref (pages as in bib; Chicco BMC Genomics 21:6) | metadata only | cited as method references / MCC for binary case | supported as method citations; settings (k=5, C=1...) are ours |
| 16 | demsar2006 | verified (JMLR 7:1-30) | abstract | Wilcoxon/Friedman procedures | supported |
| 17 | nadeau2003 | verified (Mach. Learn. 52(3):239-281) | **working-paper version** CIRANO 99s-25 and NIPS 1999 abstract; the Springer journal PDF was not retrievable | overlapping training sets -> correlated estimates, liberal naive tests | supported in substance; text now says the correction is derived for random subsampling and is not applied here |

Result: 17/17 metadata verified; every `\cite` key exists in the bibliography and every entry is cited (checked by script). **Not fully read:** Kuang et al. (abstract/full text), Abdulhammed Results section, Nadeau & Bengio journal version. Claims about these were weakened accordingly. No source was fabricated. DOIs were verified where present; entries without DOI (older/classic items) were not given one.
