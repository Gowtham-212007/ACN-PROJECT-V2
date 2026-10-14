# FINAL AUDIT (14 Oct 2026)
Built from `main.tex` in this folder (copied from paragraph_by_paragraph_revision; edits below). Two PDFs: `submission_authored.pdf` (= final.pdf, author placeholders kept as the user asked) and `submission_blind.pdf` (anonymous). Both 15 pages (after trimming, see below), A4, 0 undefined references. Page count: 15 = within the standard limit; no extra-page fee.
## Review policy
The conference site (cicps27.gcect.ac.in) names Microsoft CMT but does not state single- or double-blind; it gives deadlines 15 Oct 2026 (submission) and 20 Dec 2026 (camera-ready). Policy NOT established -> both variants provided; check the CMT portal or conference@gcect.ac.in.
## Edits in this pass
- Author block: `\ifdefined\BLIND` switch (anonymous vs placeholder block). Repository text likewise.
- LR best-space result: "significant but negligible" replaced by exploratory wording (diff 0.004; Holm p = 0.021 over the five best-space tests; folds share training data).
- k-NN: -0.001 confirmed from unrounded means 0.8005 vs 0.8017 (stat_wilcoxon.csv: -0.001189); sentence now says so.
- Section 5.9: distinguishes Table 1 range (97.75-99.9965 %) from the value plotted in Fig. 4 (99.987 %, lower of Emirmahmutoglu & Atay's two values).
- Figures 3 and 10 narrowed slightly to keep 16 pages with the author block.
## Checked against files
- 30-comparison family: stat_wilcoxon.csv has 30 rows, 6 per classifier (orig vs pca-10/rbf-10/cosine-10; pca-10 vs linear/rbf/cosine-10); one Holm correction over all 30 in src/acn stats script (`w["p_holm"]=holm(w.p_value)`). Matches the text.
- Table 2 class supports sum to 6,000 (computed from T8_per_class_best.csv).
- Headline numbers consistent with earlier claim checks (see CLAIM_AUDIT.md).
## Not resolved
Author names/affiliation/e-mail, repository URL, declarations confirmation, certified plagiarism/AI reports. See AUTHOR_ACTIONS.md. Status: NOT ready for submission until those are done; ready for submission after author confirmation only for the blind variant if the repository link can stay withheld.

Update 14 Oct: author block, institute and running header removed from the default build at the author's request (no author fields; only the repository line remains a placeholder). Add names before camera-ready.

## 15-page trim (14 Oct)
Done by: smaller figures 2/3/4 (0.6/0.72/0.78 text width), tighter float spacing, bibliography in the template's small size unchanged, shorter Discussion RQ paragraph (same content), dropped the middle memory values (3.1 ... 359.1 MB kept as endpoints), removed three duplicated sentences (cross-study prose, external-validity sentence, imbalance-treatment sentence), shortened disclosure/availability wording, removed the anonymous institution line from the blind variant. No empirical number, table or caveat changed. Sentence splits (8 sentences) also applied. Whether the organisers count references within 15 pages is not stated; the PDF is 15 pages in total.

## Emirmahmutoglu & Atay correction (14 Oct)
Table 1: accuracy 99.9965 %; F1 99.987 %. Fig. 4 plots 99.9965. Caption no longer mentions a 'lower of two values'. Section 5.9 rewritten. Kuang DOI added. Rebuilt: authored and blind PDFs both 15 pages.

14 Oct: Section 5.9 range sentence now refers to external studies only (Fig. 4); Fig. 4 caption no longer lists 'metrics' as differing (all bars are accuracy).
