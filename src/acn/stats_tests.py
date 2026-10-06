"""Paired statistics on macro-F1 across the 15 CV folds (same folds for every method -> paired design).

* Friedman test  : omnibus test across the 5 feature spaces (per classifier) and across the 5 classifiers (per space).
* Wilcoxon signed-rank (two-sided) with Holm correction: post-hoc pairwise comparisons; effect size = matched-pairs
  rank-biserial correlation r (+1 = first method always better).
CAVEAT: repeated-CV folds share training data, so the 15 differences are not independent; p-values are optimistic
(Nadeau & Bengio, 2003 - corrected resampled t-test is the usual remedy). Treat p-values as screening evidence only."""
import glob, itertools, sys
import numpy as np, pandas as pd
from scipy import stats
from .config import *

SPACES10 = ["orig", f"pca-{MATCHED_N}"] + [f"kpca-{k}-{MATCHED_N}" for k in KERNELS]
PAIRS = [("orig", f"pca-{MATCHED_N}"), (f"pca-{MATCHED_N}", f"kpca-linear-{MATCHED_N}"), (f"pca-{MATCHED_N}", f"kpca-rbf-{MATCHED_N}"),
         (f"pca-{MATCHED_N}", f"kpca-cosine-{MATCHED_N}"), ("orig", f"kpca-rbf-{MATCHED_N}"), ("orig", f"kpca-cosine-{MATCHED_N}")]


def latest(pattern):
    f = sorted(f for f in glob.glob(f"{RAW_DIR}/{pattern}") if "smoke" not in f)
    return f[-1]


def holm(p):
    p = np.asarray(p); o = np.argsort(p); adj = np.empty_like(p); run = 0
    for rank, i in enumerate(o):
        run = max(run, (len(p) - rank) * p[i]); adj[i] = min(1.0, run)
    return adj


def wilcoxon(a, b):
    d = a - b; nz = d[d != 0]
    if len(nz) == 0:
        return 0.0, 1.0, 0.0
    res = stats.wilcoxon(a, b, zero_method="wilcox")
    rk = stats.rankdata(np.abs(nz)); r = (rk[nz > 0].sum() - rk[nz < 0].sum()) / rk.sum()
    return float(res.statistic), float(res.pvalue), float(r)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else latest("cv_results_*.csv")
    df = pd.read_csv(path); df = df[df.class_weight == "none"]
    df["space"] = np.where(df.dimensionality_method == "orig", "orig",
                           np.where(df.dimensionality_method == "pca", "pca-" + df.components.astype(str),
                                    "kpca-" + df.kernel + "-" + df.components.astype(str)))
    wide = df[df.classifier.isin(CLASSIFIERS)].pivot_table(index=["repeat", "fold"], columns=["classifier", "space"], values="f1_macro")
    rows = []
    for c in CLASSIFIERS:
        for a, b in PAIRS:
            s, p, r = wilcoxon(wide[(c, a)].values, wide[(c, b)].values)
            rows.append(dict(test="wilcoxon", classifier=c, method_a=a, method_b=b, mean_f1_a=wide[(c, a)].mean(), mean_f1_b=wide[(c, b)].mean(),
                             mean_diff=(wide[(c, a)] - wide[(c, b)]).mean(), statistic=s, p_value=p, effect_r=r))
    w = pd.DataFrame(rows); w["p_holm"] = holm(w.p_value.values); w["significant_0.05"] = w.p_holm < 0.05
    fr = []
    for c in CLASSIFIERS:
        s, p = stats.friedmanchisquare(*[wide[(c, sp)].values for sp in SPACES10]); fr.append(dict(test="friedman_spaces", group=c, statistic=s, p_value=p))
    for sp in SPACES10:
        s, p = stats.friedmanchisquare(*[wide[(c, sp)].values for c in CLASSIFIERS]); fr.append(dict(test="friedman_classifiers", group=sp, statistic=s, p_value=p))
    fr = pd.DataFrame(fr); fr["p_holm"] = holm(fr.p_value.values)
    w.to_csv(f"{TABLE_DIR}/stat_wilcoxon.csv", index=False); fr.to_csv(f"{TABLE_DIR}/stat_friedman.csv", index=False)
    # Family 2: original vs the BEST reduced space of that classifier (best chosen on the same folds -> biased in favour of the
    # reduced space, so a loss by the reduced space is strong evidence while a win is optimistic).
    rows2 = []
    for c in CLASSIFIERS:
        cand = [sp for (cc, sp) in wide.columns if cc == c and sp != "orig"]; best = max(cand, key=lambda sp: wide[(c, sp)].mean())
        s_, p_, r_ = wilcoxon(wide[(c, "orig")].values, wide[(c, best)].values)
        rows2.append(dict(test="wilcoxon_best_reduced", classifier=c, method_a="orig", method_b=best, mean_f1_a=wide[(c, "orig")].mean(), mean_f1_b=wide[(c, best)].mean(),
                          mean_diff=(wide[(c, "orig")] - wide[(c, best)]).mean(), statistic=s_, p_value=p_, effect_r=r_))
    w2 = pd.DataFrame(rows2); w2["p_holm"] = holm(w2.p_value.values); w2["significant_0.05"] = w2.p_holm < 0.05
    w2.to_csv(f"{TABLE_DIR}/stat_best_reduced.csv", index=False); print(w2.round(4).to_string())
    pd.set_option("display.width", 200)
    print(w.round(4).to_string()); print(fr.round(4).to_string())


if __name__ == "__main__":
    main()
