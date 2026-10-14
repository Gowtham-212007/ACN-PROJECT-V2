# PARAGRAPH_AUDIT

Verification: numbers checked against results/v2/tables/claim_check.csv (232/232 pass), nested_*.csv, stat_*.csv and earlier literature audits (REFERENCE_AUDIT.md). Unchanged = already clear, accurate and appropriately qualified.

| ID | Opening | Decision | Note |
|---|---|---|---|
| P001 | abstract Kernel principal component analysis (KPCA) is often | Small edit | Rewrote first sentence: removed the unsupported claim that gains are reported on a single split. |
| P002 | Network intrusion detection \and CIC-IDS2017 \and Kernel PCA | No change | Clear and verified against artifacts where numeric. |
| P003 | Introduction Researchers usually build and compare network i | Small edit | Plain-language edit (previous turn). |
| P004 | Such comparisons are hard to read for three reasons. First,  | Small edit | Plain-language edit. |
| P005 | Research questions. RQ1: how does reduction change multi-cla | No change | Clear and verified against artifacts where numeric. |
| P006 | Contributions. (i) A reproducible comparison of the original | No change | Clear and verified against artifacts where numeric. |
| P007 | Related Work We read fifteen studies. Table~tab:lit gives fi | Small edit | Plain-language edit. |
| P008 | Dataset and its quality. Ring et al.~ring2019 survey public  | No change | Clear and verified against artifacts where numeric. |
| P009 | Dimensionality reduction. Abdulhammed et al.~abdulhammed2019 | No change | Clear and verified against artifacts where numeric. |
| P010 | Evaluation methodology. Arp et al.~arp2022 describe pitfalls | No change | Clear and verified against artifacts where numeric. |
| P011 | CAPTION: Recent studies (2025) and this work. Results are qu | Reviewed | Caption states scope/non-comparability where relevant. |
| P012 | Dataset and Preprocessingsec:data Data. We use the eight dai | No change | Clear and verified against artifacts where numeric. |
| P013 | Duplicates. 308{,381 flows (10.9\,\%) are exact duplicates ( | No change | Clear and verified against artifacts where numeric. |
| P014 | Sample. Exact KPCA needs an n\times n kernel matrix, so we d | No change | Clear and verified against artifacts where numeric. |
| P015 | Methodologysec:method Pipeline. Fig.~fig:pipe shows the prot | No change | Clear and verified against artifacts where numeric. |
| P016 | Algorithm and formulas. Algorithm~alg:cv summarises one eval | Small edit | Removed editorial parenthetical about the library; text now only states the scaling. |
| P017 | centred as K=K-1_nK-K1_n+1_nK1_n; with 1_n the n\times n mat | No change | Clear and verified against artifacts where numeric. |
| P018 | and balanced accuracy equals macro-recall. The multi-class M | No change | Clear and verified against artifacts where numeric. |
| P019 | CAPTION: Fold-wise evaluation of one feature space S and cla | Reviewed | Caption states scope/non-comparability where relevant. |
| P020 | CAPTION: Experimental pipeline. All data-dependent preproces | Reviewed | Caption states scope/non-comparability where relevant. |
| P021 | Classifiers. Logistic regression (L2, lbfgs), k-NN with k=5  | No change | Clear and verified against artifacts where numeric. |
| P022 | Validation. Repeated stratified 5-fold cross-validation, 3 r | No change | Clear and verified against artifacts where numeric. |
| P023 | Nested cross-validation for selection. Picking the best of 1 | No change | Clear and verified against artifacts where numeric. |
| P024 | Nested hyper-parameter search. For k-NN, SVM and random fore | No change | Clear and verified against artifacts where numeric. |
| P025 | Row-order robustness checks (proxy chronology). The raw file | No change | Clear and verified against artifacts where numeric. |
| P026 | Metrics. Accuracy; macro-precision, macro-recall and macro-F | No change | Clear and verified against artifacts where numeric. |
| P027 | Statistics. Per classifier we compare feature spaces at matc | No change | Clear and verified against artifacts where numeric. |
| P028 | Cost. A serial benchmark (no parallel workers) records train | No change | Clear and verified against artifacts where numeric. |
| P029 | Setup. A 2-vCPU, 7\,GB VM (Python 3.13, scikit-learn 1.9) ra | No change | Clear and verified against artifacts where numeric. |
| P030 | Results Original-feature baseline and the cost of reading ac | No change | Clear and verified against artifacts where numeric. |
| P031 | CAPTION: Per-class results of the selected model (RF, origin | Reviewed | Caption states scope/non-comparability where relevant. |
| P032 | Original space versus PCA versus Kernel PCA Table~tab:n10 an | No change | Clear and verified against artifacts where numeric. |
| P033 | A stricter question is whether each classifier's best reduce | No change | Clear and verified against artifacts where numeric. |
| P034 | CAPTION: Mean accuracy and macro-F1 at 10 components (origin | Reviewed | Caption states scope/non-comparability where relevant. |
| P035 | Fig.~fig:all shows all 25 classifier-by-space executions at  | No change | Clear and verified against artifacts where numeric. |
| P036 | CAPTION: Macro-F1 of all classifier \times feature-space exe | Reviewed | Caption states scope/non-comparability where relevant. |
| P037 | Accuracy of each algorithm across feature spaces Fig.~fig:pe | No change | Clear and verified against artifacts where numeric. |
| P038 | CAPTION: Accuracy (mean \pm std over 15 folds, standard clas | Reviewed | Caption states scope/non-comparability where relevant. |
| P039 | Selection optimism: nested cross-validationsec:results-neste | No change | Clear and verified against artifacts where numeric. |
| P040 | Effect of hyper-parameter tuning Table~tab:tuning reports th | No change | Clear and verified against artifacts where numeric. |
| P041 | CAPTION: Nested hyper-parameter search: mean macro-F1 over f | Reviewed | Caption states scope/non-comparability where relevant. |
| P042 | Row-order robustness (proxy chronology) In the head/tail spl | No change | Clear and verified against artifacts where numeric. |
| P043 | Kernel, component count and class weighting Linear KPCA repr | No change | Clear and verified against artifacts where numeric. |
| P044 | Computational cost The serial benchmark (table in the reposi | No change | Clear and verified against artifacts where numeric. |
| P045 | Accuracy comparison with recent studies Fig.~fig:cmp and Tab | No change | Clear and verified against artifacts where numeric. |
| P046 | CAPTION: Accuracy reported by recent studies versus this wor | Reviewed | Caption states scope/non-comparability where relevant. |
| P047 | Discussion Answers to the research questions. RQ1 and RQ2: r | No change | Clear and verified against artifacts where numeric. |
| P048 | Why accuracy misleads. Benign flows make up 67.2\,\% of the  | Small edit | Tightened wording. |
| P049 | Possible explanations (untested). We ran no experiment to se | No change | Clear and verified against artifacts where numeric. |
| P050 | Threats to Validity and Limitations The conclusions depend o | No change | Clear and verified against artifacts where numeric. |
| P051 | 1. Sample, not full data. All results come from one stratifi | No change | Clear and verified against artifacts where numeric. |
| P052 | 2. Leakage status. Sampling was performed on the raw, un-imp | Small edit | Tightened final sentence. |
| P053 | 3. Limited external validity. All data come from one dataset | Small edit | Trimmed redundant clause. |
| P054 | 4. Selection and inference. The headline configuration (RF,  | No change | Clear and verified against artifacts where numeric. |
| P055 | 5. Limited tuning. Hyper-parameter search covered only k-NN, | No change | Clear and verified against artifacts where numeric. |
| P056 | 6. Dataset quality and cost. The original CIC-IDS2017 flows  | No change | Clear and verified against artifacts where numeric. |
| P057 | We propose no new algorithm and claim no state-of-the-art, r | No change | Clear and verified against artifacts where numeric. |
| P058 | Conclusion The question was whether PCA or KPCA improves int | Small edit | Reworded opening. |
| P059 | Future work. Repeat the pipeline over several sampling seeds | No change | Clear and verified against artifacts where numeric. |
| P060 | \section*{Data and Code Availability The raw CIC-IDS2017 Mac | No change | Clear and verified against artifacts where numeric. |
| P061 | \section*{Acknowledgments and AI-assistance disclosure Gener | No change | Clear and verified against artifacts where numeric. |
