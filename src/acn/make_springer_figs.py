"""Two extra figures for the Springer manuscript, built from results/v2 outputs only.
 fig10_all_executions: macro-F1 of every classifier x feature-space execution at 10 components (one chart).
 fig11_accuracy_comparison: reported accuracy of recent papers vs this work (NOT directly comparable: different datasets/splits)."""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .common import *
from .make_figures import agg, load_cv, S10, SN, save, COL, HAT  # also applies the shared rcParams

CLF = ["LR", "KNN", "SVM", "DT", "RF"]


def fig10(a):
    a = a[a.class_weight == "none"] if "class_weight" in a and "none" in set(a.class_weight) else a
    fig, ax = plt.subplots(figsize=(6.2, 2.6)); w = 0.16
    for i, s in enumerate(S10):
        v = [a[(a.space == s) & (a.classifier == c)].f1_macro_mean.iloc[0] for c in CLF]
        e = [a[(a.space == s) & (a.classifier == c)].f1_macro_std.iloc[0] for c in CLF]
        ax.bar(np.arange(5) + (i - 2) * w, v, w, yerr=e, color=COL[i], hatch=HAT[i], edgecolor="white", label=SN[s], capsize=1.2, error_kw=dict(lw=.6))
    ax.set_xticks(range(5)); ax.set_xticklabels(["Logistic regr.", "k-NN", "SVM (RBF)", "Decision tree", "Random forest"]); ax.set_ylim(0, 1); ax.set_ylabel("Macro-F1 (mean $\\pm$ std, 15 folds)")
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.16), frameon=False); ax.grid(axis="y", lw=.3); save(fig, "fig10_all_executions")


def fig11(acc_ours):
    # reported accuracy (%), as stated by each source; datasets differ, see Table in the paper
    rows = [("Waghmode et al. 2025\n(LS-SVM, CIC-IDS2017)", 99.5), ("Patil et al. 2025\n(Extra Trees+IG, CIC-IDS2017)", 99.98),
            ("Xu & Liu 2025\n(MLP, CICIDS2017)", 97.75), ("Emirmahmutoglu & Atay 2025\n(FPA+RF, CSE-CIC-IDS2018)", 99.9965), ("This work\n(RF, 6,000-record sample)", acc_ours * 100)]
    fig, ax = plt.subplots(figsize=(6.4, 2.6)); y = np.arange(len(rows))[::-1]
    ax.barh(y, [r[1] for r in rows], color=["#777777"] * 4 + ["#009E73"], height=.6)
    for yy, r in zip(y, rows): ax.text(r[1] + .06, yy, (f"{r[1]:.4f}" if r[1] > 99.9 else f"{r[1]:.2f}"), va="center", fontsize=8)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8); ax.set_xlim(95, 100.5); ax.tick_params(axis="x", labelsize=8); ax.set_xlabel("Reported accuracy (%); axis starts at 95 %; not directly comparable", fontsize=8); ax.grid(axis="x", lw=.3)
    save(fig, "fig11_accuracy_comparison")


if __name__ == "__main__":
    df = load_cv(); a = agg(df, ["space", "classifier", "class_weight"]); print(a.columns.tolist()); print(a.class_weight.unique())
    fig10(a); r = a[(a.space == "orig") & (a.classifier == "RF")]; print(r[["class_weight", "accuracy_mean", "f1_macro_mean"]]); fig11(float(r.accuracy_mean.iloc[0]) if len(r) == 1 else float(r[r.class_weight == "none"].accuracy_mean.iloc[0]))
