"""Tables from the tuning, temporal and blocked-CV runs.  Writes CSV + LaTeX fragments (TEX_DIR).
  ACN_RUN=v2 python -m src.acn.analyze_extra"""
import json, numpy as np, pandas as pd
from .common import newest
from .config import *

SN = {"orig": "Original (78)", "pca-10": "PCA-10", "pca-30": "PCA-30", "kpca-linear-10": "KPCA-lin-10", "kpca-rbf-10": "KPCA-RBF-10", "kpca-cosine-10": "KPCA-cos-10",
      "kpca-cosine-30": "KPCA-cos-30", "kpca-rbf-30": "KPCA-RBF-30"}
def tex(df, name, colfmt):
    df.to_csv(f"{TABLE_DIR}/{name}.csv", index=False)
    open(TEX_DIR / f"{name}.tex", "w").write(df.to_latex(index=False, escape=False, column_format=colfmt, float_format=lambda x: f"{x:.3f}"))

# ---- tuning
t = pd.read_csv(newest("tuning_*.csv")); rows = []
for (c, s), g in t.groupby(["classifier", "space"]):
    rows.append(dict(Classifier=c, Space=SN[s], Default=g.default_f1_macro.mean(), Tuned=g.tuned_f1_macro.mean(), Tuned_sd=g.tuned_f1_macro.std(), folds_tuned_better=int((g.tuned_f1_macro > g.default_f1_macro).sum())))
T12 = pd.DataFrame(rows); T12.to_csv(f"{TABLE_DIR}/T12_tuning_full.csv", index=False)
piv = T12.pivot(index="Classifier", columns="Space", values="Tuned")
best = []
for c in ["KNN", "SVM", "RF"]:
    g = T12[T12.Classifier == c].set_index("Space"); red = g.drop("Original (78)")
    s_t = red.Tuned.idxmax(); s_d = red.Default.idxmax()   # best reduced space by tuned / by default score
    best.append(dict(Classifier=c, Orig_default=g.loc["Original (78)", "Default"], Orig_tuned=g.loc["Original (78)", "Tuned"],
                     Space_d=s_d, Reduced_default=red.Default.max(), Gap_default=g.loc["Original (78)", "Default"] - red.Default.max(),
                     Space_t=s_t, Reduced_tuned=red.Tuned.max(), Gap_tuned=g.loc["Original (78)", "Tuned"] - red.Tuned.max(),
                     Gap_default_at_tuned_space=g.loc["Original (78)", "Default"] - red.loc[s_t, "Default"]))
B = pd.DataFrame(best); B.to_csv(f"{TABLE_DIR}/T12_tuning_both.csv", index=False)
# Table: each block uses its own best reduced space (default-best for default, tuned-best for tuned); same-space default gap in a separate column
B2 = B.rename(columns={"Orig_default": "Orig.", "Space_d": "Best red. space", "Reduced_default": "Red.", "Gap_default": "$\\Delta$",
                       "Orig_tuned": "Orig. ", "Space_t": "Best red. space ", "Reduced_tuned": "Red. ", "Gap_tuned": "$\\Delta$ ", "Gap_default_at_tuned_space": "$\\Delta$ def. at tuned-best space"})
B2 = B2[["Classifier", "Orig.", "Best red. space", "Red.", "$\\Delta$", "Orig. ", "Best red. space ", "Red. ", "$\\Delta$ ", "$\\Delta$ def. at tuned-best space"]]
tex(B2, "T12_tuning", "lccrrccrrr")
_f = TEX_DIR / "T12_tuning.tex"; _t = _f.read_text().replace("\\toprule\n", "\\toprule\n & \\multicolumn{4}{c}{Default settings} & \\multicolumn{4}{c}{Tuned (nested search)} & \\\\\n\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}\n", 1); _f.write_text(_t)
# ---- temporal + blocked
def sp_table(df, split_names, name):
    out = []
    for sp in ["orig", "pca-10", "pca-30", "kpca-linear-10", "kpca-rbf-10", "kpca-cosine-10", "kpca-cosine-30"]:
        r = {"Space": SN[sp]}
        for lab, sn in split_names:
            for c in ["LR", "KNN", "SVM", "DT", "RF"]:
                r[f"{lab} {c}"] = df[(df.split == sn) & (df.space == sp) & (df.classifier == c)].f1_macro_present.mean()
        out.append(r)
    return pd.DataFrame(out)
d = pd.read_csv(f"{RAW_DIR}/temporal_results.csv")
T13 = sp_table(d, [("Chrono", "chronological_within_file_70_30"), ("Random", "random_stratified_70_30_same_classes")], "T13")
T13.to_csv(f"{TABLE_DIR}/T13_temporal_full.csv", index=False)
comp = []
for c in ["LR", "KNN", "SVM", "DT", "RF"]:
    for sp in ["orig", "pca-10", "kpca-cosine-30"]:
        comp.append(dict(Classifier=c, Space=SN[sp], Random=T13.set_index("Space").loc[SN[sp], f"Random {c}"], Head_tail=T13.set_index("Space").loc[SN[sp], f"Chrono {c}"]))
C = pd.DataFrame(comp); C["Penalty"] = C.Random - C.Head_tail; C = C.rename(columns={"Head_tail": "Head/tail"}); tex(C, "T13_temporal", "llrrr")
try:
    b = pd.read_csv(f"{RAW_DIR}/blocked_results.csv")
    B = sp_table(b, [("Blocked", "blocked_contiguous_5"), ("Random", "random_stratified_5fold_same_classes")], "T14"); B.to_csv(f"{TABLE_DIR}/T14_blocked_full.csv", index=False)
    comp = []
    for c in ["LR", "KNN", "SVM", "DT", "RF"]:
        for sp in ["orig", "pca-10", "kpca-cosine-30"]:
            comp.append(dict(Classifier=c, Space=SN[sp], Random=B.set_index("Space").loc[SN[sp], f"Random {c}"], Blocked=B.set_index("Space").loc[SN[sp], f"Blocked {c}"]))
    C2 = pd.DataFrame(comp); C2["Penalty"] = C2.Random - C2.Blocked; tex(C2, "T14_blocked", "llrrr")
except FileNotFoundError:
    print("blocked results not available yet")
print(pd.DataFrame(best).round(3).to_string()); print(C.round(3).to_string())
