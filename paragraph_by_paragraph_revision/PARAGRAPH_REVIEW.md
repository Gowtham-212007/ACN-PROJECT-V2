# PARAGRAPH_REVIEW

Reviewed by reading each block of `humanized_manuscript_review/main.tex` against `results/v2` outputs and earlier claim checks. IDs P00-P58 follow source order (P00 = title/abstract block). Blocks that are only figures, tables, algorithm or bibliography commands are listed with their caption/note decision. 'No change' means the text was read and judged accurate and clear; it is not a claim of perfect prose.

| ID | Opening | Role | Decision | Note | Verification |
|---|---|---|---|---|---|
| P00 | `\title{Does Dimensionality Reduction Help Classica` | Caption/table/code/structure | small edit | abstract: memory ratio labelled 'whole-pipeline traced memory'; earlier prior-studies claim softened | numbers/citations checked in CLAIM_VERIFICATION.md |
| P01 | `\keywords{Network intrusion detection \and CIC-IDS` | Caption/table/code/structure | no change |  | structural |
| P02 | `\section{Introduction} Researchers often develop a` | Motivation | small edit | 'one of the most used' -> 'widely used' (no supporting count) | numbers/citations checked in CLAIM_VERIFICATION.md |
| P03 | `Three problems make these comparisons hard to read` | Problem statement | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P04 | `\textbf{Research questions.} \textbf{RQ1:} how doe` | RQs | small edit | RQ5 no longer lists 'smaller training sets': no such experiment exists in results/v2 (n_train is 4,800 in every row of cv_results) | numbers/citations checked in CLAIM_VERIFICATION.md |
| P05 | `\textbf{Contributions.} (i) A reproducible compari` | Contributions | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P06 | `\section{Related Work} We surveyed fifteen studies` | Related-work overview | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P07 | `\textit{Dataset and its quality.} \textbf{Ring et ` | Related work: dataset | small edit | Ring: removed an unsupported claim that we use the survey to place CIC-IDS2017; closing sentence no longer groups Ring/Sharafaldin as flaw studies | numbers/citations checked in CLAIM_VERIFICATION.md |
| P08 | `\textit{Dimensionality reduction.} \textbf{Abdulha` | Related work: reduction | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P09 | `\textit{Evaluation methodology.} \textbf{Arp et al` | Related work: evaluation | small edit | removed duplicated 'not exhaustive' sentence; access statement shortened | numbers/citations checked in CLAIM_VERIFICATION.md |
| P10 | `\begin{table}[htbp] \caption{Recent studies (2025)` | Caption/table/code/structure | table edit | Patil PCA entries renamed PCA-based feature selection | numbers/citations checked in CLAIM_VERIFICATION.md |
| P11 | `\section{Dataset and Preprocessing}\label{sec:data` | Data | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P12 | `\textbf{Duplicates.} 308{,}381 flows (10.9\,\%) ar` | Duplicates | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P13 | `\textbf{Sample.} Exact KPCA needs an $n\times n$ k` | Sample | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P14 | `\section{Methodology}\label{sec:method} \textbf{Pi` | Pipeline | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P15 | `\begin{figure}[htbp]\centering \includegraphics[wi` | Caption/table/code/structure | no change |  | structural |
| P16 | `\textbf{Algorithm and formulas.} Algorithm~\ref{al` | Formulas | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P17 | `\begin{algorithm}[t] \caption{Fold-wise evaluation` | Caption/table/code/structure | no change |  | structural |
| P18 | `\textbf{Classifiers.} Logistic regression (L2, lbf` | Classifiers | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P19 | `\textbf{Validation.} Repeated stratified 5-fold cr` | Validation | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P20 | `\textbf{Nested cross-validation for selection.} Pi` | Nested CV | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P21 | `\textbf{Nested hyper-parameter search.} For $k$-NN` | Tuning | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P22 | `\textbf{Row-order robustness checks (proxy chronol` | Row-order checks | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P23 | `\textbf{Metrics.} Accuracy; macro-precision, macro` | Metrics | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P24 | `\textbf{Statistics.} Per classifier we compare fea` | Statistics | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P25 | `\textbf{Cost.} A serial benchmark (no parallel wor` | Cost method | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P26 | `\textbf{Setup.} A 2-vCPU, 7\,GB VM (Python 3.13, s` | Setup | small edit | 2,850 fits explained as 190 configurations x 15 folds incl. majority-class baseline | numbers/citations checked in CLAIM_VERIFICATION.md |
| P27 | `\section{Results} \subsection{Original-feature bas` | Baseline result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P28 | `\begin{table}[htbp] \caption{Per-class results of ` | Caption/table/code/structure | no change |  | structural |
| P29 | `\subsection{Original space versus PCA versus Kerne` | Main result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P30 | `A stricter question is whether each classifier's \` | Best-reduced result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P31 | `\begin{table}[htbp] \caption{Accuracy / macro-F1 (` | Caption/table/code/structure | no change |  | structural |
| P32 | `Fig.~\ref{fig:all} shows all 25 classifier-by-spac` | Caption/table/code/structure | no change |  | structural |
| P33 | `\begin{figure}[htbp]\centering \includegraphics[wi` | Caption/table/code/structure | no change |  | structural |
| P34 | `\subsection{Accuracy of each algorithm across feat` | Per-algorithm accuracy | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P35 | `\subsection{Selection optimism: nested cross-valid` | Nested result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P36 | `\subsection{Effect of hyper-parameter tuning} Tabl` | Tuning result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P37 | `\begin{table}[htbp] \caption{Nested hyper-paramete` | Caption/table/code/structure | no change |  | structural |
| P38 | `\subsection{Row-order robustness (proxy chronology` | Row-order result | small edit | 'They assume' -> 'Both checks assume' (unclear referent) | numbers/citations checked in CLAIM_VERIFICATION.md |
| P39 | `\subsection{Kernel, component count and class weig` | Kernel/components | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P40 | `\subsection{Computational cost} The serial benchma` | Cost result | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P41 | `\subsection{Accuracy comparison with recent studie` | Cross-study context | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P42 | `\begin{figure}[htbp]\centering \includegraphics[wi` | Caption/table/code/structure | caption edit | states bars are not a like-for-like ranking; figure retained per faculty checklist | numbers/citations checked in CLAIM_VERIFICATION.md |
| P43 | `\section{Discussion} \textbf{Answers to the resear` | RQ answers | small edit | RQ5 no longer cites training sizes (unsupported) | numbers/citations checked in CLAIM_VERIFICATION.md |
| P44 | `\textbf{Why accuracy misleads.} Benign flows are 6` | Accuracy caveat | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P45 | `\textbf{Possible explanations (untested).} We ran ` | Hypotheses | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P46 | `\section{Threats to Validity and Limitations} The ` | Caption/table/code/structure | no change |  | structural |
| P47 | `\textbf{1. Sample, not full data.} All results com` | Limitation 1 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P48 | `\textbf{2. Leakage status.} Sampling was performed` | Limitation 2 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P49 | `\textbf{3. Limited external validity.} All data co` | Limitation 3 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P50 | `\textbf{4. Selection and inference.} The headline ` | Limitation 4 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P51 | `\textbf{5. Limited tuning.} Hyper-parameter search` | Limitation 5 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P52 | `\textbf{6. Dataset quality and cost.} The original` | Limitation 6 | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P53 | `We propose no new algorithm. We claim no state-of-` | Scope statement | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P54 | `\section{Conclusion} We asked whether PCA or KPCA ` | Conclusion | small edit | conclusion no longer cites smaller training sets (unsupported) | numbers/citations checked in CLAIM_VERIFICATION.md |
| P55 | `\textbf{Future work.} Repeat the pipeline over sev` | Future work | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P56 | `\section*{Data and Code Availability} The raw CIC-` | Data availability | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P57 | `\section*{Acknowledgments and AI-assistance disclo` | Disclosure | no change |  | numbers/citations checked in CLAIM_VERIFICATION.md |
| P58 | `\bibliographystyle{splncs04} \bibliography{referen` | Caption/table/code/structure | no change |  | structural |
