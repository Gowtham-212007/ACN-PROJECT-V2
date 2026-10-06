"""Nested cross-validation for configuration selection.

Outer: repeated stratified 5-fold (performance estimate).  Inner: stratified 3-fold on the OUTER-TRAIN part only
(configuration selection by mean inner macro-F1).  The selected configuration is then scored on the untouched outer-test
fold, so the reported score is free of same-CV selection optimism.  Candidate set = every (space, classifier, weighting)
of the main grid (majority baseline excluded).  Inner validation folds hold only 2-3 records of the smallest classes,
so selection is noisy - this is reported, not hidden.

  python -m src.acn.run_nested --repeats 2 --n-jobs 2
"""
import argparse, json, time
from datetime import datetime
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from .config import *
from .data import load_sample
from .features import all_spaces
from .run_cv import run_task


def inner_task(orep, ofold, itr_global, iva_global, ifold, space, X, y, ncls, seed, clfs, ts):
    rows, _ = run_task(orep, ifold, itr_global, iva_global, space, X, y, ncls, seed, clfs, ts)
    for r in rows:
        r["outer_repeat"], r["outer_fold"] = orep, ofold
    return rows


def outer_task(orep, ofold, tr, te, space, X, y, ncls, seed, clfs, ts):
    rows, _ = run_task(orep, ofold, tr, te, space, X, y, ncls, seed, clfs, ts)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(SAMPLE_NPZ)); ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--repeats", type=int, default=2); ap.add_argument("--inner", type=int, default=3)
    ap.add_argument("--n-jobs", type=int, default=2); ap.add_argument("--out", default=str(RAW_DIR))
    a = ap.parse_args()
    X, y, classes, _ = load_sample(a.data)
    spaces, clfs, ncls = all_spaces(), list(CLASSIFIERS), len(classes)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outer = list(RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=a.repeats, random_state=a.seed).split(X, y))
    jobs_in, jobs_out = [], []
    for i, (tr, te) in enumerate(outer):
        orep, ofold = i // N_SPLITS, i % N_SPLITS
        skf = StratifiedKFold(a.inner, shuffle=True, random_state=a.seed + i)
        for j, (itr, iva) in enumerate(skf.split(X[tr], y[tr])):
            for s in spaces:
                jobs_in.append(delayed(inner_task)(orep, ofold, tr[itr], tr[iva], j, s, X, y, ncls, a.seed, clfs, ts))
        for s in spaces:
            jobs_out.append(delayed(outer_task)(orep, ofold, tr, te, s, X, y, ncls, a.seed, clfs, ts))
    print(f"{len(outer)} outer folds, {len(jobs_in)} inner + {len(jobs_out)} outer tasks", flush=True)
    t0 = time.time()
    res = Parallel(n_jobs=a.n_jobs, verbose=5)(jobs_in + jobs_out)
    rows = [r for rs in res for r in rs]
    n_in = len(jobs_in)
    inner = pd.DataFrame([r for rs in res[:n_in] for r in rs])
    outr = pd.DataFrame([r for rs in res[n_in:] for r in rs])
    inner = inner[inner.classifier != "DUMMY"]; outr = outr[outr.classifier != "DUMMY"]
    import os; os.makedirs(a.out, exist_ok=True)
    inner[["outer_repeat", "outer_fold", "fold", "experiment_id", "classifier", "f1_macro", "accuracy"]].to_csv(
        f"{a.out}/nested_inner_{ts}.csv", index=False)
    outr.to_csv(f"{a.out}/nested_outer_{ts}.csv", index=False)
    print(f"done in {time.time()-t0:.0f}s ts={ts}")


if __name__ == "__main__":
    main()
