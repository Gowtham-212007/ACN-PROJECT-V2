"""Training-size sensitivity (replaces the original single-split 0.2/0.4/0.6 design with 10 random stratified splits each).
NOT a temporal / day-aware split: the cached sample has no timestamps or day labels (see reports/RESEARCH_AUDIT.md)."""
import time
from datetime import datetime
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import StratifiedShuffleSplit
from .config import *
from .data import load_sample
from .features import Space
from .run_cv import run_task

SPACES = [Space("orig"), Space("pca", n=10)] + [Space("kpca", k, 10) for k in KERNELS]
TEST_SIZES, REPEATS = [0.2, 0.4, 0.6], 10


def main():
    X, y, classes, _ = load_sample(); ts = datetime.now().strftime("%Y%m%d_%H%M%S"); jobs = []
    for tsz in TEST_SIZES:
        for r, (tr, te) in enumerate(StratifiedShuffleSplit(REPEATS, test_size=tsz, random_state=SEED).split(X, y)):
            jobs += [(tsz, r, tr, te, s) for s in SPACES]
    res = Parallel(n_jobs=2)(delayed(run_task)(r, 0, tr, te, s, X, y, len(classes), SEED, ["LR", "KNN", "SVM", "DT", "RF"], ts)
                             for (tsz, r, tr, te, s) in jobs)
    rows = []
    for (tsz, r, tr, te, s), (rr, _) in zip(jobs, res):
        for row in rr:
            row.update(test_size=tsz, split_strategy="stratified_shuffle_split", repeat=r); rows.append(row)
    df = pd.DataFrame(rows); df = df[df.class_weight == "none"]
    df.to_csv(f"{RAW_DIR}/size_results_{ts}.csv", index=False); print(len(df), "rows")


if __name__ == "__main__":
    main()
