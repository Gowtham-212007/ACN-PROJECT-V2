"""Within-file chronological generalisation test (the raw MachineLearningCVE files have NO Timestamp column).
For every source file (one capture day / session) the FIRST 70% of its rows (by original row position) are training data and the LAST 30% are test data.
Row order is ASSUMED to follow capture time: evidence (attack rows clustered in contiguous blocks; attack share varies strongly across the file)
supports this but it is not proven.  Whole-day splits are NOT used: each attack family occurs on one day, so a day-wise split leaves test classes
absent from training.  Only classes present in BOTH parts are scored (reported).  A random stratified 70/30 split of the SAME rows/classes
(5 seeds) is run for comparison, so the temporal 'penalty' is measured on identical class sets.
  ACN_RUN=v2 python -m src.acn.run_temporal --data data/sample_raw6000.npz"""
import argparse, json, time, warnings
import numpy as np, pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from .config import *
from .data import load_sample
from .evaluation import metrics
from .features import Space, fit_preprocess, fit_reduce
from .models import make_classifier

SPACES = [Space("orig"), Space("pca", n=10), Space("pca", n=30), Space("kpca", "linear", 10), Space("kpca", "rbf", 10), Space("kpca", "cosine", 10), Space("kpca", "cosine", 30)]


def chrono_split(day, order, frac=0.7):
    tr = np.zeros(len(day), bool)
    for d in np.unique(day):
        m = np.where(day == d)[0]; cut = np.quantile(order[m], frac); tr[m[order[m] <= cut]] = True
    return np.where(tr)[0], np.where(~tr)[0]


def evaluate(split_name, X, y, classes, tr, te, present, rows, seed=SEED):
    Ztr, Zte, *_ = fit_preprocess(X[tr], X[te])
    for sp in SPACES:
        Rtr, Rte, *_ = fit_reduce(Ztr, Zte, sp, SEED)
        for c in CLASSIFIERS:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore"); pred = make_classifier(c, False, SEED).fit(Rtr, y[tr]).predict(Rte)
            m = metrics(y[te], pred, len(classes)); m["f1_macro_present"] = f1_score(y[te], pred, labels=present, average="macro", zero_division=0)
            rows.append(dict(split=split_name, seed=seed, space=sp.name, classifier=c, n_train=len(tr), n_test=len(te), n_classes_scored=len(present), **m))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=str(SAMPLE_NPZ)); ap.add_argument("--out", default=str(RAW_DIR)); ap.add_argument("--random-seeds", type=int, default=5)
    a = ap.parse_args(); X, y, classes, meta = load_sample(a.data); tr, te = chrono_split(meta["day"], meta["order"])
    train_cls = np.unique(y[tr]); keep = np.isin(y[te], train_cls); te_dropped = te[~keep]; te = te[keep]; present = np.intersect1d(np.unique(y[te]), train_cls)
    info = dict(n_train=int(len(tr)), n_test_scored=int(len(te)), n_test_dropped_unseen_class=int(len(te_dropped)), classes_scored=[classes[i] for i in present],
                classes_not_scored=[classes[i] for i in range(len(classes)) if i not in present],
                test_class_counts={classes[i]: int((y[te] == i).sum()) for i in present}, train_class_counts={classes[i]: int((y[tr] == i).sum()) for i in present},
                files=[str(f) for f in meta["files"]], rule="first 70% of rows (by original order) of each file = train, last 30% = test")
    print(json.dumps(info, indent=1)); json.dump(info, open(f"{a.out}/temporal_info.json", "w"), indent=1)
    rows = []; evaluate("chronological_within_file_70_30", X, y, classes, tr, te, present, rows)
    # random stratified 70/30 on the same rows, same class set, same sizes
    pool = np.concatenate([tr, te]); mask = np.isin(y[pool], present); pool = pool[mask]
    for s in range(a.random_seeds):
        r_tr, r_te = train_test_split(pool, test_size=len(te) / len(pool), stratify=y[pool], random_state=s)
        evaluate("random_stratified_70_30_same_classes", X, y, classes, r_tr, r_te, present, rows, seed=s)
    df = pd.DataFrame(rows); df.to_csv(f"{a.out}/temporal_results.csv", index=False)
    print(df.groupby(["split", "space", "classifier"]).f1_macro_present.mean().unstack().round(3).to_string())


if __name__ == "__main__":
    main()
