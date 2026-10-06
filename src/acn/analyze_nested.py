"""Summarise nested CV: score of the configuration chosen on INNER folds, measured on the untouched OUTER fold.
Outputs results/tables/nested_summary.csv, nested_selection_counts.csv, nested_naive_vs_nested.json"""
import json, numpy as np, pandas as pd
from scipy.stats import wilcoxon
from .common import newest
from .config import *

inner = pd.read_csv(newest("nested_inner_*.csv")); outer = pd.read_csv(newest("nested_outer_*.csv"))
outer["space"] = outer.experiment_id.str.split("|").str[0]
inner["space"] = inner.experiment_id.str.split("|").str[0]
keys = ["repeat", "fold"]; outer = outer.rename(columns={"repeat": "outer_repeat_", "fold": "outer_fold_"})
O = outer.set_index(["outer_repeat_", "outer_fold_", "experiment_id"])
I = inner.groupby(["outer_repeat", "outer_fold", "experiment_id"]).f1_macro.mean().rename("inner_f1").reset_index()
I["space"] = I.experiment_id.str.split("|").str[0]; I["clf"] = I.experiment_id.str.split("|").str[1]
I["is_orig"] = I.space == "orig"


def pick(sub):  # highest mean inner macro-F1; deterministic tie-break on experiment_id
    return sub.sort_values(["inner_f1", "experiment_id"], ascending=[False, True]).iloc[0].experiment_id


def run(name, filt):
    rows, sel = [], []
    for (r, f), g in I.groupby(["outer_repeat", "outer_fold"]):
        e = pick(g[filt(g)]); sel.append(e)
        rows.append(dict(outer_repeat=r, outer_fold=f, selected=e, **O.loc[(r, f, e), ["accuracy", "f1_macro", "balanced_accuracy", "mcc"]].to_dict()))
    return pd.DataFrame(rows)

res = {"A. nested: any (space, classifier, weighting)": run("all", lambda g: g.index == g.index)}
for c in CLASSIFIERS:
    res[f"B. nested {c}: choose space+weighting (orig allowed)"] = run(c, lambda g, c=c: g.clf == c)
    res[f"C. nested {c}: choose among REDUCED spaces+weighting"] = run(c, lambda g, c=c: (g.clf == c) & ~g.is_orig)
    res[f"D. nested {c}: ORIGINAL features only, choose weighting"] = run(c, lambda g, c=c: (g.clf == c) & g.is_orig)
sumrows, fixed = [], {}
def fx(eid): return O.xs(eid, level="experiment_id").sort_index()
for name, d in res.items():
    d = d.sort_values(["outer_repeat", "outer_fold"]); ref = None
    if name.startswith("A.") or name.startswith("D."): ref = "orig|RF|std" if name.startswith("A.") else f"orig|{name.split()[2].rstrip(':')}|std"
    elif name[:2] in ("B.", "C."):
        c = name.split()[2].rstrip(":"); ref = f"orig|{c}|std"
    if name[:2] in ("B.", "C."):   # fair reference: original features with the SAME freedom to choose the class weighting (nested)
        dd = res[f"D. nested {c}: ORIGINAL features only, choose weighting"].sort_values(["outer_repeat", "outer_fold"]); r = dd.f1_macro.values; ref = "D (orig, weighting chosen in inner CV)"
    else:
        r = fx(ref).f1_macro.values
    diff = d.f1_macro.values - r
    p = wilcoxon(d.f1_macro.values, r).pvalue if np.any(diff != 0) else 1.0
    sumrows.append(dict(procedure=name, outer_folds=len(d), nested_macroF1=d.f1_macro.mean(), sd=d.f1_macro.std(), nested_acc=d.accuracy.mean(),
                        nested_bacc=d.balanced_accuracy.mean(), nested_mcc=d.mcc.mean(), reference=ref, reference_macroF1=r.mean(),
                        diff_vs_reference=diff.mean(), wilcoxon_p_unadjusted=p, frac_selected_orig=np.mean([s.startswith("orig") for s in d.selected]),
                        n_distinct_selected=d.selected.nunique()))
S = pd.DataFrame(sumrows); S.to_csv("results/tables/nested_summary.csv", index=False)
cnt = res["A. nested: any (space, classifier, weighting)"].selected.value_counts().rename_axis("selected_config").reset_index(name="outer_folds_selected")
cnt.to_csv("results/tables/nested_selection_counts.csv", index=False)
# naive (same-CV) vs nested
main = pd.read_csv(newest("cv_results_2*.csv")); main = main[main.classifier != "DUMMY"]
naive = main.groupby("experiment_id").f1_macro.mean().max()
A = S.iloc[0]
json.dump(dict(naive_same_cv_best=naive, nested_estimate=A.nested_macroF1, nested_sd=A.sd, optimism=naive - A.nested_macroF1,
               selection_frequency=cnt.set_index("selected_config").outer_folds_selected.to_dict()), open("results/tables/nested_naive_vs_nested.json", "w"), indent=1)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(S.round(3).to_string()); print(cnt.head(8).to_string()); print("naive", naive, "nested", A.nested_macroF1)

# ---- compact LaTeX table for the paper (Table: nested selection)
lines = [r"\begin{tabular}{lcccc}", r"\hline", r"Classifier & Original (D) & Reduced, chosen (C) & $\Delta$ (D$-$C) & $p$ \\", r"\hline"]
for c in CLASSIFIERS:
    D = S[S.procedure.str.startswith(f"D. nested {c}:")].iloc[0]; C = S[S.procedure.str.startswith(f"C. nested {c}:")].iloc[0]
    d = res[f"D. nested {c}: ORIGINAL features only, choose weighting"].sort_values(["outer_repeat", "outer_fold"]).f1_macro.values
    cc = res[f"C. nested {c}: choose among REDUCED spaces+weighting"].sort_values(["outer_repeat", "outer_fold"]).f1_macro.values
    p = wilcoxon(d, cc).pvalue if np.any(d != cc) else 1.0
    lines.append(f"{CLF_NAMES[c] if c in CLF_NAMES else c} & {D.nested_macroF1:.3f}$\\pm${D.sd:.3f} & {C.nested_macroF1:.3f}$\\pm${C.sd:.3f} & {(D.nested_macroF1 - C.nested_macroF1):+.3f} & {('$<$0.001' if p < 0.001 else format(p, '.3f'))} \\\\".replace("+-", "$-$").replace(" -0", " $-$0"))
lines += [r"\hline", r"\end{tabular}"]
import os; os.makedirs("papers/ieee/tables", exist_ok=True); open("papers/ieee/tables/T11_nested.tex", "w").write("\n".join(lines) + "\n")
S.to_csv("results/tables/nested_summary.csv", index=False)
