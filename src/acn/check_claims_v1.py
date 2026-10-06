"""Recompute every numeric claim made in the paper's abstract/results/discussion/conclusion from the RAW result files.
Each row: claim, value recomputed from raw data, value stated in the paper, tolerance, pass/fail.  Output: results/tables/claim_check.csv
  python -m src.acn.check_claims
"""
import glob, numpy as np, pandas as pd
from .common import *

rows = []
def chk(name, got, stated, tol):
    ok = abs(got - stated) <= tol
    rows.append(dict(claim=name, recomputed=round(float(got), 4), stated=stated, tol=tol, ok=bool(ok)))

df = load_cv()
def cell(space, c, cw="none", col="f1_macro"):
    return df[(df.space == space) & (df.classifier == c) & (df.class_weight == cw)][col]
# --- abstract / headline
for col, st, tol in [("accuracy", .952, .0006), ("f1_macro", .722, .0006), ("mcc", .894, .0006), ("f1_weighted", .947, .0006), ("balanced_accuracy", .717, .0006)]:
    chk(f"RF orig {col} mean", cell("orig", "RF", col=col).mean(), st, tol)
chk("RF orig accuracy sd", cell("orig", "RF", col="accuracy").std(), .010, .0006)
chk("RF orig macro-F1 sd", cell("orig", "RF").std(), .058, .0006)
chk("RF orig MCC sd", cell("orig", "RF", col="mcc").std(), .022, .0006)
du = df[df.classifier == "DUMMY"]
chk("majority accuracy", du.accuracy.mean(), .718, .0006); chk("majority macro-F1", du.f1_macro.mean(), .076, .0006); chk("majority MCC", du.mcc.mean(), 0.0, 1e-9)
g = df[df.classifier != "DUMMY"].groupby(["space", "classifier", "class_weight"]).f1_macro.mean().sort_values(ascending=False)
chk("best config is orig|RF|none (1=yes)", float(g.index[0] == ("orig", "RF", "none")), 1, 0)
chk("SVM orig macro-F1", cell("orig", "SVM").mean(), .388, .0006)
chk("SVM cosine-30 macro-F1", cell("kpca-cosine-30", "SVM").mean(), .510, .0006)
chk("SVM orig+balanced macro-F1", cell("orig", "SVM", "balanced").mean(), .546, .0006)
# --- Table 3 extremes / macro-F1 band for best models
chk("fold SD of macro-F1 min over 5 clfs (orig)", min(cell("orig", c).std() for c in CLASSIFIERS), .037, .0006)
chk("fold SD of macro-F1 max over 5 clfs (orig)", max(cell("orig", c).std() for c in CLASSIFIERS), .074, .0006)
# --- linear KPCA vs PCA
def lin_pca_max(cws):
    return max(abs(cell(f"pca-{n}", c, cw).mean() - cell(f"kpca-linear-{n}", c, cw).mean())
               for c in CLASSIFIERS for cw in cws for n in COMPONENTS if len(cell(f"pca-{n}", c, cw)) and len(cell(f"kpca-linear-{n}", c, cw)))
chk("max |PCA - linear KPCA| macro-F1, standard weights, all n", lin_pca_max(["none"]), .0103, .00006)
chk("max |PCA - linear KPCA| macro-F1, all weights, all n", lin_pca_max(["none", "balanced"]), .0142, .00006)
for c in ["LR", "KNN", "SVM"]:
    chk(f"max |PCA - linear KPCA| for {c} (paper: <=0.001)", max(abs(cell(f"pca-{n}", c, cw).mean() - cell(f"kpca-linear-{n}", c, cw).mean()) for cw in ["none", "balanced"] for n in COMPONENTS if len(cell(f"pca-{n}", c, cw))), .0005, .0005)
# --- kernel vs component-count spread (standard weights; spread of marginal means over reduced spaces)
for c, kern_gt in [("LR", False), ("KNN", True), ("SVM", False), ("DT", True), ("RF", True)]:
    t = df[(df.classifier == c) & (df.class_weight == "none") & (df.dimensionality_method != "orig")].groupby(["kernel", "components"]).f1_macro.mean().unstack()
    kr, cr = t.mean(axis=1).max() - t.mean(axis=1).min(), t.mean(axis=0).max() - t.mean(axis=0).min()
    chk(f"{c}: kernel spread > component spread (1=yes; paper: KNN,DT,RF yes; LR,SVM no)", float(kr > cr), float(kern_gt), 0)
# --- LR vs components
chk("LR PCA-5 macro-F1", cell("pca-5", "LR").mean(), .28, .005); chk("LR PCA-30 macro-F1", cell("pca-30", "LR").mean(), .57, .005)
chk("LR orig macro-F1", cell("orig", "LR").mean(), .61, .005)
# --- class weighting
for c, a, b, col in [("LR", .638, .778, "balanced_accuracy"), ("SVM", .358, .720, "balanced_accuracy"), ("LR", .612, .630, "f1_macro"),
                     ("SVM", .388, .546, "f1_macro"), ("DT", .713, .702, "f1_macro"), ("RF", .722, .687, "f1_macro")]:
    chk(f"{c} orig {col} none", cell("orig", c, "none", col).mean(), a, .0006); chk(f"{c} orig {col} balanced", cell("orig", c, "balanced", col).mean(), b, .0006)
# --- Wilcoxon
w = pd.read_csv(str(TABLE_DIR) + "/stat_wilcoxon.csv")
chk("number of Wilcoxon comparisons", len(w), 30, 0); chk("significant after Holm", w["significant_0.05"].sum(), 17, 0)
sig_o = w[(w.method_a == "orig") & w["significant_0.05"]]
chk("sig. comparisons with orig where orig is better (all of them?)", float((sig_o.mean_diff > 0).all()), 1, 0)
rb = w[(w.method_b == "kpca-rbf-10") & (w.method_a == "pca-10")].set_index("classifier")
chk("RBF sig. worse than PCA: LR,SVM,DT,RF all sig (count)", float(sum(rb.loc[c, "significant_0.05"] and rb.loc[c, "mean_diff"] > 0 for c in ["LR", "SVM", "DT", "RF"])), 4, 0)
cs = w[(w.method_b == "kpca-cosine-10") & (w.method_a == "pca-10")].set_index("classifier")
chk("cosine vs PCA significant classifiers (count; paper: LR only)", float(cs["significant_0.05"].sum()), 1, 0)
chk("cosine vs PCA significant for LR with PCA better", float(cs.loc["LR", "significant_0.05"] and cs.loc["LR", "mean_diff"] > 0), 1, 0)
# --- best reduced
b = pd.read_csv(str(TABLE_DIR) + "/stat_best_reduced.csv").set_index("classifier")
for c in ["LR", "DT", "RF"]: chk(f"best-reduced {c}: orig better, p_holm<0.01", float(b.loc[c, "mean_diff"] > 0 and b.loc[c, "p_holm"] < .01), 1, 0)
chk("best-reduced KNN not significant", float(not b.loc["KNN", "significant_0.05"]), 1, 0)
chk("best-reduced SVM p_holm", b.loc["SVM", "p_holm"], .0003, .00005); chk("best-reduced SVM effect r (-1 = reduced better in all 15 folds)", b.loc["SVM", "effect_r"], -1, 0)
# --- per-class
pcl = pd.read_csv(str(TABLE_DIR) + "/T8_per_class_best.csv").set_index("Class")
chk("web-attack F1 min", pcl.loc[["Web Brute Force", "Web Sql Injection", "Web XSS"], "F1"].min(), .21, .005)
chk("web-attack F1 max", pcl.loc[["Web Brute Force", "Web Sql Injection", "Web XSS"], "F1"].max(), .50, .005)
chk("web-attack support max", pcl.loc[["Web Brute Force", "Web Sql Injection", "Web XSS"], "Support"].max(), 11, 0)
chk("slow-DoS recall min", pcl.loc[["DoS Slowhttptest", "DoS slowloris"], "Recall"].min(), .57, .005); chk("slow-DoS recall max", pcl.loc[["DoS Slowhttptest", "DoS slowloris"], "Recall"].max(), .71, .005)
chk("F1>=0.96 for BENIGN,Hulk,FTP,SSH,Heartbleed (min)", pcl.loc[["BENIGN", "DoS Hulk", "FTP-Patator", "SSH-Patator", "Heartbleed"], "F1"].min(), .96, .005)
chk("benign share", pcl.loc["BENIGN", "Support"] / pcl.Support.sum(), .718, .0006)
att = pcl.drop("BENIGN").Support; chk("attack classes with 10-17 records (count; paper: nine of ten)", float(((att >= 10) & (att <= 17)).sum()), 9, 0)
chk("attack classes with <=17 records, excl. Hulk (count; paper: nine of ten)", float((att <= 17).sum()), 9, 0)
# --- cost
rt = pd.read_csv(newest("runtime_2*.csv")); RF_ = rt.groupby("space").reducer_fit_s.mean()  # reducer fit: mean over the 5 classifier rows (as in Table 5)
rt = rt.set_index(["space", "classifier"])
chk("PCA reducer fit s", RF_["pca-10"], .01, .003)
ks = ["kpca-linear-10", "kpca-rbf-10", "kpca-cosine-10"]
chk("KPCA reducer fit min", min(RF_[k] for k in ks), .09, .005); chk("KPCA reducer fit max", max(RF_[k] for k in ks), .12, .005)
chk("KPCA/PCA fit-time ratio (paper: roughly tenfold)", np.mean([RF_[k] for k in ks]) / RF_["pca-10"], 10, 3)
chk("RF train KPCA min", min(rt.loc[(k, "RF"), "train_time_s"] for k in ks), .36, .005); chk("RF train KPCA max", max(rt.loc[(k, "RF"), "train_time_s"] for k in ks), .38, .006)
chk("RF train PCA", rt.loc[("pca-10", "RF"), "train_time_s"], .21, .006)
chk("DT train PCA", rt.loc[("pca-10", "DT"), "train_time_s"], .016, .0006)
chk("DT train KPCA min", min(rt.loc[(k, "DT"), "train_time_s"] for k in ks), .09, .006); chk("DT train KPCA max", max(rt.loc[(k, "DT"), "train_time_s"] for k in ks), .10, .0006)
chk("RF infer PCA", rt.loc[("pca-10", "RF"), "inference_time_s"], .007, .0006)
chk("RF infer KPCA min", min(rt.loc[(k, "RF"), "inference_time_s"] for k in ks), .014, .0006); chk("RF infer KPCA max", max(rt.loc[(k, "RF"), "inference_time_s"] for k in ks), .016, .0006)
chk("peak mem KPCA MB", rt.loc[("kpca-rbf-10", "RF"), "peak_mem_mb"], 11.7, .1); chk("peak mem orig MB", rt.loc[("orig", "RF"), "peak_mem_mb"], 1.7, .1)
chk("memory ratio (paper: sevenfold)", rt.loc[("kpca-rbf-10", "RF"), "peak_mem_mb"] / rt.loc[("orig", "RF"), "peak_mem_mb"], 7, .3)
sc = pd.read_csv(newest("kpca_scaling_2*.csv")); sc = sc[sc.method == "kpca-rbf-10"].set_index("n")
for n, st in [(400, 3.1), (600, 6.4), (800, 11.0), (1000, 16.8)]: chk(f"KPCA scaling memory n={n}", sc.loc[n, "peak_mem_mb"], st, .06)
chk("log-log memory slope 400->1000 (paper: ~quadratic, 2)", np.log(sc.loc[1000, "peak_mem_mb"] / sc.loc[400, "peak_mem_mb"]) / np.log(2.5), 2.0, .25)
chk("THEORETICAL dense float64 kernel matrix, 1,308,978 flows, TB (decimal)", 1308978 ** 2 * 8 / 1e12, 14, 0.5)
# --- training-size sensitivity: orig best at every size for LR,SVM,DT,RF
z = pd.read_csv(newest("size_results_2*.csv")); z = z[z.class_weight == "none"] if "class_weight" in z else z
z["space"] = np.where(z.dimensionality_method == "orig", "orig", z.dimensionality_method + np.where(z.kernel.notna(), "-" + z.kernel.fillna(""), ""))
m = z[z.classifier != "DUMMY"].groupby(["classifier", "n_train", "space"]).f1_macro.mean()
ok = all(m.loc[(c, n)].idxmax() == "orig" for c in ["LR", "SVM", "DT", "RF"] for n in [400, 600, 800])
chk("orig highest mean macro-F1 at every size for LR,SVM,DT,RF", float(ok), 1, 0)

# --- nested CV (requires nested_summary.csv from analyze_nested)
ns = pd.read_csv(str(TABLE_DIR) + "/nested_summary.csv").set_index("procedure"); A = ns.iloc[0]
chk("nested overall macro-F1", A.nested_macroF1, .715, .0006); chk("nested overall sd", A.sd, .044, .0006); chk("nested overall accuracy", A.nested_acc, .945, .0006); chk("nested overall MCC", A.nested_mcc, .880, .0006)
chk("selection optimism (same-CV max - nested)", df[df.classifier != "DUMMY"].groupby("experiment_id").f1_macro.mean().max() - A.nested_macroF1, .008, .0006)
chk("nested: original-feature config chosen in all 15 outer folds", A.frac_selected_orig, 1.0, 0)
chk("accuracy - macro-F1 gap (RF orig)", cell("orig", "RF", col="accuracy").mean() - cell("orig", "RF").mean(), .23, .0006)
for c, dv, cv, p_ in [("LR", .619, .601, .055), ("KNN", .620, .609, .279), ("SVM", .546, .595, 0), ("DT", .706, .628, .002), ("RF", .727, .656, .001)]:
    D = ns.loc[[i for i in ns.index if i.startswith(f"D. nested {c}:")][0]]; C = ns.loc[[i for i in ns.index if i.startswith(f"C. nested {c}:")][0]]
    chk(f"nested {c} original (D)", D.nested_macroF1, dv, .0006); chk(f"nested {c} reduced (C)", C.nested_macroF1, cv, .0006)
chk("same-CV LR best-reduced gap", b.loc["LR", "mean_diff"], .043, .0006)
out = pd.DataFrame(rows); out.to_csv(str(TABLE_DIR) + "/claim_check.csv", index=False)
print(out.to_string()); print("\nFAILED:", out[~out.ok].claim.tolist())
