# Raw CIC-IDS2017 data verification (MachineLearningCSV.zip, 8 files)
Produced by `python -m src.acn.profile_raw` (raw numbers in `results/raw/raw_profile.json`) and `prepare_raw.py` (`data/sample_raw6000.manifest.json`).
* **Files readable:** all 8 CSVs, identical 79 columns (78 features + Label) in every file.
* **Total flows:** 2,830,743 (matches the 2,830,743 published for the MachineLearningCVE release; Tue+Wed+Thu-am = 1,308,978, matching the original project's README).
* **Classes:** 15 labels (the original 1,000-row sample had 11: Monday, Thursday-afternoon and both Friday sessions were not used).
* **Timestamps:** none in these files (no `Timestamp`, `Flow ID` or IP columns). Day = source file. Row order inside each file is time-structured (attack rows occur in contiguous blocks; e.g. Wednesday attack share 69%/37%/4% across thirds; Monday is a single BENIGN run) - treated as an *assumed* chronological order, not proven.
* **Constant features (all files):** Bwd Avg Bulk Rate, Bwd Avg Bytes/Bulk, Bwd Avg Packets/Bulk, Bwd PSH Flags, Bwd URG Flags, Fwd Avg Bulk Rate, Fwd Avg Bytes/Bulk, Fwd Avg Packets/Bulk. Kept (harmless after scaling) so the 78-feature definition matches the original study. 'Fwd Header Length.1' duplicates 'Fwd Header Length' (known artefact, Engelen et al.).
* **Duplicates:** 308,381 exact duplicate rows (features+label) removed before sampling; 698 feature-duplicate groups carry conflicting labels (kept, informational).
* **Source check:** counts and class names match the published CIC-IDS2017 MachineLearningCVE release; no checksum from the CIC site was available to compare, so provenance is by structure/counts, not by hash.

## Per file
| File | Rows | inf | NaN | rows with NaN/inf | exact duplicates | labels |
|---|---|---|---|---|---|---|
| Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv | 225,745 | 64 | 4 | 34 | 2,633 | DDoS 128,027, BENIGN 97,718 |
| Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv | 286,467 | 727 | 15 | 371 | 72,353 | PortScan 158,930, BENIGN 127,537 |
| Friday-WorkingHours-Morning.pcap_ISCX.csv | 191,033 | 216 | 28 | 122 | 6,888 | BENIGN 189,067, Bot 1,966 |
| Monday-WorkingHours.pcap_ISCX.csv | 529,918 | 810 | 64 | 437 | 26,935 | BENIGN 529,918 |
| Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv | 288,602 | 396 | 18 | 207 | 35,630 | BENIGN 288,566, Infiltration 36 |
| Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv | 170,366 | 250 | 20 | 135 | 6,066 | BENIGN 168,186, Web Attack - Brute Force 1,507, Web Attack - XSS 652, Web Attack - Sql Injection 21 |
| Tuesday-WorkingHours.pcap_ISCX.csv | 445,909 | 327 | 201 | 264 | 24,065 | BENIGN 432,074, FTP-Patator 7,938, SSH-Patator 5,897 |
| Wednesday-workingHours.pcap_ISCX.csv | 692,703 | 1586 | 1008 | 1297 | 81,909 | BENIGN 440,031, DoS Hulk 231,073, DoS GoldenEye 10,293, DoS slowloris 5,796, DoS Slowhttptest 5,499, Heartbleed 11 |

## Class distribution (full data -> de-duplicated pool -> 6000-row sample)
| Class | Raw | Pool | Sample |
|---|---|---|---|
| BENIGN | 2,273,097 | 2,096,484 | 4,034 |
| DoS Hulk | 231,073 | 172,849 | 424 |
| PortScan | 158,930 | 90,819 | 270 |
| DDoS | 128,027 | 128,016 | 340 |
| DoS GoldenEye | 10,293 | 10,286 | 119 |
| FTP-Patator | 7,938 | 5,933 | 111 |
| SSH-Patator | 5,897 | 3,219 | 106 |
| DoS slowloris | 5,796 | 5,385 | 110 |
| DoS Slowhttptest | 5,499 | 5,228 | 110 |
| Bot | 1,966 | 1,953 | 104 |
| Web Attack - Brute Force | 1,507 | 1,470 | 103 |
| Web Attack - XSS | 652 | 652 | 101 |
| Infiltration | 36 | 36 | 36 |
| Web Attack - Sql Injection | 21 | 21 | 21 |
| Heartbleed | 11 | 11 | 11 |

Sampling: seed 0, floor 100 per class (or all if fewer), remainder proportional to pool prevalence; NaN cells left in the sample: 2 (imputed inside training folds only). Sample stores `day` and `order` for chronological splits.
