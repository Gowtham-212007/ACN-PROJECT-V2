# AI Disclosure and Writing Audit
## Policy (IEEE Access "Preparing Your Article", fetched 2026-10-09)
AI-generated content (text, figures, images, code) must be disclosed in the **Acknowledgments**, identifying the AI system, the sections where it was used and a brief explanation of the level of use. AI used only for editing/grammar is generally outside the rule but disclosure is recommended. Fabricated content or nonexistent references lead to rejection.
## What the project history verifies (Claude Code session, Claude Sonnet 5.5, plus subagents)
Pipeline code (prepare_raw, run_cv, nested, tuning, temporal/blocked, stats, runtime, tables/figures, claim checker); drafting and editing of all manuscript sections, abstract, captions, limitations and the audit documents; bibliographic cross-checking via subagents. The experiments were executed by code; no result was typed by the AI. The disclosure paragraph in the Acknowledgment states exactly this (see IEEE_ACCESS_FINAL.tex).
## Authors must confirm
(a) that this is accurate and complete (any other AI tool, e.g. translation/grammar tools, must be added); (b) the bracketed sentence "[THE AUTHORS MUST CONFIRM ...]" must be deleted after confirmation; (c) that they have reviewed and take responsibility for all content. I cannot verify the authors' own contributions outside the session.
## Writing review (what was changed)
- Removed internal-history phrases that a journal reader cannot follow ("the original project ...", "our earlier sample") or that point to unpublished work.
- Softened statements that exceeded the sources (Abdulhammed, Nadeau & Bengio) and added "proposes no new algorithm / no production-ready claim".
- Abstract rewritten to 242 words (limit 150-250), no abbreviations other than names (CIC-IDS2017), one paragraph.
Not changed (candid): the paper is long and carries repeated caveats (limitations are stated in Methods, Results and the Limitations section); some sentences are dense. A native-English proofreading pass is recommended (IEEE Access rejects poor grammar). No AI-text detector was run; none would prove authorship, and none is claimed.
