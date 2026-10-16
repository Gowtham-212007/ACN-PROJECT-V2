"""Recompute every numeric claim in the v2 paper (abstract, results, discussion, limitations, conclusion) from RAW result files.
Rows: claim, recomputed value, value stated in the paper, tolerance, ok.  Output: <TABLE_DIR>/claim_check.csv.
  ACN_RUN=v2 python -m src.acn.check_claims        (v1 numbers: src/acn/check_claims_v1.py with ACN_RUN unset)"""
import ast, glob, json, numpy as np, pandas as pd
from .common import *
from .data import load_sample

rows = []
def chk(name, got, stated, tol=0.0006):
    rows.append(dict(claim=name, recomputed=round(float(got), 4), stated=stated, tol=tol, ok=bool(abs(float(got) - stated) <= tol)))

df = load_cv(); man = json.load(open(str(SAMPLE_NPZ).replace(".npz", ".manifest.json"))); prof = json.load(open(ROOT / "results" / "raw" / "raw_profile.json"))
def cell(space, c, cw="none", col="f1_macro"): return df[(df.space == space) & (df.classifier == c) & (df.class_weight == cw)][col]
# ---- data
chk("raw flows", man["n_raw_rows"], 2830743, 0); chk("classes", len(man["raw_counts"]), 15, 0); chk("files", len(man["files"]), 8, 0)
chk("duplicates removed", man["n_duplicates_removed"], 308381, 0); chk("duplicate share of raw rows (%)", 100 * man["n_duplicates_removed"] / man["n_raw_rows"], 10.9, .05)
chk("conflicting-label feature groups", man["feature_duplicate_groups_with_conflicting_labels"], 698, 0); chk("pool size", man["n_pool"], 2522362, 0)
chk("sample size", man["n_sample"], 6000, 0); chk("sample share of pool (%)", 100 * 6000 / man["n_pool"], .24, .005)
chk("NaN cells in sample", man["nan_cells_in_sample"], 2, 0); chk("benign share of sample (%)", 100 * man["sample_counts"]["BENIGN"] / 6000, 67.2, .05)
chk("benign share of pool (%)", 100 * man["pool_counts"]["BENIGN"] / man["n_pool"], 83, .5)
for k, v in [("Heartbleed", 11), ("Web Attack - Sql Injection", 21), ("Infiltration", 36)]: chk(f"sample count {k}", man["sample_counts"][k], v, 0)
chk("floor: min sample count over other classes", min(v for k, v in man["sample_counts"].items() if k not in ("Heartbleed", "Web Attack - Sql Injection", "Infiltration")), 100, 20)
chk("PortScan removed (%)", 100 * (1 - man["pool_counts"]["PortScan"] / man["raw_counts"]["PortScan"]), 43, .5); chk("Hulk removed (%)", 100 * (1 - man["pool_counts"]["DoS Hulk"] / man["raw_counts"]["DoS Hulk"]), 25, .5)
chk("benign removed (%)", 100 * (1 - man["pool_counts"]["BENIGN"] / man["raw_counts"]["BENIGN"]), 7.8, .05)
chk("constant features in all files", len(prof["constant_in_all_files"]), 8, 0)
chk("max share of rows with NaN/inf in a file (%) <= 0.2", max(100 * v["rows_with_nan_or_inf"] / v["rows"] for v in prof["files"].values()), 0.1, 0.1)
# ---- headline
for col, st in [("accuracy", .972), ("f1_macro", .901), ("mcc", .948), ("f1_weighted", .971), ("balanced_accuracy", .883)]: chk(f"RF orig {col} mean", cell("orig", "RF", col=col).mean(), st)
chk("RF orig accuracy sd", cell("orig", "RF", col="accuracy").std(), .004); chk("RF orig macro-F1 sd", cell("orig", "RF").std(), .020); chk("RF orig MCC sd", cell("orig", "RF", col="mcc").std(), .008)
du = df[df.classifier == "DUMMY"]; chk("majority accuracy", du.accuracy.mean(), .672); chk("majority macro-F1", du.f1_macro.mean(), .054); chk("majority MCC", du.mcc.mean(), 0, 1e-9)
g = df[df.classifier != "DUMMY"].groupby(["space", "classifier", "class_weight"]).f1_macro.mean().sort_values(ascending=False)
chk("best config is orig|RF|none", float(g.index[0] == ("orig", "RF", "none")), 1, 0)
chk("accuracy - macro-F1 gap", cell("orig", "RF", col="accuracy").mean() - cell("orig", "RF").mean(), .071)
chk("fold SD macro-F1 orig, min/max over classifiers ~0.02 (max)", max(cell("orig", c).std() for c in CLASSIFIERS), .024, .0006)
# ---- per class + confusion
pcl = pd.read_csv(TABLE_DIR / "T8_per_class_best.csv").set_index("Class")
tenok = ["BENIGN", "DDoS", "DoS GoldenEye", "DoS Hulk", "DoS Slowhttptest", "DoS slowloris", "FTP-Patator", "Heartbleed", "PortScan", "SSH-Patator"]
chk("ten classes with F1>=0.96 (min)", pcl.loc[tenok, "F1"].min(), .96, .005); chk("count classes F1>=0.96", float((pcl.F1 >= .955).sum()), 10, 0)
for k, v in [("Web Brute Force", .53), ("Web XSS", .59), ("Bot", .87), ("Infiltration", .875), ("Web Sql Injection", .84)]: chk(f"F1 {k}", pcl.loc[k, "F1"], v, .005)
chk("Bot recall", pcl.loc["Bot", "Recall"], .82, .005); chk("Infiltration recall", pcl.loc["Infiltration", "Recall"], .78, .005)
X, y, classes, _ = load_sample(); yt, yp = np.load(RAW_DIR / "best_oof_true.npy"), np.load(RAW_DIR / "best_oof_pred.npy"); bf, xs = classes.index("Web Attack - Brute Force"), classes.index("Web Attack - XSS")
chk("BF->XSS", ((yt == bf) & (yp == xs)).sum(), 48, 0); chk("BF total", (yt == bf).sum(), 103, 0); chk("XSS->BF", ((yt == xs) & (yp == bf)).sum(), 35, 0); chk("XSS total", (yt == xs).sum(), 101, 0)
chk("Heartbleed test records per fold", man["sample_counts"]["Heartbleed"] / 5, 2, .3); chk("SQLi test records per fold", man["sample_counts"]["Web Attack - Sql Injection"] / 5, 4, .3)
chk("Heartbleed train records per fold", man["sample_counts"]["Heartbleed"] * 4 / 5, 9, .3)
# ---- Table n=10 and stats
for c, st in [("LR", .736), ("KNN", .800), ("SVM", .675), ("DT", .881), ("RF", .901)]: chk(f"orig macro-F1 {c}", cell("orig", c).mean(), st)
for c, st in [("LR", .506), ("KNN", .802), ("SVM", .485), ("DT", .805), ("RF", .834)]: chk(f"PCA-10 macro-F1 {c}", cell("pca-10", c).mean(), st)
chk("SVM cosine-10", cell("kpca-cosine-10", "SVM").mean(), .605); chk("SVM RBF-10", cell("kpca-rbf-10", "SVM").mean(), .525)
w = pd.read_csv(TABLE_DIR / "stat_wilcoxon.csv"); chk("Wilcoxon comparisons", len(w), 30, 0); chk("significant", w["significant_0.05"].sum(), 23, 0)
def sig(c, a, b): r = w[(w.classifier == c) & (w.method_a == a) & (w.method_b == b)].iloc[0]; return bool(r["significant_0.05"]), r.mean_diff
chk("orig>PCA-10 sig for LR,SVM,DT,RF (count)", sum(sig(c, "orig", "pca-10")[0] and sig(c, "orig", "pca-10")[1] > 0 for c in ["LR", "SVM", "DT", "RF"]), 4, 0)
chk("orig vs PCA-10 KNN not sig", float(not sig("KNN", "orig", "pca-10")[0]), 1, 0); chk("orig vs PCA-10 KNN diff", sig("KNN", "orig", "pca-10")[1], -.001, .0006)
chk("orig>RBF-10 sig all five", sum(sig(c, "orig", "kpca-rbf-10")[0] and sig(c, "orig", "kpca-rbf-10")[1] > 0 for c in CLASSIFIERS), 5, 0)
chk("orig>cos-10 sig all five", sum(sig(c, "orig", "kpca-cosine-10")[0] and sig(c, "orig", "kpca-cosine-10")[1] > 0 for c in CLASSIFIERS), 5, 0)
chk("RBF worse than PCA sig: LR,KNN,DT,RF", sum(sig(c, "pca-10", "kpca-rbf-10")[0] and sig(c, "pca-10", "kpca-rbf-10")[1] > 0 for c in ["LR", "KNN", "DT", "RF"]), 4, 0)
chk("RBF better than PCA sig: SVM", float(sig("SVM", "pca-10", "kpca-rbf-10")[0] and sig("SVM", "pca-10", "kpca-rbf-10")[1] < 0), 1, 0)
chk("cosine better than PCA sig: SVM", float(sig("SVM", "pca-10", "kpca-cosine-10")[0] and sig("SVM", "pca-10", "kpca-cosine-10")[1] < 0), 1, 0); chk("SVM cosine-PCA diff", -sig("SVM", "pca-10", "kpca-cosine-10")[1], .120)
chk("cosine worse than PCA sig: LR,KNN,DT", sum(sig(c, "pca-10", "kpca-cosine-10")[0] and sig(c, "pca-10", "kpca-cosine-10")[1] > 0 for c in ["LR", "KNN", "DT"]), 3, 0)
chk("cosine vs PCA RF not sig", float(not sig("RF", "pca-10", "kpca-cosine-10")[0]), 1, 0)
chk("linear vs PCA never sig", float(not any(sig(c, "pca-10", "kpca-linear-10")[0] for c in CLASSIFIERS)), 1, 0)
b = pd.read_csv(TABLE_DIR / "stat_best_reduced.csv").set_index("classifier")
chk("best-reduced DT gap", b.loc["DT", "mean_diff"], .070); chk("best-reduced RF gap", b.loc["RF", "mean_diff"], .056); chk("best-reduced RF p_holm", b.loc["RF", "p_holm"], .0003, .00005); chk("best-reduced DT p_holm", b.loc["DT", "p_holm"], .0003, .00005)
chk("best-reduced RF/DT r=1", float(b.loc["RF", "effect_r"] == 1 and b.loc["DT", "effect_r"] == 1), 1, 0)
chk("best-reduced LR space is pca-30", float(b.loc["LR", "method_b"] == "pca-30"), 1, 0); chk("best-reduced LR gap", b.loc["LR", "mean_diff"], .004, .0006); chk("best-reduced LR p_holm", b.loc["LR", "p_holm"], .021, .0006)
chk("best-reduced KNN not sig", float(not b.loc["KNN", "significant_0.05"]), 1, 0)
chk("SVM cosine-30", cell("kpca-cosine-30", "SVM").mean(), .746); chk("SVM best-reduced p_holm", b.loc["SVM", "p_holm"], .0003, .00005); chk("SVM best-reduced r=-1", b.loc["SVM", "effect_r"], -1, 0)
for n, st in zip(COMPONENTS, [.520, .605, .690, .725, .746]): chk(f"SVM cosine-{n}", cell(f"kpca-cosine-{n}", "SVM").mean(), st)
# ---- kernel/comps
lin = lambda cs, cws: max(abs(cell(f"pca-{n}", c, cw).mean() - cell(f"kpca-linear-{n}", c, cw).mean()) for c in cs for cw in cws for n in COMPONENTS if len(cell(f"pca-{n}", c, cw)))
chk("lin-PCA LR max", lin(["LR"], ["none", "balanced"]), .001, .0006); chk("lin-PCA KNN,SVM max", lin(["KNN", "SVM"], ["none", "balanced"]), 0, 1e-6)
chk("lin-PCA DT std-weights max", lin(["DT"], ["none"]), .004, .0006); chk("lin-PCA RF std max", lin(["RF"], ["none"]), .005, .0006)
chk("lin-PCA DT all-weights max", lin(["DT"], ["none", "balanced"]), .007, .0006); chk("lin-PCA RF all-weights max", lin(["RF"], ["none", "balanced"]), .005, .0006)
chk("LR PCA-5", cell("pca-5", "LR").mean(), .37, .005); chk("LR PCA-30", cell("pca-30", "LR").mean(), .73, .005)
def spreads(c):
    t = df[(df.classifier == c) & (df.class_weight == "none") & (df.dimensionality_method != "orig")].groupby(["kernel", "components"]).f1_macro.mean().unstack(); return t.mean(axis=1), t.mean(axis=0)
for c, kern_gt in [("LR", 0), ("KNN", 1), ("SVM", 0), ("DT", 1), ("RF", 1)]:
    km, cm_ = spreads(c); chk(f"{c}: kernel spread > component spread (paper: KNN,DT,RF yes)", float(km.max() - km.min() > cm_.max() - cm_.min()), kern_gt, 0)
for c in ["LR", "KNN", "DT", "RF"]: chk(f"{c}: RBF is the weakest kernel (mean over n)", float(spreads(c)[0].idxmin() == "rbf"), 1, 0)
km, _ = spreads("SVM"); chk("SVM kernel means cosine", km["cosine"], .657, .0006); chk("SVM kernel means linear", km["linear"], .536, .0006); chk("SVM kernel means rbf", km["rbf"], .515, .0006)
# ---- class weighting
for c, a, bb in [("LR", .748, .863), ("SVM", .680, .827)]: chk(f"{c} bacc none", cell("orig", c, "none", "balanced_accuracy").mean(), a); chk(f"{c} bacc balanced", cell("orig", c, "balanced", "balanced_accuracy").mean(), bb)
for c, a, bb in [("SVM", .675, .686), ("DT", .881, .892), ("LR", .736, .710), ("RF", .901, .885)]: chk(f"{c} F1 none", cell("orig", c).mean(), a); chk(f"{c} F1 balanced", cell("orig", c, "balanced").mean(), bb)
# ---- nested
ns = pd.read_csv(TABLE_DIR / "nested_summary.csv").set_index("procedure"); A = ns.iloc[0]
chk("nested macro-F1", A.nested_macroF1, .900); chk("nested sd", A.sd, .022); chk("nested acc", A.nested_acc, .972); chk("nested MCC", A.nested_mcc, .947)
chk("optimism", df[df.classifier != "DUMMY"].groupby("experiment_id").f1_macro.mean().max() - A.nested_macroF1, .001, .0006); chk("orig chosen all 15", A.frac_selected_orig, 1, 0)
sel = pd.read_csv(TABLE_DIR / "nested_selection_counts.csv").set_index("selected_config").outer_folds_selected
chk("nested RF std count", sel["orig|RF|std"], 11, 0); chk("nested DT std count", sel["orig|DT|std"], 3, 0); chk("nested DT cw count", sel["orig|DT|cw"], 1, 0)
for c, dv, cv in [("LR", .736, .731), ("KNN", .800, .799), ("SVM", .686, .746), ("DT", .891, .799), ("RF", .901, .839)]:
    D = ns.loc[[i for i in ns.index if i.startswith(f"D. nested {c}:")][0]]; C = ns.loc[[i for i in ns.index if i.startswith(f"C. nested {c}:")][0]]
    chk(f"nested {c} orig", D.nested_macroF1, dv); chk(f"nested {c} reduced", C.nested_macroF1, cv)
D_ = lambda c: ns.loc[[i for i in ns.index if i.startswith(f"D. nested {c}:")][0]].nested_macroF1; C_ = lambda c: ns.loc[[i for i in ns.index if i.startswith(f"C. nested {c}:")][0]].nested_macroF1
for c, st in [("DT", .093), ("RF", .062), ("LR", .004), ("KNN", .002), ("SVM", -.060)]: chk(f"nested gap {c}", D_(c) - C_(c), st, .0011)
chk("nested LR unadjusted p", ns.loc[[i for i in ns.index if i.startswith("C. nested LR:")][0]].wilcoxon_p_unadjusted, .010, .0006)
# ---- tuning
t = pd.read_csv(newest("tuning_*.csv")); t["p"] = t.selected.apply(ast.literal_eval)
def tm(c, s, k): return t[(t.classifier == c) & (t.space == s)][k].mean()
for (c, s, d, tu) in [("RF", "orig", .901, .899), ("RF", "pca-30", .842, .839), ("SVM", "orig", .668, .791), ("SVM", "kpca-cosine-30", .745, .812), ("KNN", "orig", .801, .808)]:
    chk(f"tuning {c} {s} default", tm(c, s, "default_f1_macro"), d); chk(f"tuning {c} {s} tuned", tm(c, s, "tuned_f1_macro"), tu)
chk("SVM gap default (orig vs cos30)", tm("SVM", "kpca-cosine-30", "default_f1_macro") - tm("SVM", "orig", "default_f1_macro"), .076, .0011); chk("SVM gap tuned", tm("SVM", "kpca-cosine-30", "tuned_f1_macro") - tm("SVM", "orig", "tuned_f1_macro"), .021, .0011)
sv = t[t.classifier == "SVM"].pivot(index="outer_fold", columns="space", values="tuned_f1_macro"); chk("cosine-30 >= orig in folds (tuned SVM)", (sv["kpca-cosine-30"] >= sv["orig"]).sum(), 4, 0)
chk("SVM C=10 in all selections", float((t[t.classifier == "SVM"].p.apply(lambda x: x["C"]) == 10).all()), 1, 0); chk("KNN k=3 in all selections", float((t[t.classifier == "KNN"].p.apply(lambda x: x["n_neighbors"]) == 3).all()), 1, 0)
chk("tuning selections per classifier", len(t[t.classifier == "SVM"]), 20, 0)
# ---- temporal / blocked
ti = json.load(open(RAW_DIR / "temporal_info.json")); chk("temporal train", ti["n_train"], 4199, 0); chk("temporal test scored", ti["n_test_scored"], 1769, 0); chk("temporal dropped", ti["n_test_dropped_unseen_class"], 32, 0)
chk("temporal classes scored", len(ti["classes_scored"]), 7, 0); chk("temporal infiltration test records", ti["test_class_counts"]["Infiltration"], 4, 0)
tr = pd.read_csv(RAW_DIR / "temporal_results.csv"); T = lambda sp, s, c: tr[(tr.split == sp) & (tr.space == s) & (tr.classifier == c)].f1_macro_present.mean()
ch, rd = "chronological_within_file_70_30", "random_stratified_70_30_same_classes"
for c, s, sp, st in [("RF", "orig", ch, .838), ("RF", "orig", rd, .948), ("DT", "orig", ch, .846), ("DT", "orig", rd, .959), ("RF", "pca-10", ch, .759), ("RF", "kpca-cosine-30", ch, .704), ("KNN", "orig", ch, .790), ("KNN", "kpca-cosine-30", ch, .806), ("SVM", "kpca-cosine-30", ch, .616), ("SVM", "orig", ch, .479)]: chk(f"temporal {sp[:4]} {c} {s}", T(sp, s, c), st)
chk("temporal penalty RF/DT ~0.11", (T(rd, "orig", "RF") - T(ch, "orig", "RF") + T(rd, "orig", "DT") - T(ch, "orig", "DT")) / 2, .112, .006)
chk("chrono: orig best for DT,RF,LR vs PCA-10, cos-30 (count of 6)", sum(T(ch, "orig", c) > max(T(ch, "pca-10", c), T(ch, "kpca-cosine-30", c)) for c in ["DT", "RF", "LR"]), 3, 0)
bl = pd.read_csv(RAW_DIR / "blocked_results.csv"); bi = json.load(open(RAW_DIR / "blocked_info.json")); chk("blocked classes scored per fold", float(sum(len(d["scored"]) for d in bi)), 39, 0)
chk("blocked class counts 6,9,10,8,6", float([len(d["scored"]) for d in bi] == [6, 9, 10, 8, 6]), 1, 0)
B = lambda sp, s, c: bl[(bl.split == sp) & (bl.space == s) & (bl.classifier == c)].f1_macro_present.mean()
bk, br = "blocked_contiguous_5", "random_stratified_5fold_same_classes"
for c, s, sp, st in [("RF", "orig", bk, .851), ("RF", "orig", br, .932), ("RF", "pca-10", bk, .807), ("RF", "kpca-cosine-30", bk, .812), ("SVM", "kpca-cosine-30", bk, .662), ("SVM", "orig", bk, .581)]: chk(f"blocked {sp[:4]} {c} {s}", B(sp, s, c), st)
chk("blocked: orig best for DT,RF,LR (count)", sum(B(bk, "orig", c) > max(B(bk, "pca-10", c), B(bk, "kpca-cosine-30", c)) for c in ["DT", "RF", "LR"]), 3, 0)
chk("blocked KNN spread across 3 spaces <= 0.02", max(B(bk, s, "KNN") for s in ["orig", "pca-10", "kpca-cosine-30"]) - min(B(bk, s, "KNN") for s in ["orig", "pca-10", "kpca-cosine-30"]), .019, .002)
pen = []
for tb, a, bb in [(tr, rd, ch), (bl, br, bk)]:
    for c in CLASSIFIERS:
        for s in ["orig", "pca-10", "kpca-cosine-30"]: pen.append((tb[(tb.split == a) & (tb.space == s) & (tb.classifier == c)].f1_macro_present.mean() - tb[(tb.split == bb) & (tb.space == s) & (tb.classifier == c)].f1_macro_present.mean()))
chk("min penalty over temporal+blocked tables", min(pen), .06, .006); chk("max penalty", max(pen), .245, .006)
chk("chrono penalty min over classifiers (orig)", min(T(rd, "orig", c) - T(ch, "orig", c) for c in CLASSIFIERS), .07, .006); chk("chrono penalty max (orig, SVM)", max(T(rd, "orig", c) - T(ch, "orig", c) for c in CLASSIFIERS), .236, .006)
# ---- cost
rt = pd.read_csv(newest("runtime_2*.csv")); RF_ = rt.groupby("space").reducer_fit_s.mean(); rt = rt.set_index(["space", "classifier"]); ks = ["kpca-linear-10", "kpca-rbf-10", "kpca-cosine-10"]
chk("PCA fit s", RF_["pca-10"], .0247, .002); chk("KPCA fit min", min(RF_[k] for k in ks), 5.5, .05); chk("KPCA fit max", max(RF_[k] for k in ks), 5.6, .05)
chk("fit ratio > 200", np.mean([RF_[k] for k in ks]) / RF_["pca-10"], 222, 30)
chk("DT PCA train", rt.loc[("pca-10", "DT"), "train_time_s"], .07, .005); chk("DT KPCA min", min(rt.loc[(k, "DT"), "train_time_s"] for k in ks), 5.3, .05); chk("DT KPCA max", max(rt.loc[(k, "DT"), "train_time_s"] for k in ks), 5.6, .05)
chk("RF orig train", rt.loc[("orig", "RF"), "train_time_s"], .84, .005); chk("RF PCA train", rt.loc[("pca-10", "RF"), "train_time_s"], .90, .005)
chk("RF KPCA train min", min(rt.loc[(k, "RF"), "train_time_s"] for k in ks), 6.3, .06); chk("RF KPCA train max", max(rt.loc[(k, "RF"), "train_time_s"] for k in ks), 6.6, .05)
chk("RF infer orig", rt.loc[("orig", "RF"), "inference_time_s"], .020, .0006); chk("RF infer PCA", rt.loc[("pca-10", "RF"), "inference_time_s"], .021, .0006)
chk("RF infer KPCA min", min(rt.loc[(k, "RF"), "inference_time_s"] for k in ks), .092, .0006); chk("RF infer KPCA max", max(rt.loc[(k, "RF"), "inference_time_s"] for k in ks), .123, .0006)
chk("infer ratio ~5", np.mean([rt.loc[(k, "RF"), "inference_time_s"] for k in ks]) / rt.loc[("pca-10", "RF"), "inference_time_s"], 5, .5)
chk("peak mem KPCA MB", rt.loc[("kpca-rbf-10", "RF"), "peak_mem_mb"], 363, .5); chk("peak mem orig MB", rt.loc[("orig", "RF"), "peak_mem_mb"], 9.8, .1); chk("mem ratio ~37", rt.loc[("kpca-rbf-10", "RF"), "peak_mem_mb"] / rt.loc[("orig", "RF"), "peak_mem_mb"], 37, .5)
sc = pd.read_csv(newest("kpca_scaling_2*.csv")); sc = sc[sc.method == "kpca-rbf-10"].set_index("n")
for n, st in [(400, 3.1), (800, 11.0), (1600, 41.6), (3200, 161.3), (4800, 359.1)]: chk(f"scaling mem n={n}", sc.loc[n, "peak_mem_mb"], st, .06)
chk("mem slope 800->4800", np.log(sc.loc[4800, "peak_mem_mb"] / sc.loc[800, "peak_mem_mb"]) / np.log(6), 1.9, .06); chk("time slope 800->4800", np.log(sc.loc[4800, "fit_time_s"] / sc.loc[800, "fit_time_s"]) / np.log(6), 2.4, .06)
chk("fit time n=800", sc.loc[800, "fit_time_s"], .08, .005); chk("fit time n=4800", sc.loc[4800, "fit_time_s"], 5.9, .06)
chk("one kernel matrix MB at n=4800", 4800 ** 2 * 8 / 1e6, 184, 1); chk("traced peak / one matrix", sc.loc[4800, "peak_mem_mb"] / (4800 ** 2 * 8 / 1e6), 2, .1)
chk("THEORETICAL kernel matrix, 2,830,743 flows, TB", 2830743 ** 2 * 8 / 1e12, 64, .5)
# ---- training size
z = pd.read_csv(newest("size_results_2*.csv")); z["space"] = np.where(z.dimensionality_method == "orig", "orig", z.dimensionality_method + np.where(z.kernel.notna(), "-" + z.kernel.fillna(""), ""))
m = z[z.classifier != "DUMMY"].groupby(["classifier", "n_train", "space"]).f1_macro.mean()
chk("size: orig highest for LR,DT,RF at all 3 sizes (count of 9)", sum(m.loc[(c, n)].idxmax() == "orig" for c in ["LR", "DT", "RF"] for n in [2400, 3600, 4800]), 9, 0)
chk("size: SVM orig highest at 3600 & 4800", sum(m.loc[("SVM", n)].idxmax() == "orig" for n in [3600, 4800]), 2, 0); chk("size: SVM n=2400 cosine - orig", m.loc[("SVM", 2400, "kpca-cosine")] - m.loc[("SVM", 2400, "orig")], .009, .0011)
out = pd.DataFrame(rows); out.to_csv(TABLE_DIR / "claim_check.csv", index=False)
print(f"{len(out)} checks; failed: {out[~out.ok].claim.tolist()}"); print(out[~out.ok].to_string())
