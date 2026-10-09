"""Figures 1-9 (PDF vector + 300-dpi PNG) in results/figures. Bar charts start at zero (no truncated axes)."""
import glob, os, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np, pandas as pd
from .common import *
from .data import class_table, load_sample
from .evaluation import cm

plt.rcParams.update({"font.family": "serif", "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5, "legend.fontsize": 6.5,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150, "savefig.dpi": 300, "pdf.fonttype": 42})
S10 = ["orig", "pca-10", "kpca-linear-10", "kpca-rbf-10", "kpca-cosine-10"]
SN = {"orig": "Original", "pca-10": "PCA", "kpca-linear-10": "KPCA lin", "kpca-rbf-10": "KPCA RBF", "kpca-cosine-10": "KPCA cos"}
COL = ["#222222", "#0072B2", "#56B4E9", "#D55E00", "#009E73"]
HAT = ["", "//", "\\\\", "xx", ".."]


def save(fig, name):
    fig.savefig(f"{FIG_DIR}/{name}.pdf", bbox_inches="tight"); fig.savefig(f"{FIG_DIR}/{name}.png", bbox_inches="tight"); plt.close(fig)


def fig1():
    fig, ax = plt.subplots(figsize=(7.0, 1.55)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 22)
    boxes = ["CIC-IDS2017\nflows (stratified\nsample from\nraw CSVs)", "Stratified\n5-fold split\nx 3 repeats", "TRAIN fold:\nmean-impute +\nstandardise (fit)",
             "TRAIN fold:\nreducer fit\nOrig | PCA |\nKPCA (3 kernels)", "Classifier\nLR, kNN, SVM,\nDT, RF", "TEST fold:\ntransform\nonly + predict", "Metrics:\nAcc, macro-F1,\nbal.Acc, MCC,\nper-class, time"]
    w, g = 12.0, 2.15
    for i, t in enumerate(boxes):
        x = 0.5 + i * (w + g); ax.add_patch(FancyBboxPatch((x, 3), w, 15, boxstyle="round,pad=0.2", fc="#F2F2F2" if i not in (2, 3) else "#DCEBF7", ec="#333", lw=0.7))
        ax.text(x + w / 2, 10.5, t, ha="center", va="center", fontsize=5.5)
        if i < len(boxes) - 1: ax.annotate("", xy=(x + w + g - 0.2, 10.5), xytext=(x + w + 0.3, 10.5), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.text(50, 0.6, "Test folds never influence imputation, scaling, dimensionality reduction or model fitting.", ha="center", fontsize=6.8, style="italic")
    save(fig, "fig1_pipeline")


def fig2(y, classes):
    ct = class_table(y, classes); names = [c.replace("Web Attack - ", "Web ") for c, _, _ in ct]; n = [c[1] for c in ct]
    fig, ax = plt.subplots(figsize=(3.4, 2.5)); i = np.argsort(n); ax.barh(np.array(names)[i], np.array(n)[i], color="#555")
    ax.set_xscale("log"); ax.set_xlabel("Records in sample (log scale)")
    for k, v in enumerate(np.array(n)[i]): ax.text(v * 1.08, k, str(v), va="center", fontsize=6.3)
    ax.set_xlim(5, 3000); save(fig, "fig2_class_distribution")


def bars(a, metric, ylabel, name, wide=True):
    std = a[a.class_weight == "none"]; fig, ax = plt.subplots(figsize=(7.0, 2.3)); w = 0.16
    for j, sp in enumerate(S10):
        m = [std[(std.space == sp) & (std.classifier == c)][f"{metric}_mean"].iloc[0] for c in CLASSIFIERS]
        s = [std[(std.space == sp) & (std.classifier == c)][f"{metric}_std"].iloc[0] for c in CLASSIFIERS]
        ax.bar(np.arange(5) + (j - 2) * w, m, w, yerr=s, color=COL[j], hatch=HAT[j], edgecolor="white" if j in (0, 1, 3) else "k", lw=0.4, error_kw=dict(lw=0.6, capsize=1.2), label=SN[sp])
    dm = a[(a.classifier == "DUMMY")][f"{metric}_mean"].iloc[0]; ax.axhline(dm, color="r", ls="--", lw=0.8, label="Majority class")
    ax.set_xticks(range(5)); ax.set_xticklabels([CLF_NAMES[c] for c in CLASSIFIERS]); ax.set_ylim(0, 1.0); ax.set_ylabel(ylabel)
    ax.legend(ncol=6, loc="upper center", bbox_to_anchor=(0.5, 1.16), frameon=False); ax.grid(axis="y", lw=0.3); save(fig, name)


def fig5(a):
    std = a[a.class_weight == "none"]; M = np.array([[std[(std.space == sp) & (std.classifier == c)].f1_macro_mean.iloc[0] for sp in S10] for c in CLASSIFIERS])
    fig, ax = plt.subplots(figsize=(3.4, 2.1)); im = ax.imshow(M, cmap="viridis", vmin=0, vmax=0.8, aspect="auto")
    ax.set_xticks(range(5)); ax.set_xticklabels([SN[s] for s in S10], rotation=30, ha="right"); ax.set_yticks(range(5)); ax.set_yticklabels(CLASSIFIERS)
    for i in range(5):
        for j in range(5): ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=6.5, color="w" if M[i, j] < 0.45 else "k")
    fig.colorbar(im, ax=ax, label="Macro-F1", fraction=0.046); ax.spines[:].set_visible(False); save(fig, "fig5_classifier_vs_reduction")


def fig6(a):
    std = a[a.class_weight == "none"]; fig, axs = plt.subplots(1, 5, figsize=(7.0, 1.9), sharey=True)
    for ax, c in zip(axs, CLASSIFIERS):
        for k, col, ls in [("pca", "#0072B2", "-"), ("linear", "#56B4E9", ":"), ("rbf", "#D55E00", "-"), ("cosine", "#009E73", "-")]:
            sp = [f"pca-{n}" if k == "pca" else f"kpca-{k}-{n}" for n in COMPONENTS]
            ax.plot(COMPONENTS, [std[(std.space == s) & (std.classifier == c)].f1_macro_mean.iloc[0] for s in sp], marker="o", ms=2.5, lw=1, color=col, ls=ls, label="PCA" if k == "pca" else f"KPCA {k}")
        ax.axhline(std[(std.space == "orig") & (std.classifier == c)].f1_macro_mean.iloc[0], color="k", ls="--", lw=0.8, label="Original (78)")
        ax.set_title(c); ax.set_xlabel("Components"); ax.set_ylim(0, 0.85); ax.set_xticks(COMPONENTS); ax.grid(lw=0.3)
    axs[0].set_ylabel("Macro-F1"); axs[2].legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.32), frameon=False); save(fig, "fig6_components_vs_f1")


def fig7(a):
    rt = pd.read_csv(newest("runtime_*.csv")); std = a[a.class_weight == "none"]
    fig, ax = plt.subplots(figsize=(3.4, 2.5)); mk = {"LR": "o", "KNN": "s", "SVM": "^", "DT": "D", "RF": "P"}
    for _, r in rt.iterrows():
        f = std[(std.space == r.space) & (std.classifier == r.classifier)].f1_macro_mean.iloc[0]; j = S10.index(r.space)
        ax.scatter(r.train_time_s, f, c=COL[j], marker=mk[r.classifier], s=22, edgecolor="k", lw=0.3)
    ax.set_xscale("log"); ax.set_xlabel("Training time per fold (s, log)"); ax.set_ylabel("Macro-F1 (CV mean)"); ax.set_ylim(0, 1.0); ax.grid(lw=0.3); ax.tick_params(axis="x", labelsize=6)
    h1 = [plt.Line2D([], [], marker="o", ls="", color=COL[i], label=SN[s]) for i, s in enumerate(S10)]
    h2 = [plt.Line2D([], [], marker=m, ls="", color="gray", mec="k", label=c) for c, m in mk.items()]
    ax.legend(handles=h1 + h2, ncol=5, fontsize=5.6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), columnspacing=0.8, handletextpad=0.2); save(fig, "fig7_perf_vs_cost")


def fig8(classes):
    yt, yp = np.load(f"{RAW_DIR}/best_oof_true.npy"), np.load(f"{RAW_DIR}/best_oof_pred.npy"); C = cm(yt, yp, len(classes))
    sel = json.load(open(f"{TABLE_DIR}/selected_model.json")); short = [c.replace("Web Attack - ", "Web ").replace("DoS ", "DoS-") for c in classes]
    fig, ax = plt.subplots(figsize=(3.5, 3.2)); ax.imshow(C, cmap="Blues", norm=matplotlib.colors.PowerNorm(0.4))
    ax.set_xticks(range(len(C))); ax.set_yticks(range(len(C))); ax.set_xticklabels(short, rotation=60, ha="right", fontsize=5.8); ax.set_yticklabels(short, fontsize=5.8)
    for i in range(len(C)):
        for j in range(len(C)):
            if C[i, j]: ax.text(j, i, C[i, j], ha="center", va="center", fontsize=(4.2 if C[i, j] >= 1000 else 5.5), color="w" if C[i, j] > C.max() * 0.4 else "k")
    ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title(f"{sel['classifier']} on {sel['space']} (pooled out-of-fold, first repeat)", fontsize=6.5); save(fig, "fig8_confusion_best")


def fig9(n_total=1000):
    df = pd.read_csv(newest("size_results_*.csv")); df["space"] = np.where(df.dimensionality_method == "orig", "orig", np.where(df.dimensionality_method == "pca", "pca-10", "kpca-" + df.kernel + "-10"))
    fig, axs = plt.subplots(1, 5, figsize=(7.0, 1.9), sharey=True)
    for ax, c in zip(axs, CLASSIFIERS):
        for j, sp in enumerate(S10):
            g = df[(df.classifier == c) & (df.space == sp)].groupby("test_size").f1_macro.agg(["mean", "std"])
            ax.errorbar(n_total * (1 - g.index.values), g["mean"], yerr=g["std"], color=COL[j], marker="o", ms=2.5, lw=1, capsize=1.5, elinewidth=0.5, label=SN[sp])
        ax.set_title(c); ax.set_xlabel("Training records"); ax.set_xticks([int(n_total * (1 - t)) for t in sorted(df.test_size.unique(), reverse=True)]); ax.set_ylim(0, 1.0); ax.grid(lw=0.3); ax.tick_params(axis="x", labelsize=6)
    axs[0].set_ylabel("Macro-F1"); axs[2].legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.32), frameon=False); save(fig, "fig9_training_size")


def main():
    os.makedirs(FIG_DIR, exist_ok=True); X, y, classes, _ = load_sample(); df = load_cv(); a = agg(df, ["space", "classifier", "class_weight"])
    fig1(); fig2(y, classes); bars(a, "accuracy", "Accuracy", "fig3_accuracy"); bars(a, "f1_macro", "Macro-F1", "fig4_macro_f1")
    fig5(a); fig6(a); fig7(a); fig8(classes); fig9(len(y)); print(sorted(os.listdir(FIG_DIR)))


if __name__ == "__main__":
    main()
