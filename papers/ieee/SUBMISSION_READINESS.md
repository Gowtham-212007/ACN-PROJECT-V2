# Submission Readiness - IEEE Access (journal), target 2026-10-15

## Status: **READY AFTER AUTHOR INPUTS** (technical package complete; not submittable until the placeholders are filled)

Not submitted, not accepted, not certified plagiarism-free, not approved by IEEE.

## Blockers that only the authors can resolve
See reports/AUTHOR_INFORMATION_REQUIRED.md: author names/affiliations/e-mails/ORCID/biographies, funding & declarations, repository URL, confirmation of the AI-disclosure paragraph, confirmation of originality (no prior publication of the 1,000-record experiment, no concurrent submission), APC arrangement. The PDF currently contains 14 visible `TO BE FILLED` placeholders.

## Verified about IEEE Access (official pages fetched 2026-10-09)
Official LaTeX template (ACCESS_latex_template_20260513, class `ieeeaccess`) used; source + matching PDF both required, <=40 MB, double-column; abstract 150-250 words in one paragraph (template text); keywords alphabetical; every author needs a short biography; submitting author needs a public, populated ORCID; AI content disclosed in Acknowledgments naming system and sections; APC $2,160 + taxes with IEEE-member/institution discounts; portal listed on the journal site: https://ieee.atyponrex.com/journal/ieee-access. **Not verified:** preprint policy, duplicate-submission page, exact current peer-review criteria, whether the portal asks for further declarations. Scope fit: IEEE Access is a multidisciplinary gold open-access journal for original research; an empirical NIDS study is within scope, but acceptance is not predictable.

## Scientific status (unchanged results)
Findings reproduced from code: 232/232 claim checks pass; numbers in the text matched to result files (FINAL_NUMERICAL_AUDIT.md). Qualified conclusion kept. Remaining scientific weaknesses (disclosed in the paper): one dataset and one sample; small minority-class support; limited tuning; no cross-dataset test; proxy-chronology only; near-duplicate/session leakage not removed; Kuang/Abdulhammed(results)/Nadeau-Bengio(journal) full texts not read.

## Package state
- Manuscript: papers/ieee/IEEE_ACCESS_FINAL.tex/.pdf (10 pages, official template, fonts embedded, 242-word abstract), references.bib (+ thebibliography embedded in the .tex).
- Audits: FINAL_NUMERICAL_AUDIT, FINAL_REFERENCE_AUDIT, PLAGIARISM_AND_ORIGINALITY_AUDIT (no certified score), AI_DISCLOSURE_AND_WRITING_AUDIT, reports/FINAL_PROJECT_AUDIT.
- Older conference/COMPSAC drafts and earlier readiness documents moved to papers/ieee/archive/ (kept for provenance; not final).
- Git: commits exist locally; they could not be pushed (GitHub access for the repo was refused).

## Revision after external review of the COMPSAC review PDF (2026-10-09)
Fixed in all versions (Access, A4 conference, COMPSAC review/camera-ready): (1) tuning table now compares like with like (separate best reduced space for default and tuned, plus default gap in the tuned-best space; k-NN default gap 0.000 with cosine KPCA-30, +0.003 in PCA-30); (2) Tables III and VI are full-width (`table*`), no 4-5 pt scaling; (3) p-values below 0.001 shown as `<0.001`; (4) confusion matrix labelled "first repeat" consistently; (5) duplicate wording: exact same-label duplicates removed, 698 conflicting-label feature groups remain in the pool, none in the 6,000 sample (checked: no two sample records share a feature vector); Friedman results now reported with the dependence caveat. Numerical claim check: 0 failing. Still not claimed submission-ready: author inputs, AI-disclosure confirmation, certified similarity check and an anonymous reviewer-accessible archive remain open.
