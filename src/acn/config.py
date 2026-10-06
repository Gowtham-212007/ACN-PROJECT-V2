"""Central configuration. Every experiment parameter lives here (or is exposed as a CLI flag)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_NPZ = ROOT / "data" / "sample.npz"          # 1000-row stratified CIC-IDS2017 sample (existing)
RAW_DIR = ROOT / "results" / "raw"
TABLE_DIR = ROOT / "results" / "tables"
FIG_DIR = ROOT / "results" / "figures"

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
