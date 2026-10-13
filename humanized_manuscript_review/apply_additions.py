"""Second step (run after apply_revision.py): adds (a) ten per-paper related-work entries, (b) per-algorithm accuracy figure (fig12)."""
t = open("main.tex").read()
def seg(a, b):
    i = t.index(a); j = t.index(b, i) + len(b); return t[i:j]
R = []
R.append((seg("\\textit{Dataset and its problems.}", "publisher or preprint pages."),
r"""\textit{Dataset and its quality.} \textbf{Ring et al.}~\cite{ring2019} survey public network-intrusion datasets and define 15 properties for judging which evaluation settings each dataset suits; we use this to place CIC-IDS2017 among available flow datasets. \textbf{Sharafaldin et al.}~\cite{sharafaldin2018} introduced CIC-IDS2017 and describe its traffic and attack scenarios; we use the original flow files they distribute. \textbf{Engelen et al.}~\cite{engelen2021} report ``TCP appendix'' artefact flows (about a quarter of all flows), attack attempts labelled as attacks although they contain no malicious payload, and feature-extraction flaws that enable shortcut learning, and they released a corrected version; this limits how far our absolute scores can be trusted. \textbf{Panigrahi and Borah}~\cite{panigrahi2018} likewise describe shortcomings of the dataset and propose a combined dataset, which we did not use. These four papers concern how far scores can be trusted, not dimensionality reduction.

\textit{Dimensionality reduction.} \textbf{Abdulhammed et al.}~\cite{abdulhammed2019} apply an auto-encoder and PCA to CIC-IDS2017, reducing 81 features to 10 and reporting about 99.6\,\% accuracy in multi-class and binary classification; they are our nearest CIC-IDS2017 reference for PCA. \textbf{Kuang et al.}~\cite{kuang2014} combine KPCA, an SVM and a genetic algorithm for intrusion detection; this is the closest earlier KPCA-plus-SVM design to ours, but it predates CIC-IDS2017 and so cannot have used it. \textbf{Abdel-Rahman et al.}~\cite{abdelrahman2026} propose a feature-importance-guided autoencoder and state that, with a random forest, it outperformed earlier reduction techniques on NSL-KDD, UNSW-NB15 and CIC-IDS2017; we did not extract their numbers, and we study classical reducers rather than a learned one. \textbf{Chavan and Alone}~\cite{chavan2025} report ``high accuracy'' for a random forest on CIC-IDS 2017, with no figure or split in the abstract, so there is nothing to compare numerically with our random-forest result.

\textit{Evaluation methodology.} \textbf{Arp et al.}~\cite{arp2022} describe pitfalls in machine learning for security that can produce unrealistic performance; in response we fit every data-dependent step on training folds only and report class-aware metrics beside accuracy. \textbf{Apruzzese et al.}~\cite{apruzzese2022} propose cross-evaluating ML-based network intrusion detection across datasets; we do not, so our conclusions stay within one dataset. Among the studies we read, none pairs a no-reduction baseline, per-class analysis and fold-wise fitting across PCA and several KPCA kernels. Our reading was not exhaustive, so this is not a claim about a gap in the literature. IEEE Xplore was unreachable, so all studies come from open publisher or preprint pages."""))
R.append(("\\subsection{Selection optimism: nested cross-validation}",
r"""\subsection{Accuracy of each algorithm across feature spaces}
Fig.~\ref{fig:peralgo} shows one panel per classifier: bars give mean accuracy for PCA and the three KPCA kernels at 5 to 30 components, and the dashed line is the accuracy on the original 78 features. For logistic regression, $k$-NN, decision tree and random forest, none of the 20 reduced configurations exceeds the original accuracy (the closest is $k$-NN with cosine KPCA at 30 components: 0.9339 against 0.9341). Only the SVM has reduced configurations above its original 0.906, and only cosine KPCA at 15, 20 and 30 components (best 0.924). Accuracy differences are small next to class-level differences, which is why macro-F1 is the primary metric.
\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth]{figures/fig12_per_algorithm_accuracy.pdf}
\caption{Accuracy (mean $\pm$ std over 15 folds, standard class weights) of each classifier for PCA and KPCA at 5--30 components. Dashed line: original 78 features. The vertical axis starts at 0.5.}\label{fig:peralgo}
\end{figure}

\subsection{Selection optimism: nested cross-validation}"""))
for a, b in R:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
open("main.tex", "w").write(t); print("additions applied")
