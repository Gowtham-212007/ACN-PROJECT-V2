# Literature survey audit (15 IEEE Xplore papers, 2025-2026)
Metadata: Crossref (DOI lookup; all 15 resolved; venue, year, pages, authors). Content: abstracts via Semantic Scholar. IEEE Xplore pages were NOT opened (not reachable from this environment), and full texts were NOT read, except Xu & Liu whose figures (0.9775 overall test set, 0.5863 unknown-attack set) come from the arXiv v2 version (Tables II/III). Authors must confirm each entry on IEEE Xplore.

| # | Paper (DOI 10.1109/...) | Dataset per abstract | Reported figure used in paper | Source of figure |
|---|---|---|---|---|
| 1 | Pramana et al., ICADEIS 2026 (icadeis71120.2026.11644518) | CICIDS2017 | accuracy and F1 0.99996 (ridge-XGBoost) | abstract |
| 2 | Qin, ICNCIS 2025 (icncis67521.2025.11296040) | CIC-IDS2017 | multi-class acc 0.9989, macro-F1 0.7114; binary 0.9995 | abstract |
| 3 | Patil & Joshi, EITES 2025 (eites66543.2025.00014) | CIC-IDS2017 | accuracy 99.21 % | abstract |
| 4 | Ahuja & Vats Doohan, ICTBIG 2025 (ictbig68706.2025.11323800) | "CIC-IDS" (version unstated) | XGBoost 97.73 % | abstract |
| 5 | Amin & Jadhav, ICONAT 2025 (iconat66879.2025.11362473) | CICIDS2017 | accuracy 97.6 % | abstract |
| 6 | Mosally, Cyber-AI 2025 (cyber-ai66431.2025.11233429) | CICIDS2017 | PCA 78->33 (99 % variance); RF > SVM; no figures in abstract | abstract |
| 7 | Zhang et al., ICICR 2025 (icicr65456.2025.00129) | not named in abstract | RF+PCA best among reduction pipelines; no figures | abstract |
| 8 | Vankayalapati et al., ICICACS 2026 (icicacs68679.2026.11578848) | CIC-IDS2017 | 96.3 % multi-class, 99.9 % binary | abstract |
| 9 | G.P. et al., ICSADL 2026 (icsadl67539.2026.11451878) | CICIDS2017 | 1D-CNN 96.34 %, FPR 3.01 % | abstract |
| 10 | Sharma & Kumar, ICIH 2025 (icih67754.2025.11609046) | CIC-IDS2017 | F1 99.6 / 97.4 / 94.7 % (XGBoost / IF / HDBSCAN); accuracy not stated | abstract |
| 11 | Darmono et al., ICCRAIDS 2026 (iccraids67816.2026.11519701) | CICIDS2017 | macro-F1 about 0.973-0.976 | abstract |
| 12 | Xu & Liu, ICETIS 2025 (icetis66286.2025.11144025) | CICIDS2017 | MLP 0.9775 overall / 0.5863 unknown attacks | arXiv v2 Tables II-III |
| 13 | Jiwueze & Varol, IDS 2026 (ids69480.2026.00027) | CIC-IDS-2017 vs a revised dataset | qualitative; no accuracy | abstract |
| 14 | Mohsin et al., DataSciMI 2026 (datascimi67380.2026.11523882) | CICIDS2017 | RF/DT better with engineered features; no figure | abstract |
| 15 | Bandarupalli, CE2CT 2025 (ce2ct64011.2025.10940012) | CIC-IDS-2017 | no figure in abstract | abstract |

Selection rule for the five best (Table 1): highest accuracy stated in the abstract for a multi-class or unspecified task. Papers 6, 7, 10, 11, 13, 14, 15 give no accuracy in their abstracts, which is stated in the paper.
Caveats: #1's 0.99996 may refer to a DDoS-focused model; #4's dataset version is unstated; confirm both on Xplore.
Removed from the reference list (faculty asks for exactly the 15 surveyed papers): Sharafaldin, Ring, Engelen, Panigrahi, Arp, Apruzzese, Abdulhammed, Kuang, Waghmode, Patil (Informatica), Abdelaziz, Emirmahmutoglu, Chavan, Abdel-Rahman, and the method references (Schoelkopf, Cortes, Cover, Quinlan, Breiman, scikit-learn, Chicco, Demsar, Nadeau). The statements they supported are now uncited or reworded.
