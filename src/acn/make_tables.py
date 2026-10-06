"""Generate Tables I-X as CSV (results/tables) and LaTeX fragments (papers/ieee/tables)."""
import json, os
import numpy as np, pandas as pd
from .common import *
from .data import class_table, load_sample
from .evaluation import per_class

TEX = ROOT / "papers" / "ieee" / "tables"; os.makedirs(TEX, exist_ok=True)
S10 = ["orig", "pca-10", "kpca-linear-10", "kpca-rbf-10", "kpca-cosine-10"]
SN = {"orig": "Original (78)", "pca-10": "PCA-10", "kpca-linear-10": "KPCA-lin-10", "kpca-rbf-10": "KPCA-RBF-10", "kpca-cosine-10": "KPCA-cos-10"}


def save(df, name, tex_cols=None, fmt=None, colfmt=None, caption=""):
    df.to_csv(f"{TABLE_DIR}/{name}.csv", index=False)
    open(TEX / f"{name}.tex", "w").write(df.to_latex(index=False, escape=False, column_format=colfmt, float_format=lambda x: f"{x:.3f}"))


def main():
    X, y, classes, _ = load_sample(); df = load_cv(); a = agg(df, ["space", "classifier", "class_weight"])
    # Table I / II
    ct = class_table(y, classes)
    save(pd.DataFrame([("Source files (as stated in repo README)", "Tue + Wed + Thu-morning CSVs"), ("Source flows (README; not recomputed here)", "1,308,978"),
                       ("Records used in all experiments", len(y)), ("Features", X.shape[1]), ("Constant (zero-variance) features", int((X.std(0) == 0).sum())),
                       ("Classes", len(classes)), ("Majority-class share", f"{100*max(c[1] for c in ct)/len(y):.1f}\\%"),
                       ("Smallest class (records)", min(c[1] for c in ct))], columns=["Property", "Value"]), "T1_dataset", colfmt="lr")
    save(pd.DataFrame([(c.replace("Web Attack - ", "Web "), n, f"{p:.1f}") for c, n, p in ct], columns=["Class", "Records", "\\%"]), "T2_class_distribution", colfmt="lrr")
    save(pd.DataFrame([("Validation", "Repeated stratified 5-fold CV, 3 repeats (15 folds), seed 42"), ("Preprocessing", "Mean imputation + standardisation, fitted on training folds only"),
                       ("Feature spaces", "Original; PCA; Kernel PCA (linear, RBF, cosine)"), ("Components", "5, 10, 15, 20, 30"),
                       ("Classifiers", "LR, 5-NN, SVM (RBF, C=1), DT (entropy), RF (100 trees); fixed hyper-parameters"),
                       ("Class handling", "Standard vs class\\_weight=balanced (not for k-NN)"), ("Primary metric", "Macro-F1 (mean over folds)"),
                       ("Baseline", "Majority-class classifier")], columns=["Factor", "Setting"]), "T3_config", colfmt="lp{5.2cm}")
    # Table IV: original baseline
    rows = []
    for c in CLASSIFIERS + ["DUMMY"]:
        for w in ["none", "balanced"]:
            r = a[(a.space == "orig") & (a.classifier == c) & (a.class_weight == w)]
            if len(r):
                r = r.iloc[0]; rows.append([CLF_NAMES[c], w, pm(r.accuracy_mean, r.accuracy_std), pm(r.f1_macro_mean, r.f1_macro_std),
                                            pm(r.f1_weighted_mean, r.f1_weighted_std), pm(r.balanced_accuracy_mean, r.balanced_accuracy_std), pm(r.mcc_mean, r.mcc_std)])
    save(pd.DataFrame(rows, columns=["Classifier", "Weights", "Acc.", "Macro-F1", "Wtd-F1", "Bal.Acc.", "MCC"]), "T4_original_baseline", colfmt="llccccc")
    # Table V / VI: macro-F1 by components (standard weights)
    std = a[a.class_weight == "none"]
    def grid(rowspaces, labels, name):
        out = []
        for sp, lb in zip(rowspaces, labels):
            row = [lb]
            for c in CLASSIFIERS:
                r = std[(std.space == sp) & (std.classifier == c)].iloc[0]; row.append(pm(r.f1_macro_mean, r.f1_macro_std, 2))
            out.append(row)
        save(pd.DataFrame(out, columns=["Space"] + CLASSIFIERS), name, colfmt="l" + "c" * 5)
    grid([f"pca-{n}" for n in COMPONENTS], [f"PCA-{n}" for n in COMPONENTS], "T5_pca")
    grid([f"kpca-{k}-{n}" for k in KERNELS for n in COMPONENTS], [f"{k}-{n}" for k in KERNELS for n in COMPONENTS], "T6_kpca")
    # Table VII: matched n=10 CV mean +- std (accuracy | macro-F1)
    out = []
    for sp in S10:
        row = [SN[sp]]
        for c in CLASSIFIERS:
            r = std[(std.space == sp) & (std.classifier == c)].iloc[0]; row.append(f"{r.accuracy_mean:.3f} / {r.f1_macro_mean:.3f}$\\pm${r.f1_macro_std:.3f}")
        out.append(row)
    save(pd.DataFrame(out, columns=["Space"] + CLASSIFIERS), "T7_cv_summary_n10", colfmt="lccccc")
    # Table VIII: per-class, selected model, pooled out-of-fold predictions of repeat 0
    (sp, c, w), f1 = best_config(df); oof = json.load(open(newest("oof_repeat0_2*.json")))[f"{sp}|{c}|{'cw' if w == 'balanced' else 'std'}"]
    idx = np.array(oof["idx"]); pred = np.array(oof["pred"]); order = np.argsort(idx)
    assert len(set(idx)) == len(y)
    pc = pd.DataFrame(per_class(y[idx], pred, [k.replace("Web Attack - ", "Web ") for k in classes]))
    pc.columns = ["Class", "Precision", "Recall", "F1", "Support"]; save(pc, "T8_per_class_best", colfmt="lrrrr")
    np.save(f"{RAW_DIR}/best_oof_true.npy", y[idx]); np.save(f"{RAW_DIR}/best_oof_pred.npy", pred)
    json.dump(dict(space=sp, classifier=c, class_weight=w, f1_macro_mean=f1), open(f"{TABLE_DIR}/selected_model.json", "w"))
    # Table IX runtime
    rt = pd.read_csv(newest("runtime_*.csv"))
    t9 = rt.assign(Space=rt.space.map(SN), Classifier=rt.classifier.map(CLF_NAMES))[["Space", "Classifier", "train_time_s", "inference_time_s", "peak_mem_mb"]]
    t9.columns = ["Space", "Classifier", "Train (s)", "Inference (s)", "Peak mem (MB)"]; save(t9, "T9_runtime", colfmt="llrrr")
    sc = pd.read_csv(newest("kpca_scaling_*.csv")); save(sc, "T9b_kpca_scaling")
    # Table X statistics (Holm-adjusted)
    w = pd.read_csv(f"{TABLE_DIR}/stat_wilcoxon.csv")
    t10 = w[["classifier", "method_a", "method_b", "mean_diff", "p_holm", "effect_r"]].copy()
    t10.columns = ["Clf", "A", "B", "$\\Delta$F1 (A-B)", "$p_{Holm}$", "$r$"]; save(t10, "T10_stats", colfmt="lllrrr")
    w2 = pd.read_csv(f"{TABLE_DIR}/stat_best_reduced.csv")
    t10b = w2[["classifier", "method_b", "mean_f1_a", "mean_f1_b", "mean_diff", "p_holm", "effect_r"]].copy()
    t10b.columns = ["Clf", "Best reduced space", "F1 orig", "F1 reduced", "$\\Delta$F1 (orig-red.)", "$p_{Holm}$", "$r$"]; save(t10b, "T10b_stats_best_reduced", colfmt="llrrrrr")
    print("selected:", sp, c, w if isinstance(w, str) else "", round(f1, 4)); print(pc.round(3).to_string())


if __name__ == "__main__":
    main()
