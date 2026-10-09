# COMPSAC 2027 - SEPT - Submission Checklist

Files: `COMPSAC_SEPT_2027_REVIEW.pdf` (anonymous, source `COMPSAC_SEPT_2027_REVIEW.tex`) and `COMPSAC_SEPT_2027_CAMERA_READY.tex` (placeholders for authors/repo). Both are generated from `paper.tex` and share the same tables/figures/numbers.

## 1. Venue rules - what was verified (official COMPSAC 2027 pages, fetched 2026-10-07)
| Item | Status | Source |
|---|---|---|
| COMPSAC 2027: Tokyo, 13-16 Jul 2027 | verified | ieeecompsac.computer.org/2027/call-for-papers |
| Full-paper deadline 31 Jan 2027; decisions 7 Apr 2027; camera-ready 1 Jun 2027 | verified | same |
| Full paper 10 pages, **inclusive of tables, figures, appendices and references**; +2 pages possible at $125/page | verified | .../2027/information-for-authors |
| Double-blind: remove names, affiliations, contacts; redact references to authors' names/affiliations/prior works | verified | same |
| AI-generated content (text, figures, images, code) must be disclosed in the acknowledgments | verified (wording quoted from the page) | same |
| IEEE template (Word/LaTeX/Overleaf), US Letter, IEEE Cross Check screening | verified | CFP page |
| **SEPT 2027 track page** (chairs, topics, exact submission link) | **NOT verified** - the SEPT pages found were for 2022/2026 (2026 used EasyChair, `compsac2026`); the 2027 track page/portal must be confirmed by the authors before uploading | - |

## 2. Format
- [x] IEEEtran v1.8b `conference` option (CTAN), US Letter 612x792 pt.
- [x] Review PDF = **9 pages** (limit 10 incl. references and acknowledgments); no undefined references, no LaTeX errors, no overfull boxes.
- [ ] Authors: re-check against the official IEEE conference template download on the day of submission (IEEEtran 1.8b is what the IEEE site distributes; I could not confirm a COMPSAC-specific class).
- [ ] Run IEEE PDF eXpress (required for camera-ready) - not done.

## 3. Anonymity (review PDF) - checked
- [x] Author block replaced by "Anonymous submission"; no affiliations/emails.
- [x] PDF metadata: `/Author` empty, `/Title` "Anonymous submission", `/Subject`, `/Keywords` empty; Creator "TeX", Producer "pdfTeX-1.40.25" (no personal names, no file paths).
- [x] Text extraction searched for names, employer, e-mail, "github", home-directory paths: none found.
- [x] Repository paragraph rewritten: code will be released after review (no URL, no repo name).
- [x] The one reference to the authors' earlier work ("our earlier 1,000-record sample") was neutralised to "a preliminary 1,000-record experiment that is not reported here".
- [x] No self-citations in the bibliography.
- [x] Acknowledgments contain only the AI disclosure (no funding/people/institutions). **If you add funding/grant acknowledgments, add them only in the camera-ready.**
- [ ] When uploading, do not use a file name that contains your name; check the submission system's metadata fields.

## 4. AI disclosure (in "Acknowledgments", both versions)
States: AI system = Claude (Anthropic; Claude Code, Claude Sonnet 5.5, plus subagents for citation checking); used for pipeline code, drafting/editing text of all sections, generating figures/tables from result files, and bibliographic cross-checking; numbers produced by code and re-checked by script; authors responsible. **Authors must confirm this statement is accurate and complete for their actual use** (e.g., any other AI tool, or changes made by hand).

## 5. Content constraints (all kept)
- [x] Nested CV, hyper-parameter tuning, computational-cost analysis and the limitations section retained; qualified/negative finding retained (original features >= PCA/KPCA for DT/RF; RBF-SVM exception shrinking under tuning).
- [x] "Row-order robustness checks / proxy chronology" - no claim of true temporal validation anywhere (grep of "chronolog", "time-aware", "temporal" in the review text: only the label "proxy chronology" and "true temporal drift is not tested").
- [x] Sample stated as class-stratified (floor of 100/class), not prevalence-preserving - abstract, Sample paragraph, limitation 1.
- [x] No experimental number changed in this pass.

## 6. Audits run for this version
- Claim audit: `ACN_RUN=v2 python -m src.acn.check_claims` -> 232 checks, 0 failing; all 116 decimals in the prose matched to result CSVs (4 external/unrecomputed: 0.2% NaN share, 2.5 M pool, Python 3.13, cited 99.6%).
- Reference audit: 17/17 entries re-verified against Crossref/publisher/arXiv (previous pass); `\cite` keys = bib keys = bibitems (17/17, no orphans). Still unverifiable: Kuang et al. abstract (paywalled), per-classifier results of Abdulhammed et al., Nadeau & Bengio full text.
- Figures: images; the data behind them is covered by the checker, the pixels were inspected visually only.

## 7. Authors must still do
1. Fill author names, affiliations, emails and repository URL in the camera-ready `.tex` (placeholders marked `TO BE FILLED`); add funding/real acknowledgments there.
2. Confirm the SEPT 2027 track and submission portal; select SEPT at submission.
3. Decide on the 9-page vs 10-page budget (1 page spare, e.g. for the camera-ready author block).
4. Re-read the three unverified references (above) if you want to keep the sentences that cite them.
5. Confirm originality (no concurrent submission) and IEEE Cross Check readiness.
