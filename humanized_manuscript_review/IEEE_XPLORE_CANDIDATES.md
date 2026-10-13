# Verified IEEE (DOI 10.1109) 2025-26 CIC-IDS2017 candidates
Source: Crossref metadata + Semantic Scholar/OpenAlex abstracts. IEEE Xplore pages themselves were not opened; confirm each on Xplore before citing. Figures are from abstracts only.

| Author | Venue | DOI | Method | Reported (abstract) |
|---|---|---|---|---|
| Qin | ICNCIS 2025 | 10.1109/icncis67521.2025.11296040 | RF + Top-20 flow features + fuzzy rules + SMOTE, CIC-IDS2017 | multiclass acc 0.9989, macro-F1 0.7114; LogReg acc 0.8136, macro-F1 0.3427 |
| Amin & Jadhav | ICONAT 2025 | 10.1109/iconat66879.2025.11362473 | RF(200 trees)+SMOTE, CICIDS2017 | acc 97.6%, P 97.62, R 96.64, F1 94 |
| Ahuja & Doohan | ICTBIG 2025 | 10.1109/ictbig68706.2025.11323800 | XGBoost/RF/LightGBM/SVM on 'CIC-IDS dataset' (year not stated in abstract) | XGBoost acc 97.73% |
| Sharma & Kumar | ICIH 2025 | 10.1109/icih67754.2025.11609046 | XGBoost, UMAP-HDBSCAN, Isolation Forest, temporal splits | XGBoost F1 99.6% |
| G.P. et al. | ICSADL 2026 | 10.1109/icsadl67539.2026.11451878 | Explainable IDS; RF/XGBoost/1D-CNN | 1D-CNN acc 96.34%, FPR 3.01% |
| Mosally | CYBER-AI 2025 | 10.1109/cyber-ai66431.2025.11233429 | PCA 78->33 features (99% variance), SMOTE on train only | numbers truncated in abstract |
| Zhang, Chen, Shen | ICICR 2025 | 10.1109/icicr65456.2025.00129 | LR/kNN/NB/RF/DT/MLP with PCA, LDA, FA | dataset not stated in abstract |
| Aswanandini | ICUIS 2025 | 10.1109/icuis67429.2025.11380733 | Fuzzy optimised ICA reduction, CICIDS2017+NSL-KDD | none in abstract |
| Jiwueze & Varol | IEEE IDS 2026 | 10.1109/ids69480.2026.00027 | CIC-IDS-2017 vs BCCC-CIC-IDS-2017, per-class analysis | trees more consistent; minority web attacks scarce |
| Darmono et al. | ICCRAIDS 2026 | 10.1109/iccraids67816.2026.11519701 | 42 features, 7 classes, macro-F1, synthetic augmentation | none in abstract |
| Mohsin et al. | DataSciMI 2026 | 10.1109/datascimi67380.2026.11523882 | Feature engineering + denoising AE + correlation reduction | RF/DT better with engineered features |
| Bandarupalli | CE2CT 2025 | 10.1109/ce2ct64011.2025.10940012 | DNN anomaly IDS, CIC-IDS-2017 | accuracy not seen |

Excluded (not CIC-IDS2017): Sudharshan ICOACT 2025 (KDDCUP), Nivetha ICSCSA 2025 (KDDCUP'99), Ramesh & Sahoo CICN 2025 (NSL-KDD/UNSW-NB15). Unverified: 10.1109/iccnea70678.2026.11722053.
