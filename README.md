# ACN PROJECT V2 - Kernel PCA + Classifiers for Network Intrusion Detection (CIC-IDS2017)

A controlled comparison of five classifiers on CIC-IDS2017 flow data after **Kernel PCA** dimensionality reduction.
Grid: **3 test sizes x 3 Kernel-PCA settings x 5 algorithms = 45 experiments**, one script and one result image per experiment.

## Experimental design

| Factor | Values |
|---|---|
| Test size | 0.2, 0.4, 0.6 |
| Kernel PCA (kernel -> components) | RBF -> 5, Linear -> 10, Cosine -> 15 |
| Classifiers | Logistic Regression, KNN (k=5), Support Vector Machine (RBF, C=1), Decision Tree (entropy), Random Forest (100 trees) |

- **Data:** CIC-IDS2017 Tuesday + Wednesday + Thursday-morning CSVs (1,308,978 flows, 11 classes: BENIGN, DoS Hulk / GoldenEye / slowloris / Slowhttptest, FTP-Patator, SSH-Patator, three web attacks, Heartbleed).
- **Cleaning:** strip column names, coerce to numeric, replace inf with NaN, mean-impute, label-encode.
- **Sample:** Kernel PCA is O(n^2) in memory/time, so the experiments use a **1000-row stratified sample** (>= 10 rows per class so rare attacks survive stratified splitting; 718 of 1000 rows are BENIGN).
- **Pipeline per run:** stratified split (`random_state=42`) -> `StandardScaler` (fit on train) -> `KernelPCA` (fit on train, default gamma) -> classifier -> weighted precision / recall / F1 + confusion matrix.
- **Note:** this is the second variant of the project, with a different algorithm set (SVM and Random Forest replace XGBoost and QDA).

## Results (accuracy / weighted F1)

| Algorithm | Kernel PCA (nComp) | Test 0.2 Acc / F1 | Test 0.4 Acc / F1 | Test 0.6 Acc / F1 |
|---|---|---|---|---|
| Logistic Regression | RBF (5) | 0.8050 / 0.7463 | 0.8100 / 0.7534 | 0.8150 / 0.7591 |
|  | Linear (10) | 0.8500 / 0.8118 | 0.8600 / 0.8249 | 0.8583 / 0.8229 |
|  | Cosine (15) | 0.8550 / 0.8023 | 0.8600 / 0.8074 | 0.8600 / 0.8074 |
| KNN (k=5) | RBF (5) | 0.8450 / 0.8476 | 0.8775 / 0.8694 | 0.8683 / 0.8625 |
|  | Linear (10) | 0.8650 / 0.8613 | 0.8850 / 0.8793 | 0.8867 / 0.8795 |
|  | Cosine (15) | 0.8800 / 0.8824 | 0.8875 / 0.8836 | 0.8817 / 0.8788 |
| Support Vector Machine (RBF) | RBF (5) | 0.8000 / 0.7400 | 0.8125 / 0.7558 | 0.8167 / 0.7607 |
|  | Linear (10) | 0.8500 / 0.8063 | 0.8475 / 0.8064 | 0.8517 / 0.8075 |
|  | Cosine (15) | 0.8750 / 0.8409 | 0.8775 / 0.8492 | 0.8750 / 0.8435 |
| Decision Tree (entropy) | RBF (5) | 0.8550 / 0.8572 | 0.8525 / 0.8605 | 0.8733 / 0.8749 |
|  | Linear (10) | 0.9000 / 0.9062 | 0.8775 / 0.8765 | 0.9083 / 0.9106 |
|  | Cosine (15) | 0.8550 / 0.8651 | 0.8925 / 0.8918 | 0.9000 / 0.9000 |
| Random Forest (100 trees) | RBF (5) | 0.8950 / 0.8925 | 0.9075 / 0.8986 | 0.9117 / 0.9055 |
|  | Linear (10) | 0.9150 / 0.9111 | 0.9275 / 0.9239 | 0.9300 / 0.9237 |
|  | Cosine (15) | 0.9050 / 0.8981 | 0.9275 / 0.9224 | 0.9233 / 0.9173 |

Best run: **Random Forest (100 trees), linear Kernel PCA (10 components), test size 0.6 - accuracy 0.9300**. Random Forest is the strongest family across all nine settings; Logistic Regression and SVM suffer most with RBF (5 components).

Full tables (all four metrics, per-algorithm grids) are in `results/model_performance_comparison.xlsx`; raw rows in `results/results.csv`.
Each script saves one JPG beside it with its console output, metric chart and confusion matrix, e.g. `random_forest/Test0.6_nComp10_RF.jpg`.

## Limitations - please read

- **Small sample, single split.** 1000 rows and one split per run: rare attack classes have only 2-6 test rows, so differences of a point or two are noise. No cross-validation or significance tests.
- **Accuracy is inflated by class imbalance.** Predicting BENIGN for everything scores 71.8% on this sample; compare weighted F1 and the confusion matrices.
- **Not comparable to full-data results** reported in the literature (typically 98-99%).
- Uses 3 of the 8 CIC-IDS2017 files; no hyper-parameter tuning; no no-reduction baseline.

## Reproduce

```bash
pip install -r requirements.txt

# 1. Download CIC-IDS2017 "MachineLearningCSV.zip" from the Canadian Institute for Cybersecurity
#    (https://www.unb.ca/cic/datasets/ids-2017.html) and unzip so the CSVs are in ./MachineLearningCVE/
python prepare_data.py MachineLearningCVE   # builds data/sample.npz (a prebuilt copy is included)

python make_scripts.py                      # (re)generates the 45 scripts
python run_all.py                           # runs all 45 and builds results/ workbook + CSV
python logistic/Test0.2_nComp5_LR.py      # or run a single experiment
```

## Run in Spyder / VS Code / PyCharm / Jupyter

Open any script under `<algorithm>/` and press Run (F5 in Spyder). No arguments and no working-directory setup are needed: it finds `data/sample.npz` itself,
prints the confusion matrix, metrics and classification report to the console, shows the result image, and saves it as `<name>.jpg` next to the script. The JPG contains the console output plus the metric chart and confusion-matrix heatmap.
`run_all.py` runs all 45 without opening chart windows.

## Repository layout

```
prepare_data.py     load + clean + stratified 1000-row sample -> data/sample.npz
make_scripts.py     generates the 45 experiment scripts
run_all.py          runs everything, writes results/
data/sample.npz     cached sample (so scripts run without the raw CSVs)
<algo>/             Test<size>_nComp<n>_<ALG>.py  +  matching .jpg (console output + charts)
results/            results.csv, model_performance_comparison.xlsx, json/ (one metrics file per run)
```

## Dataset citation

Sharafaldin, I., Lashkari, A. H., Ghorbani, A. A. *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.* ICISSP 2018.
