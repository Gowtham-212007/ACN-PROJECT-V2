"""Small nested hyper-parameter search (tuning only INSIDE the outer-training data).
Outer: the same stratified 5-fold split as the main grid (repeat 0, seed 42).  Inner: stratified 3-fold on the outer-training set;
scaler/imputer/reducer are REFITTED on each inner-training split.  Selection criterion: mean inner macro-F1.
Grids (deliberately small): SVM C in {0.1,1,10} x gamma in {scale,0.01,0.1} x class_weight in {none,balanced};
KNN k in {3,5,7,11}; RF n_estimators in {100,200} x max_depth in {None,10,20} x class_weight in {none,balanced}.
Spaces: original, PCA-30, KPCA-cosine-30, KPCA-RBF-30 (RBF width is tuned via gamma of the KPCA too only through the default 1/78; not tuned).
Compared with the same classifiers at default settings on the same outer folds.
  ACN_RUN=v2 python -m src.acn.run_tuning --n-jobs 2"""
import argparse, itertools, time, warnings
from datetime import datetime
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from .config import *
from .data import load_sample
from .evaluation import metrics
from .features import Space, fit_preprocess, fit_reduce
from .models import make_classifier

SPACES = [Space("orig"), Space("pca", n=30), Space("kpca", "cosine", 30), Space("kpca", "rbf", 30)]
GRIDS = {"SVM": [dict(C=C, gamma=g, class_weight=cw) for C, g, cw in itertools.product([0.1, 1, 10], ["scale", 0.01, 0.1], [None, "balanced"])],
         "KNN": [dict(n_neighbors=k) for k in [3, 5, 7, 11]],
         "RF": [dict(n_estimators=n, max_depth=d, class_weight=cw) for n, d, cw in itertools.product([100, 200], [None, 10, 20], [None, "balanced"])]}


def build(code, p, seed):
    if code == "SVM": return SVC(kernel="rbf", random_state=seed, **p)
    if code == "KNN": return KNeighborsClassifier(**p)
    return RandomForestClassifier(random_state=seed, n_jobs=1, **p)


def task(of, tr, te, space, X, y, ncls, seed):
    rows = []
    skf = StratifiedKFold(3, shuffle=True, random_state=seed + of)
    inner = {c: np.zeros(len(GRIDS[c])) for c in GRIDS}
    for itr, iva in skf.split(X[tr], y[tr]):
        a, b = tr[itr], tr[iva]
        Za, Zb, *_ = fit_preprocess(X[a], X[b]); Ra, Rb, *_ = fit_reduce(Za, Zb, space, seed)
        for c, grid in GRIDS.items():
            for i, p in enumerate(grid):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore"); inner[c][i] += f1_score(y[b], build(c, p, seed).fit(Ra, y[a]).predict(Rb), labels=np.arange(ncls), average="macro", zero_division=0) / 3
    Ztr, Zte, *_ = fit_preprocess(X[tr], X[te]); Rtr, Rte, *_ = fit_reduce(Ztr, Zte, space, seed)
    for c, grid in GRIDS.items():
        best = int(np.argmax(inner[c])); p = grid[best]
        m_t = metrics(y[te], build(c, p, seed).fit(Rtr, y[tr]).predict(Rte), ncls)
        m_d = metrics(y[te], make_classifier(c, False, seed).fit(Rtr, y[tr]).predict(Rte), ncls)
        rows.append(dict(outer_fold=of, space=space.name, classifier=c, selected=str(p), inner_f1=inner[c][best], **{f"tuned_{k}": v for k, v in m_t.items()}, **{f"default_{k}": v for k, v in m_d.items()}))
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=str(SAMPLE_NPZ)); ap.add_argument("--n-jobs", type=int, default=2); ap.add_argument("--out", default=str(RAW_DIR))
    a = ap.parse_args(); X, y, classes, _ = load_sample(a.data)
    outer = list(StratifiedKFold(N_SPLITS, shuffle=True, random_state=SEED).split(X, y)) if False else None
    from sklearn.model_selection import RepeatedStratifiedKFold
    outer = list(RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED).split(X, y))[:N_SPLITS]   # repeat 0 of the main grid
    t0 = time.time()
    res = Parallel(n_jobs=a.n_jobs, verbose=5)(delayed(task)(i, tr, te, s, X, y, len(classes), SEED) for i, (tr, te) in enumerate(outer) for s in SPACES)
    df = pd.DataFrame([r for rs in res for r in rs]); ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"{a.out}/tuning_{ts}.csv", index=False); print(f"done {time.time()-t0:.0f}s")
    print(df.groupby(["classifier", "space"])[["default_f1_macro", "tuned_f1_macro"]].mean().round(3))


if __name__ == "__main__":
    main()
