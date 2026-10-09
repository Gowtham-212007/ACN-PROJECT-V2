# IEEE Access Submission Checklist
Done by me (verified in this session):
- [x] Official 2026-05 IEEE Access LaTeX template, `\documentclass{ieeeaccess}`; compiles with `papers/ieee/build_access.sh` (pdfTeX, no LaTeX errors, no undefined references; overfull-box warnings of the same kind as the template's own log).
- [x] PDF: 10 pages, fonts embedded, abstract 242 words (150-250), keywords alphabetical, all tables/figures render (inspected page images).
- [x] Source and PDF correspond (same build).
- [x] Limitations 1-9 present (stratified/not prevalence-preserving; small minority support; one dataset/one sample; exact-duplicate removal != near-duplicate/session leakage; no cross-dataset; limited tuning; proxy-chronology only; no new algorithm; no SOTA/real-time/production claim).
- [x] AI disclosure in Acknowledgment (system, sections, level of use).
- [x] 232/232 claim checks; numerical match of prose to results (2 external numbers: Python version, cited 99.6%).
- [x] References: 17/17 metadata verified; citation keys consistent; three sources only partly read (see FINAL_REFERENCE_AUDIT).
- [x] Anonymity is NOT required (IEEE Access is not described as double-blind on the pages checked); author names are required.
Authors must do:
- [ ] Fill every `TO BE FILLED` field (names, affiliations, e-mails, ORCID, biographies, funding, repository URL).
- [ ] Confirm/edit AI disclosure; delete the bracketed confirmation sentence.
- [ ] Run Crossref Similarity Check / iThenticate or institutional equivalent.
- [ ] Proofread English (IEEE Access rejects poor grammar); optionally use a language-editing service.
- [ ] Confirm originality and no concurrent submission; read IEEE Access duplicate-submission and preprint policies.
- [ ] Re-download the template on the day of submission if IEEE has updated it (version used: 20260513).
- [ ] Create IEEE author-portal account and ORCID; upload .tex + figures/tables + PDF (source and PDF must match); pay APC or confirm institutional account.
- [ ] Deposit code/results (e.g., Zenodo) and put the URL/DOI in the Data and Code Availability section.

## Alternative layout supplied by the user (sample paper from a 2024 IEEE conference)
`ACN_PAPER_IEEE_CONFERENCE_A4.tex/.pdf`: same content and numbers as IEEE_ACCESS_FINAL, re-typeset in the IEEEtran conference layout on A4 (title, numbered author blocks, "Abstract-", "Index Terms-", Roman-numbered headings), compiled with `ieeetran/IEEEtran.cls` (CTAN v1.8b). The conference-specific footer/ISBN/DOI line of the sample is NOT reproduced; the organisers' own template and page limit must be checked for the actual target conference. Author fields are placeholders. Only the layout of the sample was used; none of its text.
