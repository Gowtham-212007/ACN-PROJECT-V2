"""Blocked (contiguous-in-time) cross-validation: every source file is cut into 5 contiguous blocks by original row order; each block in turn is the
test set and the other blocks (all files) the training set.  Unlike random folds, near-in-time flows (same attack session/burst) never straddle
train and test.  Row order is ASSUMED to follow capture time (see run_temporal.py).  Per fold only classes present in both train and test are scored
(macro-F1 over those classes); the number scored per fold is reported.  A random stratified 5-fold on the SAME rows, scored on the SAME classes per
fold, is the comparator.  Uses fixed default hyper-parameters, standard class weights.
  ACN_RUN=v2 python -m src.acn.run_blocked"""
import argparse, json, warnings
import numpy as np, pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from .config import *
from .data import load_sample
from .evaluation import metrics
from .features import Space, fit_preprocess, fit_reduce
from .models import make_classifier

SPACES = [Space("orig"), Space("pca", n=10), Space("pca", n=30), Space("kpca", "linear", 10), Space("kpca", "rbf", 10), Space("kpca", "cosine", 10), Space("kpca", "cosine", 30)]
K = 5


def blocks(day, order):
    b = np.zeros(len(day), int)
    for d in np.unique(day):
        m = np.where(day == d)[0]; r = np.argsort(np.argsort(order[m])); b[m] = np.minimum((K * r) // len(m), K - 1)
    return b


def run_fold(tag, k, X, y, classes, tr, te, rows):
    present = np.intersect1d(np.unique(y[te]), np.unique(y[tr])); keep = np.isin(y[te], present); te = te[keep]
    Ztr, Zte, *_ = fit_preprocess(X[tr], X[te])
    for sp in SPACES:
        Rtr, Rte, *_ = fit_reduce(Ztr, Zte, sp, SEED)
        for c in CLASSIFIERS:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore"); pred = make_classifier(c, False, SEED).fit(Rtr, y[tr]).predict(Rte)
            m = metrics(y[te], pred, len(classes)); m["f1_macro_present"] = f1_score(y[te], pred, labels=present, average="macro", zero_division=0)
            rows.append(dict(split=tag, fold=k, space=sp.name, classifier=c, n_train=len(tr), n_test=len(te), n_classes_scored=len(present), **m))
    return present


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=str(SAMPLE_NPZ)); ap.add_argument("--out", default=str(RAW_DIR))
    a = ap.parse_args(); X, y, classes, meta = load_sample(a.data); blk = blocks(meta["day"], meta["order"]); rows, info = [], []
    for k in range(K):
        tr, te = np.where(blk != k)[0], np.where(blk == k)[0]
        pres = run_fold("blocked_contiguous_5", k, X, y, classes, tr, te, rows); info.append(dict(fold=k, scored=[classes[i] for i in pres], n_test=int(len(te))))
        # comparator: random stratified fold, scored on the SAME classes
        skf = list(StratifiedKFold(K, shuffle=True, random_state=SEED).split(X, y))[k]; r_tr, r_te = skf; r_te = r_te[np.isin(y[r_te], pres)]
        run_fold_rows = []; Ztr, Zte, *_ = fit_preprocess(X[r_tr], X[r_te])
        for sp in SPACES:
            Rtr, Rte, *_ = fit_reduce(Ztr, Zte, sp, SEED)
            for c in CLASSIFIERS:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore"); pred = make_classifier(c, False, SEED).fit(Rtr, y[r_tr]).predict(Rte)
                m = metrics(y[r_te], pred, len(classes)); m["f1_macro_present"] = f1_score(y[r_te], pred, labels=pres, average="macro", zero_division=0)
                rows.append(dict(split="random_stratified_5fold_same_classes", fold=k, space=sp.name, classifier=c, n_train=len(r_tr), n_test=len(r_te), n_classes_scored=len(pres), **m))
        print("fold", k, "classes scored", len(pres), flush=True)
    df = pd.DataFrame(rows); df.to_csv(f"{a.out}/blocked_results.csv", index=False); json.dump(info, open(f"{a.out}/blocked_info.json", "w"), indent=1)
    print(df.groupby(["split", "space", "classifier"]).f1_macro_present.mean().unstack().round(3).to_string())


if __name__ == "__main__":
    main()
