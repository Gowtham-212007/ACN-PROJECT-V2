"""Figures for the faculty-format manuscript (cicps_faculty_format).
fig10: all 25 classifier x feature-space executions, enlarged to ~half a page.
fig11: this work vs the five best IEEE Xplore papers of the literature survey (accuracy as stated in each abstract; NOT like-for-like)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from .common import *
from .make_figures import agg, load_cv, S10, SN, save, COL, HAT
CLF = ["LR", "KNN", "SVM", "DT", "RF"]

def fig10(a):
    a = a[a.class_weight == "none"]
    fig, ax = plt.subplots(figsize=(6.2, 4.4)); w = 0.16
    for i, s in enumerate(S10):
        v = [a[(a.space == s) & (a.classifier == c)].f1_macro_mean.iloc[0] for c in CLF]
        e = [a[(a.space == s) & (a.classifier == c)].f1_macro_std.iloc[0] for c in CLF]
        ax.bar(np.arange(5) + (i - 2) * w, v, w, yerr=e, color=COL[i], hatch=HAT[i], edgecolor="white", label=SN[s], capsize=1.5, error_kw=dict(lw=.7))
    ax.set_xticks(range(5)); ax.set_xticklabels(["Logistic regr.", "k-NN", "SVM (RBF)", "Decision tree", "Random forest"], fontsize=9)
    ax.set_ylim(0, 1.05); ax.set_ylabel("Macro-F1 (mean $\\pm$ std, 15 folds)", fontsize=9)
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.12), frameon=False, fontsize=8); ax.grid(axis="y", lw=.3); save(fig, "fig10_all_executions")

def fig11(acc_ours):
    rows = [("Pramana et al. [1]\n(Ridge-XGBoost)", 99.996, "99.996"), ("Qin [2]\n(RF + fuzzy rules, multi-class)", 99.89, "99.89"),
            ("Patil & Joshi [3]\n(PMSpDN)", 99.21, "99.21"), ("Ahuja & Doohan [4]\n(XGBoost)", 97.73, "97.73"),
            ("Amin & Jadhav [5]\n(SMOTE + RF)", 97.6, "97.6"), ("This work\n(RF, original features)", acc_ours * 100, f"{acc_ours*100:.2f}")]
    fig, ax = plt.subplots(figsize=(6.4, 3.0)); y = np.arange(len(rows))[::-1]
    ax.barh(y, [r[1] for r in rows], color=["#777777"] * 5 + ["#009E73"], height=.6)
    for yy, r in zip(y, rows): ax.text(r[1] + .04, yy, r[2], va="center", fontsize=8)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8); ax.set_xlim(95, 100.6); ax.tick_params(axis="x", labelsize=8)
    ax.set_xlabel("Accuracy (%) as stated in each source; axis starts at 95 %; not like-for-like", fontsize=8); ax.grid(axis="x", lw=.3); save(fig, "fig11_accuracy_comparison")

if __name__ == "__main__":
    df = load_cv(); a = agg(df, ["space", "classifier", "class_weight"]); fig10(a)
    r = a[(a.space == "orig") & (a.classifier == "RF") & (a.class_weight == "none")]; fig11(float(r.accuracy_mean.iloc[0]))
