"""Central configuration. Every experiment parameter lives here (or is exposed as a CLI flag)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import os
RUN = os.environ.get("ACN_RUN", "")      # "" = archived v1 run (1000-row cached sample); "v2" = raw-data run (results/v2, papers/ieee/tables_v2)
if RUN == "v2":
    SAMPLE_NPZ = ROOT / "data" / "sample_raw6000.npz"   # 6000-row sample built from the raw CSVs by prepare_raw.py
    _R = ROOT / "results" / "v2"; TEX_DIR = ROOT / "papers" / "ieee" / "tables_v2"
else:
    SAMPLE_NPZ = ROOT / "data" / "sample.npz"          # 1000-row stratified CIC-IDS2017 sample (existing, archived v1 run)
    _R = ROOT / "results"; TEX_DIR = ROOT / "papers" / "ieee" / "tables"
RAW_DIR = _R / "raw"
TABLE_DIR = _R / "tables"
FIG_DIR = _R / "figures"
for _d in (RAW_DIR, TABLE_DIR, FIG_DIR, TEX_DIR): _d.mkdir(parents=True, exist_ok=True)

SEED = 42                      # master seed for every split and every stochastic model
N_SPLITS = 5                   # stratified K-fold
N_REPEATS = 3                  # repeated K-fold -> 15 paired observations per configuration
COMPONENTS = [5, 10, 15, 20, 30]
KERNELS = ["linear", "rbf", "cosine"]
MATCHED_N = 10                 # component count used for the matched PCA-vs-KPCA statistical comparison
CLASSIFIERS = ["LR", "KNN", "SVM", "DT", "RF"]
CLASS_WEIGHT_CAPABLE = ["LR", "SVM", "DT", "RF"]   # KNN has no class_weight option

CLF_NAMES = {"LR": "Logistic Regression", "KNN": "k-NN (k=5)", "SVM": "SVM (RBF)",
             "DT": "Decision Tree", "RF": "Random Forest", "DUMMY": "Majority class"}
