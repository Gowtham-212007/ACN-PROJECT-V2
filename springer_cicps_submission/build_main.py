"""Generate main.tex (Springer LNCS) from the verified IEEE Access body + new sections. Run: python3 build_main.py"""
import re
src = open("../papers/ieee/IEEE_ACCESS_FINAL.tex").read()
abstract = re.search(r"\\begin\{abstract\}\n(.*?)\n\\end\{abstract\}", src, re.S).group(1).strip()
body = src[src.index("\\section{Introduction}"):src.index("\\section*{Acknowledgment}")]
# --- environment conversion (single-column LNCS)
body = body.replace("\\begin{figure*}[t]", "\\begin{figure}[t]").replace("\\end{figure*}", "\\end{figure}")
body = body.replace("\\begin{table*}[t]", "\\begin{table}[t]").replace("\\end{table*}", "\\end{table}")
body = body.replace("\\resizebox{\\columnwidth}", "\\resizebox{\\textwidth}").replace("width=0.85\\columnwidth", "width=0.5\\textwidth")
body = body.replace("\\input{tables_v2/", "\\input{tables/").replace("\\tabsize", "\\scriptsize")
# --- remove references to unpublished earlier work
body = re.sub(r" Earlier configurations in this line of work tied kernel and component count \(RBF--5, linear--10, cosine--15\); here they are crossed so the two effects can be separated\.", "", body)
body = re.sub(r"The gap is smaller than in a preliminary 1,000-record experiment that is not reported here, but still conceals", "The gap still conceals", body)
body = body.replace("The gap is smaller than in a preliminary 1{,}000-record experiment that is not reported here, but still conceals", "The gap still conceals")
assert "preliminary 1" not in body and "Earlier configurations" not in body, "unpublished-work mention left"

# --- fit the 15-page limit: drop figure/table environments whose numbers are already in the text (kept in the repository)
def drop_env(b, label, env):
    j = b.index("\\label{%s}" % label); i = b.rfind("\\begin{%s}" % env, 0, j); k = b.index("\\end{%s}" % env, j) + len("\\end{%s}" % env)
    return b[:i] + b[k:]
for lab, env in [("fig:acc", "figure"), ("tab:temporal", "table"), ("tab:blocked", "table"), ("fig:comp", "figure"), ("fig:size", "figure")]:
    body = drop_env(body, lab, env)
for ref, rep in [("Table~\\ref{tab:temporal} shows macro-F1", "Macro-F1 (full tables in the repository)"), ("(Table~\\ref{tab:blocked}; ", "("),
                 ("Table~\\ref{tab:n10} and Fig.~\\ref{fig:f1}", "Table~\\ref{tab:n10} and Fig.~\\ref{fig:all}"), ("Fig.~\\ref{fig:size} shows", "Training-size curves (repository) show"), ("(Fig.~\\ref{fig:acc})", "(Table~\\ref{tab:perclass})"), ("Fig.~\\ref{fig:comp} shows", "Component-count curves (repository) show")]:
    body = body.replace(ref, rep)


# --- compress kernel/component/class-weight subsections into one paragraph
a=body.index("\\subsection{Kernel and component count}"); b=body.index("\\subsection{Computational cost}")
body = body[:a] + r"""\subsection{Kernel, component count and class weighting}
Linear KPCA equals PCA on centred data: results were identical for $k$-NN and SVM and within 0.001 (LR) or 0.007 (trees, tiny eigen-solver differences, not tested), so a ``linear KPCA'' result is a PCA result. Component count mattered more than kernel for LR (macro-F1 0.37 at 5 PCA components to 0.73 at 30, versus 0.736 on original features) and SVM; for $k$-NN, DT and RF the kernel mattered slightly more, with small effects. RBF-KPCA with the default $\gamma$ was weakest for LR, $k$-NN, DT and RF; for the SVM cosine KPCA was best (mean macro-F1 0.657 versus 0.536 linear, 0.515 RBF; $\gamma$ untuned). Balanced class weights raised balanced accuracy for LR and SVM but macro-F1 only for SVM and DT, and \emph{lowered} it for LR (0.736 $\to$ 0.710) and RF (0.901 $\to$ 0.885); the best model stayed the unweighted RF.

""" + body[b:]
body = drop_env(body, "tab:nested", "table")
body = body.replace("Table~\\ref{tab:nested} compares, per classifier,", "The repository table compares, per classifier,")
pass


# --- condensed paragraphs (numbers unchanged from the verified sources) to meet the 15-page limit
def repl_par(b, prefix, new):
    ps = re.split(r"(\n\s*\n)", b)
    for i in range(0, len(ps), 2):
        if ps[i].lstrip().startswith(prefix):
            ps[i] = new; return "".join(ps)
    raise KeyError(prefix)
body = repl_par(body, "\\subsection{Row-order robustness", r"""\subsection{Row-order robustness (proxy chronology)}
In the head/tail split 4{,}199 records train and 1{,}769 test (32 test records of unseen classes were dropped); only seven of the 15 classes occur in both parts, and infiltration has four test records. The random forest on original features scored 0.838 versus 0.948 for a random split of the same rows and classes (decision tree 0.846 versus 0.959), a penalty of about 0.11. Reduced spaces suffered at least as much (RF: PCA-10 0.759, cosine KPCA-30 0.704), so the order original $>$ reduced for DT, RF and LR was preserved; $k$-NN stayed a near tie (0.790 versus 0.806) and the SVM again favoured cosine KPCA-30 (0.616 versus 0.479). In the blocked cross-validation (6--10 classes scored per fold) the random forest scored 0.851 versus 0.932 for random folds on the same classes, with the original space again ahead for DT, RF and LR. These checks assume that row order follows capture time, score only a subset of classes and use single splits or five folds, so they support the ranking but give no precise penalty. Full tables are in the repository.""")
body = repl_par(body, "\\subsection{Sensitivity to training-set size}", "")
body = body.replace("the best model stayed the unweighted random forest.", "the best model stayed the unweighted random forest. At 2{,}400, 3{,}600 and 4{,}800 training records (10 splits) the original space had the highest mean macro-F1 for LR, DT and RF at every size (SVM: at 3{,}600 and 4{,}800); this is a within-sample stability check only.")
body = repl_par(body, "\\textbf{Row-order robustness checks", r"""\textbf{Row-order robustness checks (proxy chronology).} The raw files have no timestamps; attack flows occur in contiguous row blocks, so we \emph{assume}, without proof, that row order follows capture time. (i) \emph{Head/tail}: the first 70\,\% of each file's rows train, the last 30\,\% test. (ii) \emph{Blocked CV}: each file is cut into five contiguous blocks, each held out in turn. Only classes present in both training and test are scored, and a random split of the same rows on the same classes is the comparator.""")
body = repl_par(body, "\\section{Experimental Setup}", r"""\section{Experimental Setup}
A 2-vCPU Intel Xeon @ 2.10\,GHz VM with 7\,GB RAM (Linux, Python 3.13, scikit-learn 1.9, NumPy 2.5, SciPy 1.18) ran the main grid (21 spaces $\times$ 9 classifier/weighting variants $\times$ 15 folds plus baseline, 2{,}850 fits, about 28 min), the nested cross-validation (about 64 min) and the tuning search (about 16 min). Table~\ref{tab:rt} timings come from a separate serial benchmark (4{,}800 training, 1{,}200 test records).""")
body = repl_par(body, "\\section{Conclusion}", r"""\section{Conclusion}
On a 6{,}000-record sample drawn after exact same-label duplicate removal from all eight CIC-IDS2017 files, with fold-wise fitting of imputation, scaling and reduction, a random forest on the original 78 features had the highest observed macro-F1 (0.901 $\pm$ 0.020; accuracy 0.972 $\pm$ 0.004; 0.900 $\pm$ 0.022 with nested selection). PCA and KPCA with 5--30 components generally did not improve on the original features: they were clearly worse for decision tree and random forest, practically equal for logistic regression (30 components) and $k$-NN, and helped mainly the RBF-SVM (cosine KPCA), an advantage that shrank from 0.076 to 0.021 after tuning. The ranking survived row-order checks that rest on an assumed row order. Linear KPCA coincided with PCA. KPCA cost more than 200 times more fit time and 37 times more traced memory at 4{,}800 records. Accuracy (0.972) concealed weak detection of web brute force and XSS (F1 0.53, 0.59). The results are limited to this sample and to CIC-IDS2017.""")
body = drop_env(body, "tab:classes", "table")
body = drop_env(body, "fig:cm", "figure")
body = body.replace("; Fig.~\\ref{fig:cm})", ")").replace("Table~\\ref{tab:classes}", "the class counts in the repository")


body = repl_par(body, "\\subsection{Selection optimism", r"""\subsection{Selection optimism: nested cross-validation}\label{sec:results-nested}
Selecting the best of 189 configurations on the scoring folds is optimistic, so selection was repeated inside a nested cross-validation (Section~\ref{sec:method}). The configuration chosen on inner folds reached macro-F1 $0.900\pm0.022$ (accuracy 0.972, MCC 0.947) on the outer folds against 0.901 for the same-CV maximum: an optimism of about 0.001. The inner folds chose an original-feature configuration in all 15 outer folds (RF 11 times, DT 4). Original features were clearly better than the inner-selected best reduced space for DT ($+0.093$) and RF ($+0.062$), practically equal for logistic regression ($+0.004$, unadjusted $p=0.010$, far below the fold standard deviation of 0.022) and $k$-NN ($+0.002$), and worse for the SVM ($-0.060$; cosine KPCA-30 chosen in all 15 folds). The $p$-values are unadjusted Wilcoxon tests over 15 outer folds that share training data.""")
body = repl_par(body, "\\subsection{Effect of hyper", r"""\subsection{Effect of hyper-parameter tuning}
Table~\ref{tab:tuning} reports the nested search (five outer folds). Tuning left the random forest unchanged (original 0.901 default, 0.899 tuned; best reduced 0.842 versus 0.839). For $k$-NN, tuning gave $+0.007$ on original features; the best reduced space was cosine KPCA-30 under defaults (gap 0.000) and PCA-30 after tuning (0.810 versus 0.808, gap $-0.002$; default gap in PCA-30: $+0.003$), always far below fold variation. The SVM changed most: tuned macro-F1 rose from 0.668 to 0.791 on original features and from 0.745 to 0.812 with cosine KPCA-30, so the reduced-space advantage shrank from 0.076 to 0.021. Five folds cannot establish a 0.021 difference, and the selected values sit on grid edges (SVM $C=10$ and $k$-NN $k=3$ in all 20 selections), so we treat the SVM advantage of KPCA as a property of the default RBF-SVM that largely disappears with tuning, not as a robust benefit of KPCA.""")
body = repl_par(body, "\\subsection{Computational cost}", r"""\subsection{Computational cost}
Table~\ref{tab:rt} summarises the serial benchmark at 4{,}800 training / 1{,}200 test records. KPCA fitting took 5.5--5.6\,s against 0.02\,s for PCA, increased decision-tree training from 0.07\,s (PCA) to 5.3--5.6\,s and random-forest training from 0.84--0.90\,s to 6.3--6.6\,s, and raised random-forest inference about fivefold (0.020--0.021\,s to 0.092--0.123\,s per 1{,}200 records). Peak traced memory was 363\,MB for KPCA against 9.8\,MB for PCA or no reduction, and grew roughly quadratically with $n$ (3.1, 11.0, 41.6, 161.3, 359.1\,MB for $n=400$ to $4800$; log--log slope 1.9), consistent with $n\times n$ float64 kernel matrices (184\,MB at $n=4800$). As a purely theoretical estimate (not a measurement), one dense float64 kernel matrix for all 2{,}830{,}743 source flows would occupy about 64\,TB, so exact KPCA on the full dataset would need approximation or sub-sampling (not tested). Timings come from a shared 2-vCPU machine; differences below roughly a factor of two should not be over-interpreted, and no real-time claim is made.""")
body = repl_par(body, "\\textbf{Plausible but untested", r"""\textbf{Untested explanations.} Tree ensembles are insensitive to monotone feature scaling, and projection onto a few leading components may discard low-variance but discriminative directions; heavy-tailed flow features also fit variance-based reduction and the default RBF width poorly. We did not test these hypotheses.""")
body = repl_par(body, "\\textbf{6. Dataset quality", r"""\textbf{6. Dataset quality and cost.} The original CIC-IDS2017 flows contain known labelling and feature-construction artefacts \cite{engelen2021}, which may distort scores (and may explain the web brute-force/XSS confusion); we did not use the corrected release. Timings and memory come from one 2-vCPU virtual machine, memory is a traced lower bound, and the 64\,TB figure is arithmetic, not a measurement.""")
body = repl_par(body, "\\textbf{7. Cost measurements", "")
body = repl_par(body, "\\textbf{Contributions.}", r"""\textbf{Contributions.} (i) A reproducible comparison of original features, PCA and three KPCA kernels over five classical classifiers on a raw-data-derived sample drawn after exact same-label duplicate removal, with fold-wise fitting, a majority-class baseline, a nested-CV check of selection optimism and a small nested hyper-parameter search. (ii) A class-aware analysis showing how much accuracy overstates detection quality. (iii) Paired statistical tests with an explicit independence caveat, and two row-order robustness checks (proxy chronology). (iv) A runtime and memory measurement of KPCA against PCA. We do not propose a new algorithm; code and results are described in the Data and Code Availability section.""")


# --- new related work
i0, i1 = body.index("\\section{Related Work}"), body.index("\\section{Dataset and Preprocessing}")
related = r"""\section{Related Work}
We surveyed fifteen studies. Table~\ref{tab:lit} lists five recent (2025) intrusion-detection studies with the algorithm, dataset and result \emph{as stated by their authors}; the remaining ten, covering the dataset, its known problems, dimensionality reduction and evaluation practice, are discussed below. The reported numbers use different datasets, splits and metrics and must not be read as a ranking.


\textit{Dataset and its problems.} Ring et al.\ review public network-intrusion datasets and define 15 properties for judging which evaluation settings each dataset fits \cite{ring2019}. CIC-IDS2017 was introduced by Sharafaldin et al.\ \cite{sharafaldin2018}. Engelen et al.\ report problems in it: ``TCP appendix'' artefact flows (about a quarter of all flows), attack attempts labelled as attacks although they contain no malicious payload, and feature-extraction flaws that enable shortcut learning; they released a corrected version \cite{engelen2021}. Panigrahi and Borah likewise describe shortcomings and propose a combined dataset \cite{panigrahi2018}. We use the \emph{original} labelled flows, so absolute scores may partly reflect such artefacts.

\textit{Dimensionality reduction and feature selection.} Abdulhammed et al.\ apply an auto-encoder and PCA to CIC-IDS2017, reducing the dimension from 81 to 10 and reporting about 99.6\,\% accuracy with several classifiers \cite{abdulhammed2019}. Kuang et al.\ propose a hybrid of KPCA, an SVM and a genetic algorithm \cite{kuang2014}. Abdel-Rahman et al.\ propose a feature-importance-guided autoencoder and state that it outperforms earlier dimensionality-reduction techniques on three datasets including CIC-IDS2017 \cite{abdelrahman2026}; we did not extract their numerical results. Chavan and Alone apply a random forest to CIC-IDS 2017 and report ``high accuracy'' without a figure or split in the abstract \cite{chavan2025}. Patil et al.\ include PCA among their reduction methods with a stratified 70/30 split \cite{patil2025}. These studies mostly report accuracy on one split; none that we read pairs a no-reduction baseline, per-class analysis and fold-wise fitting across PCA and several KPCA kernels.

\textit{Evaluation practice.} Arp et al.\ describe pitfalls in machine learning for security that can lead to unrealistic performance \cite{arp2022}, and Apruzzese et al.\ propose cross-evaluating ML-based NIDS across datasets \cite{apruzzese2022}. Motivated by these works we (a) fit every data-dependent step on training folds only, (b) report class-aware metrics beside accuracy, (c) include trivial and no-reduction baselines, and (d) state what our sample cannot show. This section is not a systematic survey. IEEE Xplore pages could not be retrieved from our environment, so the studies above come from open publisher and preprint pages.

\begin{table}[t]
\caption{Recent studies (2025) and this work. Results are quoted from each source and are not directly comparable (different datasets, sampling, splits and metrics).}\label{tab:lit}
\centering\scriptsize
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.3cm}>{\raggedright\arraybackslash}p{3.3cm}>{\raggedright\arraybackslash}p{2.4cm}>{\raggedright\arraybackslash}p{1.7cm}>{\raggedright\arraybackslash}p{1.7cm}@{}}
\toprule
Author (year) & Title & Algorithm & Dataset & Reported result \\
\midrule
Waghmode et al.\ \cite{waghmode2025} (2025) & Intrusion detection system based on machine learning using least square support vector machine & Quantum-inspired LS-SVM with exhaustive feature selection & NSL-KDD, CIC-IDS-2017, UNSW-NB15 & Accuracy 99.5\,\% on CIC-IDS-2017 \\
Patil et al.\ \cite{patil2025} (2025) & Optimizing network intrusion detection systems through ensemble learning and feature selection using the CIC-IDS2017 dataset & Bagging and boosting ensembles; information gain, chi-square, PCA (20 features) & CIC-IDS2017, stratified 70/30 split & Accuracy 99.98\,\% (Extra Trees, 24 features); 99.58--99.96\,\% with PCA \\
Abdelaziz et al.\ \cite{abdelaziz2025} (2025) & Enhancing network threat detection with random forest-based NIDS and permutation feature importance & Random forest, permutation importance, undersampling; repeated stratified 5-fold CV & CIC-IDS2017 & Weighted-F1 99.8\,\%, macro-F1 93.31\,\% (26 features) \\
Xu and Liu \cite{xu2025} (2025) & Robust anomaly detection in network traffic: evaluating machine learning models on CICIDS2017 & MLP, 1D-CNN, one-class SVM, LOF & CICIDS2017 & Accuracy 97.75\,\% (MLP, overall test set) \\
Emirmahmuto\u{g}lu and Atay \cite{emirmahmutoglu2025} (2025) & A feature selection-driven machine learning framework for anomaly-based intrusion detection systems & PSO/FPA/DE feature selection; LR, DT, RF, k-NN and others & KDD CUP 99, NSL-KDD, UNSW-NB15, CSE-CIC-IDS2018 & Accuracy 99.9965\,\% on CSE-CIC-IDS2018 (FPA, RF) \\
\midrule
\textbf{This work} (2026) & (this paper) & Original features vs PCA vs linear/RBF/cosine KPCA; LR, k-NN, SVM, DT, RF & CIC-IDS2017, 6,000-record class-stratified sample & RF (original): accuracy 97.2\,\%, macro-F1 90.1\,\% \\
\bottomrule
\end{tabular}
\end{table}

"""
body = body[:i0] + related + body[i1:]
# --- algorithm + formulas in methodology
algo = r"""\textbf{Algorithm and formulas.} Algorithm~\ref{alg:cv} summarises one evaluation of a feature space and classifier. Features are standardised as $z_j=(x_j-\mu_j)/\sigma_j$ with $\mu_j,\sigma_j$ from the training fold. PCA projects onto the leading eigenvectors $\mathbf{v}_k$ of the training covariance matrix $\mathbf{C}=\frac{1}{n}\mathbf{Z}^{\top}\mathbf{Z}$. KPCA uses the kernel matrix $K_{ij}=k(\mathbf{z}_i,\mathbf{z}_j)$ with
\begin{equation}
k_{\mathrm{lin}}=\mathbf{z}^{\top}\mathbf{z}',\qquad k_{\mathrm{rbf}}=\exp(-\gamma\lVert\mathbf{z}-\mathbf{z}'\rVert^{2}),\ \gamma=\tfrac{1}{78},\qquad k_{\cos}=\frac{\mathbf{z}^{\top}\mathbf{z}'}{\lVert\mathbf{z}\rVert\,\lVert\mathbf{z}'\rVert},
\end{equation}
centred as $\tilde{K}=K-\mathbf{1}_nK-K\mathbf{1}_n+\mathbf{1}_nK\mathbf{1}_n$; with $\mathbf{1}_n$ the $n\times n$ matrix whose entries are all $1/n$. For the leading eigenpairs $(\lambda_k,\boldsymbol{\alpha}_k)$ of $\tilde{K}$, with $\lVert\boldsymbol{\alpha}_k\rVert=1$, a sample is projected to $\tilde{K}_{\mathrm{new}}\boldsymbol{\alpha}_k/\sqrt{\lambda_k}$, with $\tilde{K}_{\mathrm{new}}$ the centred kernel against the training fold (matches \texttt{KernelPCA.transform}; dividing by $\lambda_k$ does not). With per-class precision $P_c$ and recall $R_c$, the primary metric is
\begin{equation}
F1_c=\frac{2P_cR_c}{P_c+R_c},\qquad \text{macro-F1}=\frac{1}{C}\sum_{c=1}^{C}F1_c,\ \ C=15,
\end{equation}
and balanced accuracy equals macro-recall. The multi-class MCC from the confusion matrix $\mathbf{M}$ with $s$ samples, $t_k$ true and $p_k$ predicted counts of class $k$, and $c=\sum_k M_{kk}$ correct predictions is
\begin{equation}
\mathrm{MCC}=\frac{c\,s-\sum_k p_kt_k}{\sqrt{s^{2}-\sum_k p_k^{2}}\,\sqrt{s^{2}-\sum_k t_k^{2}}}.
\end{equation}

\begin{algorithm}[t]
\caption{Fold-wise evaluation of one feature space $S$ and classifier $f$}\label{alg:cv}
\begin{algorithmic}[1]
\Require sample $(X,y)$ of 6,000 records; space $S\in\{$original, PCA, KPCA$(k,n)\}$; classifier $f$; 3 repeats of stratified 5-fold CV (seed 42)
\Ensure mean and standard deviation of accuracy, macro-F1, MCC and cost over 15 folds
\For{each repeat $r$ and fold $(\mathrm{tr},\mathrm{te})$}
  \State fit mean imputer and standard scaler on $X_{\mathrm{tr}}$; transform $X_{\mathrm{tr}}$ and $X_{\mathrm{te}}$
  \If{$S\neq$ original}
    \State fit reducer $T_S$ ($n$ components) on the scaled $X_{\mathrm{tr}}$ only
    \State $Z_{\mathrm{tr}}\gets T_S(X_{\mathrm{tr}})$;\ $Z_{\mathrm{te}}\gets T_S(X_{\mathrm{te}})$
  \Else
    \State $Z_{\mathrm{tr}}\gets X_{\mathrm{tr}}$;\ $Z_{\mathrm{te}}\gets X_{\mathrm{te}}$
  \EndIf
  \State fit $f$ on $(Z_{\mathrm{tr}},y_{\mathrm{tr}})$;\ predict $\hat{y}$ on $Z_{\mathrm{te}}$; record metrics and fit time
\EndFor
\State \Return mean $\pm$ std over the 15 folds (nested selection repeats this inside each outer training set with 3 inner folds)
\end{algorithmic}
\end{algorithm}

"""
body = body.replace("\\textbf{Classifiers.}", algo + "\\textbf{Classifiers.}", 1)
# --- combined chart and literature accuracy figure
allexec = r"""\subsection{All executions in one chart}
Fig.~\ref{fig:all} places every classifier and feature space at 10 components in a single chart (25 executions, macro-F1, mean $\pm$ std over 15 folds). Within each classifier group the black bar is the original space; only for the SVM does a reduced space (cosine KPCA) exceed it, and the tree-based classifiers lead overall.

\begin{figure}[t]\centering
\includegraphics[width=\textwidth]{figures/fig10_all_executions.pdf}
\caption{Macro-F1 of all classifier $\times$ feature-space executions at 10 components (mean $\pm$ std over 15 folds; standard class weights; axis starts at zero).}\label{fig:all}
\end{figure}

"""
body = body.replace("\\subsection{Selection optimism: nested cross-validation}", allexec + "\\subsection{Selection optimism: nested cross-validation}", 1)
cmp_ = r"""\subsection{Accuracy comparison with recent studies}
Fig.~\ref{fig:cmp} and Table~\ref{tab:lit} show reported accuracy next to ours. The recent studies quote 97.7--99.99\,\% accuracy on their own datasets and splits, whereas our random forest reaches 97.2\,\% accuracy but only 0.901 macro-F1 on a sample that over-represents attacks and is scored by cross-validation. These numbers measure different things and are shown only to make the reporting gap visible: accuracy near 100\,\% on imbalanced flow data can coexist with weak minority-class detection, as our per-class results show.

\begin{figure}[t]\centering
\includegraphics[width=\textwidth]{figures/fig11_accuracy_comparison.pdf}
\caption{Accuracy reported by recent studies versus this work. Datasets, sampling, splits and metrics differ; the figure is not a performance ranking.}\label{fig:cmp}
\end{figure}

"""
body = body.replace("\\section{Discussion}", cmp_ + "\\section{Discussion}", 1) if False else body.replace("\\section{Discussion}", "__CMP__\\section{Discussion}", 1).replace("__CMP__", cmp_)
body = body.replace("figures_dummy", "").replace("\\begin{table}[t]", "\\begin{table}[htbp]").replace("\\begin{figure}[t]", "\\begin{figure}[htbp]")
body = body.replace("\\includegraphics[width=\\textwidth]{fig", "\\includegraphics[width=\\textwidth]{figures/fig").replace("\\includegraphics[width=0.5\\textwidth]{fig", "\\includegraphics[width=0.5\\textwidth]{figures/fig")
body = body.replace("figures/figures/", "figures/")
body = body.replace("\\section*{Data and Code Availability}", "\\section*{Data and Code Availability}")
body = repl_par(body, "\\textit{Dimensionality reduction and feature", r"""\textit{Dimensionality reduction and feature selection.} Abdulhammed et al.\ apply an auto-encoder and PCA to CIC-IDS2017 (81 to 10 dimensions) and report about 99.6\,\% accuracy \cite{abdulhammed2019}; Kuang et al.\ combine KPCA, an SVM and a genetic algorithm \cite{kuang2014}. Abdel-Rahman et al.\ state that a feature-importance-guided autoencoder outperforms PCA on three datasets including CIC-IDS2017 \cite{abdelrahman2026} (we did not extract their numbers). Chavan and Alone report ``high accuracy'' for a random forest on CIC-IDS 2017 without a figure or split in the abstract \cite{chavan2025}, and Patil et al.\ include PCA among their reduction methods \cite{patil2025}. Most report accuracy on one split; none that we read pairs a no-reduction baseline, per-class analysis and fold-wise fitting across PCA and several KPCA kernels.""")
body = repl_par(body, "\\section{Dataset and Preprocessing}", r"""\section{Dataset and Preprocessing}\label{sec:data}
\textbf{Data.} We use the eight daily CIC-IDS2017 \texttt{MachineLearningCVE} files: 2{,}830{,}743 flows, 78 numeric features, 15 labels (counts computed from the files; no provider checksum was available). There is no timestamp column. Rows with missing or infinite values are 0.2\,\% or less of each file (inf $\to$ NaN) and were not imputed before sampling. Eight features are constant in every file and were kept to match the 78-feature definition of earlier work.""")
body = repl_par(body, "\\textbf{Nested cross-validation for selection.}", r"""\textbf{Nested cross-validation for selection.} Choosing the best of 189 configurations (21 feature spaces $\times$ 9 classifier/weighting variants) on the scoring folds is optimistic. On the \emph{same} 15 outer folds, a stratified 3-fold inner cross-validation inside each outer training set (4{,}800 records) scores every configuration by macro-F1, the best is selected, and only it is scored on the untouched outer test fold. We apply this to (A) the global selection and, per classifier, to (C) the best \emph{reduced} space and weighting versus (D) the original space with weighting chosen the same way; all steps are refitted on every inner split.""")
body = repl_par(body, "\\textbf{Statistics.}", r"""\textbf{Statistics.} Per classifier we compare feature spaces at matched $n=10$ with two-sided Wilcoxon signed-rank tests on the 15 paired macro-F1 values, Holm-corrected over 30 comparisons, with the rank-biserial correlation $r$ as effect size, and Friedman omnibus tests, following the non-parametric procedures of Dem\v{s}ar \cite{demsar2006} (written for several data sets; here the blocks are folds of one sample). Because folds share training data, the 15 differences are positively correlated and naive $p$-values are too liberal \cite{nadeau2003}; we do not apply the Nadeau--Bengio correction and use the tests for screening, not as proof. Comparisons against each classifier's \emph{best} reduced space are selected on the same folds, which favours the reduced space; the nested analysis removes that bias.""")
body = body.replace(" The SVM gain also depends on component count: at 10 components, cosine KPCA is still below the original space (0.605 vs 0.675), and the SVM benefits from more components (cosine KPCA: 0.520, 0.605, 0.690, 0.725, 0.746 for 5--30 components).", " The SVM gain needs many components: cosine KPCA reaches 0.605 at 10 components (below the original 0.675) and 0.746 at 30.")

body = drop_env(body, "tab:rt", "table")
body = body.replace("Table~\\ref{tab:rt} summarises the serial benchmark", "The serial benchmark (table in the repository)").replace("Table~\\ref{tab:rt} timings", "Cost timings")
body = repl_par(body, "\\section{Experimental Setup}", r"""\textbf{Setup.} A 2-vCPU Intel Xeon @ 2.10\,GHz VM with 7\,GB RAM (Linux, Python 3.13, scikit-learn 1.9, NumPy 2.5, SciPy 1.18) ran the main grid (21 spaces $\times$ 9 variants $\times$ 15 folds plus baseline, 2{,}850 fits, about 28 min), nested CV (about 64 min) and tuning (about 16 min).""")
body = repl_par(body, "\\textbf{Why accuracy misleads.}", r"""\textbf{Why accuracy misleads.} The benign class is 67.2\,\% of records, so the trivial baseline already has accuracy 0.672. The best model's accuracy of 0.972 corresponds to macro-F1 0.901 and web-attack F1 values of 0.53 and 0.59: a systematic failure on two classes that accuracy cannot reveal, nor whether a one-point difference is noise (fold standard deviations of macro-F1 are 0.02).""")
body = repl_par(body, "\\textbf{1. Sample, not full data.}", r"""\textbf{1. Sample, not full data.} All results come from \emph{one} stratified sample of 6{,}000 records out of 2.5\,M de-duplicated flows (0.24\,\%), because exact KPCA is quadratic in memory. The sample has a floor of 100 records per class and is \emph{not} prevalence-preserving: attack classes are over-represented, so accuracy, macro-F1 and class priors do not describe deployment-time prevalence. Heartbleed (11 records), SQL injection (21) and infiltration (36) are complete but tiny, so their per-class estimates are very uncertain, and another random sample could change rankings that differ by a few points. We did not repeat the pipeline over several sampling seeds.""")

body = body.replace(" The main grid takes about 30 minutes on two cores and the nested cross-validation about one hour.", "")
body = body.replace(" We did not extract their numerical results.", "").replace(" (we did not extract their numbers)", "")
body = body.replace(" This section is not a systematic survey. IEEE Xplore", " This is not a systematic survey. IEEE Xplore")

body = repl_par(body, "\\textbf{Untested explanations.}", r"""\textbf{Untested explanations.} Tree ensembles are insensitive to monotone feature scaling, and a few leading components may discard low-variance but discriminative directions; we did not test these hypotheses.""")
body = body.replace(" These checks assume that row order follows capture time, score only a subset of classes and use single splits or five folds, so they support the ranking but give no precise penalty. Full tables are in the repository.", " These checks assume that row order follows capture time and score only a subset of classes, so they support the ranking but give no precise penalty (tables in the repository).")
body = body.replace("Motivated by these works we (a) fit every data-dependent step on training folds only, (b) report class-aware metrics beside accuracy, (c) include trivial and no-reduction baselines, and (d) state what our sample cannot show.", "Following them we fit every data-dependent step on training folds only, report class-aware metrics beside accuracy, include trivial and no-reduction baselines, and state what our sample cannot show.")

body = body.replace("\\includegraphics[width=\\textwidth]{figures/fig10_all_executions.pdf}", "\\includegraphics[width=0.8\\textwidth]{figures/fig10_all_executions.pdf}").replace("\\includegraphics[width=\\textwidth]{figures/fig11_accuracy_comparison.pdf}", "\\includegraphics[width=0.72\\textwidth]{figures/fig11_accuracy_comparison.pdf}")
body = repl_par(body, "\\section{Discussion}", r"""\section{Discussion}
\textbf{Answers to the research questions.} RQ1/RQ2: reducing 78 standardised features to 5--30 PCA or KPCA components generally did not improve and usually lowered macro-F1: clearly for decision tree and random forest, negligibly for logistic regression (30 components) and $k$-NN; the one gain, RBF-SVM with cosine KPCA, largely disappeared under tuning (0.076 to 0.021). RQ3: for $k$-NN, DT and RF the kernel mattered slightly more than component count, for LR and SVM the reverse; default-$\gamma$ RBF was weakest for four of five classifiers, and linear KPCA equals PCA. RQ4: KPCA multiplied reducer fit time by more than 200 and traced memory by about 37 at $n=4{,}800$ (quadratic in memory) with no benefit for four of five classifiers. RQ5: orderings were stable across repeated folds, training sizes, nested selection, tuning, and the scorable row-order splits.""")
body = repl_par(body, "\\subsection{Accuracy comparison", r"""\subsection{Accuracy comparison with recent studies}
Fig.~\ref{fig:cmp} and Table~\ref{tab:lit} show reported accuracy side by side. The recent studies quote 97.7--99.99\,\% on their own datasets and splits, whereas our random forest reaches 97.2\,\% accuracy but 0.901 macro-F1 on a sample that over-represents attacks. These numbers measure different things; they show only that accuracy near 100\,\% on imbalanced flow data can coexist with weak minority-class detection, as our per-class results show.
""")

body = drop_env(body, "tab:best", "table")
body = body.replace("(Table~\\ref{tab:best})", "(table in the repository)")

body = repl_par(body, "\\textbf{Setup.}", r"""\textbf{Setup.} A 2-vCPU, 7\,GB VM (Python 3.13, scikit-learn 1.9) ran the main grid (2{,}850 fits, about 28 min), nested CV (about 64 min) and tuning (about 16 min).""")
body = body.replace("We surveyed fifteen studies. Table~\\ref{tab:lit} lists five recent (2025) intrusion-detection studies with the algorithm, dataset and result \\emph{as stated by their authors}; the remaining ten, covering the dataset, its known problems, dimensionality reduction and evaluation practice, are discussed below. The reported numbers use different datasets, splits and metrics and must not be read as a ranking.", "We surveyed fifteen studies. Table~\\ref{tab:lit} lists five recent (2025) studies with algorithm, dataset and result \\emph{as stated by their authors}; ten more, on the dataset, its problems, dimensionality reduction and evaluation practice, are discussed below. Their numbers use different datasets, splits and metrics and are not a ranking.")

body = body.replace(" (cross-evaluation is discussed in \\cite{apruzzese2022}; evaluation pitfalls in \\cite{arp2022})", "")
body = repl_par(body, "\\textbf{Untested explanations.}", r"""\textbf{Untested explanations.} Tree ensembles are scale-insensitive, and a few leading components may discard discriminative low-variance directions; untested.""")

head = r"""\documentclass[runningheads]{llncs}
% PROVISIONAL: official Springer LLNCS class v2.26 (CTAN mirror of Springer's llncs package). Generated by build_main.py.
% (no T1 fontenc: avoids bitmap font generation)
\AtBeginDocument{\pdfpagewidth=210mm \pdfpageheight=297mm} % A4 PDF; llncs fixes only the 12.2x19.3 cm text block
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{url}
\usepackage{array}
\setcounter{topnumber}{3}\setcounter{totalnumber}{5}\renewcommand{\topfraction}{0.9}\renewcommand{\bottomfraction}{0.8}\renewcommand{\textfraction}{0.1}\renewcommand{\floatpagefraction}{0.75}
\begin{document}
\title{Does Dimensionality Reduction Help Classical Intrusion Detection? Original Features versus PCA and Kernel PCA on a Class-Stratified CIC-IDS2017 Sample}
\titlerunning{Dimensionality Reduction for Classical Intrusion Detection}
\author{[AUTHOR NAME 1 -- TO BE FILLED]\inst{1} \and [AUTHOR NAME 2 -- TO BE FILLED]\inst{1}}
\authorrunning{[A. Author et al. -- TO BE FILLED]}
\institute{[DEPARTMENT, INSTITUTION, CITY, COUNTRY -- TO BE FILLED]\\ \email{[EMAIL -- TO BE FILLED]}}
\maketitle
\begin{abstract}
""" + abstract + r"""

\keywords{Network intrusion detection \and CIC-IDS2017 \and Kernel PCA \and Dimensionality reduction \and Class imbalance \and Machine learning.}
\vspace{2pt}\noindent\textit{Code and results:} [REPOSITORY URL / ARCHIVE DOI -- TO BE FILLED BY THE AUTHORS]
\end{abstract}

"""
ack = r"""
\section*{Acknowledgments and AI-assistance disclosure}
\textbf{[THE AUTHORS MUST CONFIRM THAT THIS DISCLOSURE IS ACCURATE AND COMPLETE, AND ADD ANY OTHER TOOL USED, BEFORE SUBMISSION.]} Generative AI was used in this work: Claude (Anthropic; Claude Code, model Claude Sonnet 5.5) helped (i) write and revise the Python pipeline (data preparation, cross-validation, nested CV, tuning, row-order checks, statistics, runtime benchmark, tables, figures and an automated claim checker); (ii) draft and edit the text of all sections, including the abstract, captions and limitations; and (iii) look up and cross-check bibliographic metadata and statements attributed to cited sources. All reported numbers were produced by code run on the data described and re-checked by script. The authors reviewed the content and remain fully responsible for it. [FUNDING / ACKNOWLEDGMENTS -- TO BE FILLED BY THE AUTHORS.] The authors declare no competing interests [TO BE CONFIRMED BY THE AUTHORS].

\bibliographystyle{splncs04}
\bibliography{references}
\end{document}
"""
_o="Of the 30 Holm-corrected comparisons, 23 were significant."
assert _o in body
_f=r"(statistics 46.8--57.6 and 51.9--58.1, Holm-adjusted $p\le 2.7\times10^{-9}$ in every case)"
print("F",_f in body)
body=body.replace(_f,r"(all Holm-adjusted $p\le 2.7\times10^{-9}$)")
body=body.replace(_o,"Of the 30 comparisons, 23 had Holm-adjusted $p<0.05$ (screening only).")
_P=[('On a 6{,}000-record sample drawn after exact same-label duplicate removal from all eight CIC-IDS2017 files, with fold-wise fitting of imputation, scaling and reduction, a random forest on the original 78 features had the highest observed macro-F1 (0.901 $\\pm$ 0.020; accuracy 0.972 $\\pm$ 0.004; 0.900 $\\pm$ 0.022 with nested selection). PCA and KPCA with 5--30 components generally did not improve on the original features: they were clearly worse for decision tree and random forest, practically equal for logistic regression (30 components) and $k$-NN, and helped mainly the RBF-SVM (cosine KPCA), an advantage that shrank from 0.076 to 0.021 after tuning. The ranking survived row-order checks that rest on an assumed row order. Linear KPCA coincided with PCA. KPCA cost more than 200 times more fit time and 37 times more traced memory at 4{,}800 records. Accuracy (0.972) concealed weak detection of web brute force and XSS (F1 0.53, 0.59). The results are limited to this sample and to CIC-IDS2017.','On a 6{,}000-record sample drawn from all eight CIC-IDS2017 files after exact same-label duplicate removal, with imputation, scaling and reduction fitted inside each training fold, a random forest on the original 78 features scored highest: macro-F1 0.901 $\\pm$ 0.020, accuracy 0.972 $\\pm$ 0.004, and 0.900 $\\pm$ 0.022 with nested selection. PCA and KPCA with 5--30 components mostly did not beat the original features. They were clearly worse for the decision tree and random forest and practically equal for logistic regression (30 components) and $k$-NN. Only the RBF-SVM gained, with cosine KPCA, and that advantage shrank from 0.076 to 0.021 after tuning. The ranking also held in the two row-order checks, which rest on the unproven assumption that row order follows capture time. Linear KPCA coincided with PCA. At 4{,}800 records KPCA needed more than 200 times the fit time and about 37 times the traced memory. Accuracy (0.972) concealed weak detection of web brute force and XSS (F1 0.53, 0.59). The results apply to this sample and to CIC-IDS2017 only.'),
('This study proposes no new algorithm, and we make no claim of state-of-the-art, real-time, production-ready or generalizable performance. The supported finding is narrower: on this sample, original features were at least as good as PCA or KPCA for four of five classifiers, the one exception largely vanished with tuning, and accuracy hid a systematic failure on web attacks.','We propose no new algorithm and claim no state-of-the-art, real-time, production-ready or generalizable performance. The supported finding is narrower: on this sample, original features were at least as good as PCA or KPCA for four of five classifiers, the one exception largely vanished with tuning, and accuracy hid a systematic failure on web attacks.'),
('These limitations are real, and the conclusions should be read as conditional on them.','The conclusions depend on the limitations below.'),
("\\textbf{Why accuracy misleads.} The benign class is 67.2\\,\\% of records, so the trivial baseline already has accuracy 0.672. The best model's accuracy of 0.972 corresponds to macro-F1 0.901 and web-attack F1 values of 0.53 and 0.59: a systematic failure on two classes that accuracy cannot reveal, nor whether a one-point difference is noise (fold standard deviations of macro-F1 are 0.02).","\\textbf{Why accuracy misleads.} Benign flows are 67.2\\,\\% of the sample, so a trivial classifier already scores 0.672 accuracy. The best model's accuracy of 0.972 goes with a macro-F1 of 0.901 and web-attack F1 values of only 0.53 and 0.59. Accuracy hides that failure on two classes. It also cannot tell us whether a one-point difference is noise; the fold standard deviation of macro-F1 is about 0.02."),
('\\textbf{Answers to the research questions.} RQ1/RQ2: reducing 78 standardised features to 5--30 PCA or KPCA components generally did not improve and usually lowered macro-F1: clearly for decision tree and random forest, negligibly for logistic regression (30 components) and $k$-NN; the one gain, RBF-SVM with cosine KPCA, largely disappeared under tuning (0.076 to 0.021). RQ3: for $k$-NN, DT and RF the kernel mattered slightly more than component count, for LR and SVM the reverse; default-$\\gamma$ RBF was weakest for four of five classifiers, and linear KPCA equals PCA. RQ4: KPCA multiplied reducer fit time by more than 200 and traced memory by about 37 at $n=4{,}800$ (quadratic in memory) with no benefit for four of five classifiers. RQ5: orderings were stable across repeated folds, training sizes, nested selection, tuning, and the scorable row-order splits.','\\textbf{Answers to the research questions.} RQ1 and RQ2: reducing the 78 standardised features to 5--30 PCA or KPCA components mostly did not help and usually lowered macro-F1. The loss was clear for the decision tree and random forest and negligible for logistic regression (30 components) and $k$-NN. The one gain, the RBF-SVM with cosine KPCA, largely disappeared under tuning (0.076 to 0.021). RQ3: for $k$-NN, DT and RF the kernel mattered slightly more than the number of components; for LR and SVM it was the other way round. Default-$\\gamma$ RBF was weakest for four of five classifiers, and linear KPCA equals PCA. RQ4: at $n=4{,}800$, KPCA multiplied reducer fit time by more than 200 and traced memory by about 37 (memory grows quadratically), with no benefit for four of five classifiers. RQ5: orderings were stable across repeated folds, training sizes, nested selection, tuning and the scorable row-order splits.'),
('We surveyed fifteen studies. Table~\\ref{tab:lit} lists five recent (2025) studies with algorithm, dataset and result \\emph{as stated by their authors}; ten more, on the dataset, its problems, dimensionality reduction and evaluation practice, are discussed below. Their numbers use different datasets, splits and metrics and are not a ranking.','We surveyed fifteen studies. Table~\\ref{tab:lit} lists five recent (2025) ones with algorithm, dataset and result \\emph{as stated by their authors}; the other ten, on the dataset and its problems, dimensionality reduction and evaluation practice, are discussed below. Their numbers come from different datasets, splits and metrics, so they are not a ranking.'),
('\\textbf{Contributions.} (i) A reproducible comparison of original features, PCA and three KPCA kernels over five classical classifiers on a raw-data-derived sample drawn after exact same-label duplicate removal, with fold-wise fitting, a majority-class baseline, a nested-CV check of selection optimism and a small nested hyper-parameter search. (ii) A class-aware analysis showing how much accuracy overstates detection quality. (iii) Paired statistical tests with an explicit independence caveat, and two row-order robustness checks (proxy chronology). (iv) A runtime and memory measurement of KPCA against PCA. We do not propose a new algorithm; code and results are described in the Data and Code Availability section.','\\textbf{Contributions.} (i) A reproducible comparison of the original features, PCA and three KPCA kernels over five classical classifiers, on a sample taken from the raw files after exact same-label duplicate removal. It uses fold-wise fitting, a majority-class baseline, a nested-CV check of selection optimism and a small nested hyper-parameter search. (ii) A class-aware analysis of how far accuracy overstates detection quality. (iii) Paired statistical tests with an explicit independence caveat, plus two row-order robustness checks (proxy chronology). (iv) A runtime and memory comparison of KPCA with PCA. We propose no new algorithm. Code and results are described in the Data and Code Availability section.'),
('\\textbf{Research questions.} We ask: \\textbf{RQ1} how does reduction affect multi-class detection performance; \\textbf{RQ2} does KPCA beat the original space or conventional PCA; \\textbf{RQ3} how do kernel, component count and classifier interact; \\textbf{RQ4} what does the reduction cost in time and memory; \\textbf{RQ5} how stable are the conclusions under repeated, class-aware validation, nested selection, tuning, row-order splits (a proxy for chronology) and smaller training sets.','\\textbf{Research questions.} \\textbf{RQ1:} how does reduction change multi-class detection performance? \\textbf{RQ2:} does KPCA beat the original space or ordinary PCA? \\textbf{RQ3:} how do kernel, number of components and classifier interact? \\textbf{RQ4:} what does reduction cost in time and memory? \\textbf{RQ5:} do the conclusions hold under repeated class-aware validation, nested selection, tuning, row-order splits (a proxy for chronology) and smaller training sets?'),
('Three methodological issues make such comparisons hard to interpret. First, CIC-IDS2017 is class-imbalanced and, in its original form, contains labelling and flow-construction problems \\cite{engelen2021,panigrahi2018}, so accuracy can be dominated by the benign majority. Second, pitfalls in security-oriented machine learning can lead to over-optimistic performance estimates \\cite{arp2022}. Third, a no-reduction baseline is the necessary control for any claim that reduction helps; without it, a benefit is assumed rather than measured.','Three problems make these comparisons hard to read. CIC-IDS2017 is imbalanced and, in its original form, has labelling and flow-construction errors \\cite{engelen2021,panigrahi2018}, so the benign majority can dominate accuracy. Security-oriented machine learning is also prone to pitfalls that inflate results \\cite{arp2022}. And a claim that reduction helps needs a no-reduction baseline; without one, the benefit is assumed, not measured.'),
('Machine-learning network intrusion detection systems (NIDS) are commonly developed and compared on public flow datasets \\cite{ring2019}, of which CIC-IDS2017 \\cite{sharafaldin2018} is widely used. Its flow records, as distributed in the MachineLearningCVE files, carry 78 numeric features, which motivates dimensionality reduction as a way to cut training cost and possibly improve generalization. Linear PCA and auto-encoders have been applied to CIC-IDS2017 \\cite{abdulhammed2019}, and Kernel PCA (KPCA) \\cite{scholkopf1998}, which performs PCA in an implicit nonlinear feature space, has been combined with SVMs for intrusion detection \\cite{kuang2014}.','Researchers often develop and compare network intrusion detection systems (NIDS) on public flow datasets \\cite{ring2019}, and CIC-IDS2017 \\cite{sharafaldin2018} is one of the most used. In the MachineLearningCVE files its flow records have 78 numeric features. That number invites dimensionality reduction, either to cut training cost or in the hope of better generalization. Linear PCA and auto-encoders have been tried on CIC-IDS2017 \\cite{abdulhammed2019}. Kernel PCA (KPCA) \\cite{scholkopf1998} runs PCA in an implicit nonlinear feature space and has been paired with SVMs for intrusion detection \\cite{kuang2014}.'),
('\\textbf{Untested explanations.} Tree ensembles are scale-insensitive, and a few leading components may discard discriminative low-variance directions; untested.','\\textbf{Untested explanation.} A few leading components may discard discriminative low-variance directions.'),
('The ranking survived row-order checks that rest on an assumed row order.','The ranking also held in the two row-order checks, which depend on the unproven assumption that row order follows capture time.'),
('The conclusions apply to random and within-file row-ordered splits of CIC-IDS2017 only; they say nothing about true temporal drift.','These conclusions hold only for random and within-file row-ordered splits of CIC-IDS2017, not for drift over real time.'),
('Choosing the best of 189 configurations (21 feature spaces $\\times$ 9 classifier/weighting variants) on the scoring folds is optimistic. On the \\emph{same} 15 outer folds, a stratified 3-fold inner cross-validation inside each outer training set (4{,}800 records) scores every configuration by macro-F1, the best is selected, and only it is scored on the untouched outer test fold. We apply this to (A) the global selection and, per classifier, to (C) the best \\emph{reduced} space and weighting versus (D) the original space with weighting chosen the same way; all steps are refitted on every inner split.','Picking the best of 189 configurations (21 feature spaces $\\times$ 9 classifier and weighting variants) on the same folds that score it flatters the winner. To measure this, selection is nested: inside each of the 15 outer training sets (4{,}800 records) a stratified 3-fold inner cross-validation scores every configuration by macro-F1, the winner is chosen there, and only that winner is scored on the outer test fold it never saw. We run this for (A) the global choice and, for each classifier, for (C) the best \\emph{reduced} space with weighting versus (D) the original space with weighting chosen the same way.'),
('Following them we fit every data-dependent step on training folds only, report class-aware metrics beside accuracy, include trivial and no-reduction baselines, and state what our sample cannot show. This is not a systematic survey. IEEE Xplore pages could not be retrieved from our environment, so the studies above come from open publisher and preprint pages.','From them we took three practices: every data-dependent step is fitted on training folds only, accuracy is always reported next to class-aware metrics, and every reduction is compared with a trivial baseline and a no-reduction baseline. This is not a systematic survey. IEEE Xplore was unreachable, so all studies above come from open publisher or preprint pages.'),
("matched them for logistic regression and $k$-nearest neighbors;","matched them at the best component count for logistic regression and $k$-nearest neighbors;"),
("Reduced spaces suffered at least as much (RF: PCA-10 0.759, cosine KPCA-30 0.704), so","For DT, RF and LR the reduced spaces lost at least as much (RF: PCA-10 0.759, cosine KPCA-30 0.704), so"),
("state that a feature-importance-guided autoencoder outperforms PCA on three datasets","state that a feature-importance-guided autoencoder outperforms earlier dimensionality-reduction techniques on three datasets"),
("quote 97.7--99.99\\,\\%","quote 97.75--99.9965\\,\\%")]
_t=head+body+ack
for _a,_b in _P:
    print("patch",_a[:30],_a in _t); _t=_t.replace(_a,_b)
open("main.tex", "w").write(_t)
print("main.tex written", len(body.split()), "body words")
