"""Main experiment: repeated stratified K-fold CV over (feature space x classifier x class-weighting).

Per fold: impute+scale (train-fitted) -> reducer (train-fitted) -> classifier.  The reducer is fitted ONCE per
(fold, space) and shared by all classifiers - identical to fitting it inside each pipeline because it is deterministic
(equivalence is unit-tested in tests/test_pipeline.py).  Results are written to NEW timestamped files (never overwritten).

  python -m src.acn.run_cv                 # full grid (about 10-20 min on 2 cores)
  python -m src.acn.run_cv --smoke         # tiny pipeline check
"""
import argparse, json, time, warnings
from datetime import datetime
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import RepeatedStratifiedKFold
from .config import *
from .data import load_sample
from .evaluation import metrics
from .features import Space, all_spaces, fit_preprocess, fit_reduce
from .models import hyper_config, make_classifier


def run_task(rep, fold, tr, te, space, X, y, n_cls, seed, clfs, ts):
    rows, oof = [], {}
    Ztr, Zte, t_pf, t_pt = fit_preprocess(X[tr], X[te])
    Rtr, Rte, t_rf, t_rt = fit_reduce(Ztr, Zte, space, seed)
    jobs = [(c, False) for c in clfs] + [(c, True) for c in clfs if c in CLASS_WEIGHT_CAPABLE]
    if space.method == "orig":
        jobs.append(("DUMMY", False))
    for code, bal in jobs:
        clf = make_classifier(code, bal, seed)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t0 = time.perf_counter(); clf.fit(Rtr, y[tr]); t_cf = time.perf_counter() - t0
            t0 = time.perf_counter(); pred = clf.predict(Rte); t_pr = time.perf_counter() - t0
        n_warn = sum(issubclass(x.category, ConvergenceWarning) for x in w)
        eid = f"{space.name}|{code}|{'cw' if bal else 'std'}"
        rows.append(dict(experiment_id=eid, dataset="CIC-IDS2017", dataset_subset="Tue+Wed+Thu-am 1000-row stratified sample",
                         random_seed=seed, split_strategy="repeated_stratified_kfold", test_size=1.0 / N_SPLITS,
                         preprocessing="mean-impute+standardize (train-fitted)", dimensionality_method=space.method,
                         kernel=space.kernel or "", components=space.n or X.shape[1], classifier=code,
                         class_weight="balanced" if bal else "none", hyperparameter_config=json.dumps(hyper_config(clf), default=str),
                         repeat=rep, fold=fold, n_train=len(tr), n_test=len(te), convergence_warnings=n_warn,
                         **metrics(y[te], pred, n_cls),
                         train_time=t_pf + t_rf + t_cf, inference_time=t_pt + t_rt + t_pr,
                         reducer_fit_time=t_rf, clf_fit_time=t_cf, memory_usage=np.nan, timestamp=ts))
        if rep == 0:
            oof[eid] = (te.tolist(), pred.tolist())
    return rows, oof


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(SAMPLE_NPZ)); ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--splits", type=int, default=N_SPLITS); ap.add_argument("--repeats", type=int, default=N_REPEATS)
    ap.add_argument("--n-jobs", type=int, default=2); ap.add_argument("--out", default=str(RAW_DIR))
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    X, y, classes, _ = load_sample(a.data)
    spaces, clfs = all_spaces(), list(CLASSIFIERS)
    if a.smoke:
        spaces = [Space("orig"), Space("pca", n=10), Space("kpca", "rbf", 10)]; clfs = ["LR", "DT"]; a.repeats = 1
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rskf = RepeatedStratifiedKFold(n_splits=a.splits, n_repeats=a.repeats, random_state=a.seed)
    folds = [(i // a.splits, i % a.splits, tr, te) for i, (tr, te) in enumerate(rskf.split(X, y))]
    print(f"{len(folds)} folds x {len(spaces)} spaces; classifiers={clfs}; n={len(y)}, d={X.shape[1]}, classes={len(classes)}")
    t0 = time.time()
    res = Parallel(n_jobs=a.n_jobs, verbose=5)(delayed(run_task)(r, f, tr, te, s, X, y, len(classes), a.seed, clfs, ts)
                                                for (r, f, tr, te) in folds for s in spaces)
    df = pd.DataFrame([row for rows, _ in res for row in rows])
    oof = {}
    for _, o in res:
        for k, (idx, pr) in o.items():
            d = oof.setdefault(k, {"idx": [], "pred": []}); d["idx"] += idx; d["pred"] += pr
    tag = ("smoke_" if a.smoke else "") + ts
    import os; os.makedirs(a.out, exist_ok=True)
    df.to_csv(f"{a.out}/cv_results_{tag}.csv", index=False)
    json.dump(oof, open(f"{a.out}/oof_repeat0_{tag}.json", "w"))
    print(f"done in {time.time()-t0:.0f}s -> {a.out}/cv_results_{tag}.csv  ({len(df)} rows)")
    print(df.groupby(["dimensionality_method", "classifier", "class_weight"]).f1_macro.mean().round(3).to_string())


if __name__ == "__main__":
    main()
