# REFERENCE AUDIT
Verified at abstract/metadata level earlier in the session (Crossref, arXiv, Europe PMC, Semantic Scholar): Ring (arXiv 1903.02460), Arp (2010.09470), Apruzzese (2203.04686), Sharafaldin (PDF abstract), Engelen, Panigrahi, Abdulhammed, Waghmode (Sci Rep abstract), Abdel-Rahman.
This pass: Patil et al. (Informatica, abstract fetched): 99.98 % Extra Trees with information gain (24 features); abstract lists "PCA, 20 features" as a feature-selection method, no PCA accuracy range in the abstract. The 99.58-99.96 % range was verified earlier / by an external reviewer from the full text, not re-fetched now.
Emirmahmutoglu & Atay: Springer page fetch showed only the abstract (0.99987, labelled F1) and was truncated; the 99.987 % (results) / 99.9965 % (conclusion) locations come from an external reviewer and are UNCONFIRMED by me.
Kuang: Crossref metadata only; abstract unreadable.
Xu & Liu, Abdelaziz: values verified earlier; not re-fetched this pass.
Not verified: page numbers/DOIs of every bib entry beyond Crossref-checked ones; IEEE Xplore pages (not accessible).

## Update 14 Oct (external re-check, uploaded by the author)
Waghmode 99.5 % (Sci Rep); Patil 99.98 % (IG+Extra Trees, 24 features) and 99.58-99.96 % PCA-based (full paper); Abdelaziz weighted-F1 99.8 %, macro-F1 93.31 % (26 features); Xu & Liu MLP 97.75 % on overall test set (Table II); Kuang abstract: KPCA + multilayer SVM + modified RBF kernel + GA, KDD Cup 99 -> DOI 10.1016/j.asoc.2014.01.028 added to the bib. Emirmahmutoglu & Atay: the two values are different metrics (accuracy 99.9965 % in Section 5.4; F1 99.987 % in Table 4/abstract) - NOT conflicting accuracies; manuscript corrected (Table 1, Fig. 4 plots 99.9965, Section 5.9, caption). Status of these claims: reported by an external reviewer, abstract-level F1 label confirmed by me; full-text Section 5.4 not independently fetched.
