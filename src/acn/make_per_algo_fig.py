"""fig12: one accuracy bar graph per classifier. Bars = PCA / KPCA-linear / KPCA-RBF / KPCA-cosine at 5..30 components (test cases);
dashed line = original 78 features. Mean accuracy over 15 folds, standard class weights. Built from results/v2 only."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .common import *
from .make_figures import agg, load_cv, save, COL, HAT

NAMES = {"LR": "Logistic regression", "KNN": "k-NN", "SVM": "SVM (RBF)", "DT": "Decision tree", "RF": "Random forest"}
METH = [("pca", "PCA"), ("kpca-linear", "KPCA lin"), ("kpca-rbf", "KPCA RBF"), ("kpca-cosine", "KPCA cos")]
NS = [5, 10, 15, 20, 30]

def main():
    a = agg(load_cv(), ["space", "classifier", "class_weight"]); a = a[a.class_weight == "none"]
    fig, axs = plt.subplots(2, 3, figsize=(6.4, 4.0), sharey=True); axs = axs.ravel(); w = 0.2
    for k, c in enumerate(NAMES):
        ax = axs[k]; d = a[a.classifier == c].set_index("space")
        for i, (m, lab) in enumerate(METH):
            ax.bar(np.arange(5) + (i - 1.5) * w, [d.loc[f"{m}-{n}", "accuracy_mean"] for n in NS], w, yerr=[d.loc[f"{m}-{n}", "accuracy_std"] for n in NS],
                   color=COL[i + 1], edgecolor="white", label=lab, capsize=0.8, error_kw=dict(lw=.4))
        o = d.loc["orig", "accuracy_mean"]; ax.axhline(o, color="black", ls="--", lw=.9, label="Original (78)")
        ax.set_title(f"{NAMES[c]} (orig. {o:.3f})", fontsize=7); ax.set_xticks(range(5)); ax.set_xticklabels(NS, fontsize=6); ax.set_ylim(0.5, 1.0); ax.grid(axis="y", lw=.3)
        if k % 3 == 0: ax.set_ylabel("Accuracy", fontsize=7)
        if k >= 2: ax.set_xlabel("Components", fontsize=6)
    h, l = axs[0].get_legend_handles_labels(); axs[5].axis("off"); axs[5].legend(h, l, loc="center", fontsize=7, frameon=False)
    fig.tight_layout(); save(fig, "fig12_per_algorithm_accuracy")
    print(a[a.space != "orig"].accuracy_mean.min())

if __name__ == "__main__": main()
