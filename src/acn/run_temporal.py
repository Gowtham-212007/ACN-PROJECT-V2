"""Chronological (within-day) generalisation test: for every source file, the FIRST 70% of its rows (by original order) are
training data and the LAST 30% are test data.  Only classes present in both parts are scored.  Requires an .npz made by
prepare_raw.py (has `day` and `order`).  Whole-day splits are NOT used: in CIC-IDS2017 each attack family occurs on one day,
so a day-wise split would leave test classes absent from training.
  python -m src.acn.run_temporal --data data/sample_raw.npz --max-train 6000       # NOT executed on real raw data in the sandbox"""
import argparse, time
import numpy as np, pandas as pd
from .config import *
from .data import load_sample
from .evaluation import metrics
from .features import Space, all_spaces, fit_preprocess, fit_reduce
from .models import make_classifier


def chrono_split(day, order, frac=0.7):
    tr = np.zeros(len(day), bool)
    for d in np.unique(day):
        m = np.where(day == d)[0]; cut = np.quantile(order[m], frac); tr[m[order[m] <= cut]] = True
    return np.where(tr)[0], np.where(~tr)[0]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--max-train", type=int, default=6000); ap.add_argument("--out", default=str(RAW_DIR))
    a = ap.parse_args(); X, y, classes, meta = load_sample(a.data); tr, te = chrono_split(meta["day"], meta["order"])
    if len(tr) > a.max_train: tr = np.random.RandomState(SEED).choice(tr, a.max_train, replace=False)
    keep = np.isin(y[te], np.unique(y[tr])); te = te[keep]; present = np.unique(y[te])
    print(f"train={len(tr)} test={len(te)} classes scored={len(present)}/{len(classes)}"); rows = []
    Ztr, Zte, *_ = fit_preprocess(X[tr], X[te])
    for sp in [Space("orig"), Space("pca", n=10)] + [Space("kpca", k, 10) for k in KERNELS]:
        Rtr, Rte, *_ = fit_reduce(Ztr, Zte, sp, SEED)
        for c in CLASSIFIERS:
            pred = make_classifier(c, False, SEED).fit(Rtr, y[tr]).predict(Rte)
            m = metrics(y[te], pred, len(classes)); m["f1_macro"] = __import__("sklearn.metrics", fromlist=["f1_score"]).f1_score(y[te], pred, labels=present, average="macro", zero_division=0)
            rows.append(dict(space=sp.name, classifier=c, split_strategy="chronological_within_file_70_30", **m))
    pd.DataFrame(rows).to_csv(f"{a.out}/temporal_results.csv", index=False); print(pd.DataFrame(rows).pivot(index="space", columns="classifier", values="f1_macro").round(3))


if __name__ == "__main__":
    main()
