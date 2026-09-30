#!/usr/bin/env python3
"""Support Vector Machine (RBF) | Test size 0.4 | Kernel PCA kernel=cosine, n_components=15
CIC-IDS2017 (Tue+Wed+Thu-morning) 1000-row stratified sample.
Run in any IDE (Spyder / VS Code / PyCharm / Jupyter): open the file and press Run, no arguments needed.
Saves next to this file: 'Test0.4_nComp15_SVM.jpg' - one image with the console output (confusion matrix, metrics, classification report) plus charts."""
import json, os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import KernelPCA
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

TEST_SIZE, KERNEL, N_COMP, ALG, ALG_NAME = 0.4, "cosine", 15, "SVM", "Support Vector Machine (RBF)"
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:                      # Jupyter / interactive console
    HERE = os.getcwd()
def _find_root():                      # folder that contains data/sample.npz (works from any working directory)
    for p in (HERE, os.path.join(HERE, ".."), os.path.join(HERE, "..", ".."), os.getcwd()):
        if os.path.exists(os.path.join(p, "data", "sample.npz")):
            return os.path.abspath(p)
    raise FileNotFoundError("data/sample.npz not found - run prepare_data.py or keep the repo folder structure")
ROOT = _find_root()
tag = f"Test{TEST_SIZE}_nComp{N_COMP}_{ALG}"

# 1. LOAD cached, cleaned sample (see prepare_data.py)
d = np.load(os.path.join(ROOT, "data", "sample.npz"), allow_pickle=True)
X, y, class_names = d["X"], d["y"], [str(c).replace("�", "-") for c in d["classes"]]

# 2. SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=42, stratify=y)

# 3. SCALE (fit on train only)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train); X_test = scaler.transform(X_test)

# 4. DIMENSIONALITY REDUCTION: Kernel PCA (fit on train only; gamma = sklearn default 1/n_features)
kpca = KernelPCA(n_components=N_COMP, kernel=KERNEL, random_state=0)
X_train = kpca.fit_transform(X_train); X_test = kpca.transform(X_test)

# 5. CLASSIFIER
classifier = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

# 6. METRICS
labels = np.arange(len(class_names))
cm = confusion_matrix(y_test, y_pred, labels=labels)
res = dict(test_size=TEST_SIZE, kernel=KERNEL, n_components=N_COMP, algorithm=ALG, model=ALG_NAME,
           n_train=int(len(y_train)), n_test=int(len(y_test)),
           accuracy=accuracy_score(y_test, y_pred),
           precision=precision_score(y_test, y_pred, average="weighted", zero_division=0),
           recall=recall_score(y_test, y_pred, average="weighted", zero_division=0),
           f1=f1_score(y_test, y_pred, average="weighted", zero_division=0))
report = classification_report(y_test, y_pred, labels=labels, target_names=class_names, zero_division=0)
lines = ["=" * 60, f"{ALG_NAME} | test size={TEST_SIZE} | Kernel PCA {KERNEL}, nComp={N_COMP}", "=" * 60,
         f"Training samples: {len(y_train)}   Testing samples: {len(y_test)}", "", "CONFUSION MATRIX:", np.array2string(cm), ""]
for k in ("accuracy", "precision", "recall", "f1"): lines.append(f"{k.capitalize():10s}: {res[k]:.4f}")
lines += ["", "CLASSIFICATION REPORT:", report]
console_output = "\n".join(lines); print(console_output)

# 7. VISUAL OUTPUT: console output + charts in ONE image (real results only)
short = [c.replace("Web Attack - ", "Web ").replace("DoS ", "DoS-") for c in class_names]
fig = plt.figure(figsize=(19, 11), dpi=110)
gs = fig.add_gridspec(2, 2, width_ratios=[1.05, 1], height_ratios=[1, 1.7], hspace=0.28, wspace=0.12)
fig.suptitle(f"{ALG_NAME} - Test Size {TEST_SIZE} - Kernel PCA ({KERNEL}, nComp={N_COMP})", fontsize=15, fontweight="bold")
axt = fig.add_subplot(gs[:, 0]); axt.set_facecolor("#111827"); axt.set_xticks([]); axt.set_yticks([])
for sp in axt.spines.values(): sp.set_visible(False)
axt.text(0.02, 0.985, console_output, family="monospace", fontsize=9.6, color="#e5e7eb", va="top", ha="left", transform=axt.transAxes)
axt.set_title("Console output", loc="left", fontsize=11)
ax0 = fig.add_subplot(gs[0, 1]); ax1 = fig.add_subplot(gs[1, 1])
names = ["Accuracy", "Precision", "Recall", "F1 Score"]; vals = [res["accuracy"], res["precision"], res["recall"], res["f1"]]
bars = ax0.bar(names, vals, color=["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"])
ax0.set_ylim(0, 1.1); ax0.set_title(f"Weighted metrics  (train={res['n_train']}, test={res['n_test']})")
for b in bars: ax0.text(b.get_x() + b.get_width() / 2, b.get_height() + .02, f"{b.get_height():.4f}", ha="center", fontweight="bold")
im = ax1.imshow(cm, cmap="Blues"); fig.colorbar(im, ax=ax1, fraction=.046, pad=.04)
ax1.set_xticks(labels); ax1.set_yticks(labels); ax1.set_xticklabels(short, rotation=45, ha="right", fontsize=7); ax1.set_yticklabels(short, fontsize=7)
ax1.set_xlabel("Predicted"); ax1.set_ylabel("True"); ax1.set_title("Confusion Matrix")
for a in labels:
    for b_ in labels:
        if cm[a, b_]: ax1.text(b_, a, cm[a, b_], ha="center", va="center", fontsize=7, color="white" if cm[a, b_] > cm.max() / 2 else "black")
plt.savefig(os.path.join(HERE, tag + ".jpg"), format="jpg", bbox_inches="tight")
if os.environ.get("ACN_NO_SHOW") != "1": plt.show()   # IDEs display the image; run_all.py disables this
plt.close()

os.makedirs(os.path.join(ROOT, "results", "json"), exist_ok=True)
with open(os.path.join(ROOT, "results", "json", tag + ".json"), "w") as f: json.dump(res, f)
