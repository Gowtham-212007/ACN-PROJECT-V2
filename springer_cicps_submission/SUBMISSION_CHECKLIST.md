# CICPS 2027 submission checklist
Official source checked 2026-10-13: https://cicps27.gcect.ac.in/call-for-paper.php (2nd CICPS 2027, 29–30 Jan 2027)

| Item | Status |
|---|---|
| Paper deadline 15 Oct 2026 (earlier 30 Sep struck out, "Final Call"); notification 20 Nov; registration + camera-ready 20 Dec 2026 | confirmed on page |
| Submission system: Microsoft CMT | confirmed on page; **link/account not verified** |
| Page limit: 15 pages (up to 2 extra at INR 500 each) | manuscript is 15 pages incl. references, no paid pages used |
| Template: Springer conference proceedings (LNCS guidelines linked); series "Lecture Notes in Networks and Systems" | official llncs v2.26 used; the page links LNCS, LNNS not named as template — **confirm with organizers** |
| Springer proceedings approval | page states intended outcome only, **not confirmed approval**; no publication/indexing guaranteed |
| Review type (single/double blind) | **not stated** — author names are placeholders; confirm whether to anonymise |
| Fees: INR 7,000 student / 8,000 academic / 9,000 industry per author registration; student rule: first author and presenter must be student/research scholar | on page |
| Track: Security and Privacy | fits |
| Originality: "unpublished, novel, not submitted elsewhere" | **Do not submit the same work to IEEE Access or COMPSAC simultaneously.** |
| AI policy | not stated by conference; disclosure included for human review |
| Plagiarism / AI-content thresholds (<16 % / <20 % per your faculty notes) | NOT measured: only one 343-word excerpt tested on a free checker (0.00 %); run an authorised checker |

## Unresolved items (blockers) — only the authors can supply
1. Author names, department/institution, city, country, corresponding author, email.
2. Repository URL / archive DOI (placeholder in abstract and Data availability).
3. Confirm AI-disclosure accuracy and any other tool used.
4. Confirm originality: no earlier publication/submission of this work (the manuscript no longer mentions earlier 1,000-record experiments).
5. Funding / acknowledgments / competing-interest statement.
6. Springer copyright/consent forms at camera-ready.
7. Certified plagiarism and AI-content reports if the faculty requires them.
8. IEEE Xplore papers (faculty note) — none could be retrieved; add if required.

Readiness: **provisionally formatted; not ready to submit until items 1–5 are done.**

## Similarity check log (2026-10-13)
- Free checker (HireQuotient): 343-word excerpt, 0.00 % (open web only).
- Exact-phrase web searches of 8 more distinctive sentences from the new Springer sections (related work, algorithm/formulas text, limitations, discussion): no verbatim match found. Combined with earlier searches, about 15 distinct sentences have been searched in total.
- No tool in this session produces a full-document similarity percentage; browser-based checkers were not connected. Search engines do not index everything, so this is not proof of low similarity.
- Self-overlap warning: this manuscript shares most text with the IEEE Access / COMPSAC / A4 versions in this repository. If any of those is submitted or posted anywhere, a checker will flag this paper against it. Submit only one.

## Local n-gram similarity check (2026-10-13, `src/acn/simcheck_local.py`)
Manuscript text (6,466 words, references excluded) compared with the downloaded full texts of 14 sources: Xu & Liu (arXiv), Waghmode et al., Patil et al., Abdel-Rahman et al., Abdelaziz et al., Emirmahmutoğlu & Atay, Chavan & Alone, Sharafaldin et al., and the scikit-learn (decomposition, cross-validation, metrics) and Wikipedia (PCA, KPCA) pages.
- Word 8-gram matches: **0** (0.00 % of the text).
- Word 5-gram matches: 42 words (**0.65 %**), all generic phrases ("decision tree and random forest", "network intrusion detection systems", "the authors declare no competing interests").
- Not compared (download failed or paywalled): Engelen et al., Abdulhammed et al., Kuang et al., Ring et al., Arp et al., Apruzzese et al., Nadeau–Bengio. This is NOT a database check like Turnitin/iThenticate and says nothing about unindexed or unseen sources.

## Similarity sweep, Europe PMC full-text phrase search (2026-10-13)
- 150 sentences (>=14 words) from main.pdf, 288 exact-phrase queries (words 2-10 and last 9 of each sentence), 0 errors.
- 6 phrases returned hits, all generic wording matching unrelated biomedical papers: "feature vectors with the same or with different" (3), "we report means and standard deviations over the" (4), "and use the tests for screening not as" (26), "which may explain why they are hard to" (3), "reviewed the content and remain fully responsible for" (1), "no competing interests TO BE CONFIRMED BY THE" (37).
- No hit from an IDS/CIC-IDS2017 paper. Coverage limit: Europe PMC indexes mostly biomedical/open-access text, so this is weak evidence for computer-science sources.
- This is NOT a certified score. Only institutional Turnitin/iThenticate (or Crossref Similarity Check) can certify <16 %.
