"""Serial runtime + memory benchmark (no parallelism, so timings are not distorted by worker contention).
Memory = peak of Python/NumPy allocations measured with tracemalloc in a SEPARATE pass (tracemalloc slows code, so it never
shares a pass with timing).  Native allocations inside C/Cython code (e.g. tree node arrays, BLAS workspaces) are not traced."""
import time, tracemalloc
from datetime import datetime
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from .config import *
from .data import load_sample
from .features import Space, fit_preprocess, fit_reduce
from .models import make_classifier

SPACES = [Space("orig"), Space("pca", n=10)] + [Space("kpca", k, 10) for k in KERNELS]
REPS = 5


def pipeline_once(Xtr, ytr, Xte, space, code):
    Ztr, Zte, a, b = fit_preprocess(Xtr, Xte); Rtr, Rte, c, d = fit_reduce(Ztr, Zte, space, SEED)
    clf = make_classifier(code, False, SEED)
    t0 = time.perf_counter(); clf.fit(Rtr, ytr); e = time.perf_counter() - t0
    t0 = time.perf_counter(); clf.predict(Rte); f = time.perf_counter() - t0
    return a + c + e, b + d + f, c


def main():
    X, y, classes, _ = load_sample(); tr, te = next(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y))
    rows = []
    for sp in SPACES:
        for code in CLASSIFIERS:
            pipeline_once(X[tr], y[tr], X[te], sp, code)                 # warm-up
            T = np.array([pipeline_once(X[tr], y[tr], X[te], sp, code) for _ in range(REPS)])
            tracemalloc.start(); pipeline_once(X[tr], y[tr], X[te], sp, code); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
            rows.append(dict(space=sp.name, classifier=code, train_time_s=np.median(T[:, 0]), inference_time_s=np.median(T[:, 1]),
                             reducer_fit_s=np.median(T[:, 2]), peak_mem_mb=peak / 2**20, n_train=len(tr), n_test=len(te)))
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pd.DataFrame(rows).to_csv(f"{RAW_DIR}/runtime_{ts}.csv", index=False)
    # Kernel-PCA fit-time scaling in n (quadratic memory/time) vs PCA, on random sub-samples of the standardised data
    from .features import make_reducer
    Z, _, _, _ = fit_preprocess(X, X[:5]); sc = []
    for n in ([400, 800, 1600, 3200, 4800] if RUN == "v2" else [100, 200, 400, 600, 800, 1000]):
        idx = np.random.RandomState(0).choice(len(Z), n, replace=False)
        for sp in [Space("pca", n=10), Space("kpca", "rbf", 10)]:
            ts_ = []
            for _ in range(REPS):
                t0 = time.perf_counter(); make_reducer(sp, SEED).fit(Z[idx]); ts_.append(time.perf_counter() - t0)
            tracemalloc.start(); make_reducer(sp, SEED).fit(Z[idx]); pk = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
            sc.append(dict(n=n, method=sp.name, fit_time_s=np.median(ts_), peak_mem_mb=pk / 2**20))
    pd.DataFrame(sc).to_csv(f"{RAW_DIR}/kpca_scaling_{ts}.csv", index=False); print("done")


if __name__ == "__main__":
    main()
