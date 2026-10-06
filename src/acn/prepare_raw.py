"""Build an analysis-ready .npz from the RAW CIC-IDS2017 MachineLearningCSV files.
Leakage control:
  * NO imputation here: NaN (and +-inf -> NaN) are stored as-is; the CV pipeline imputes (mean) and scales inside each TRAINING fold.
  * Sampling uses only the labels (class allocation) and random numbers - no data-dependent statistic is computed from features.
  * Exact duplicate rows (all 78 features + label) are removed from the pool BEFORE sampling (--dedupe, default on), because
    identical flows landing in both training and test folds would inflate scores.  --no-dedupe reproduces the raw pool (sensitivity run).
Sampling: per class, allocation = min(count, min_per_class) + proportional share of the remainder (preserves real class prevalence);
    rows are drawn uniformly at random without replacement (seed).  The attack-class floor means rare classes are over-represented vs prevalence.
Keeps `day` (source-file index, files sorted by name) and `order` (row position inside the file BEFORE de-duplication); the raw files have no
    usable Timestamp column, row order is used for chronological splits (order is assumed, not proven, to follow capture time).
Writes <out>.npz and <out>.manifest.json (full provenance).
  python -m src.acn.prepare_raw /path/MachineLearningCVE --n 6000 --min-per-class 30 --out data/sample_raw6000.npz
"""
import argparse, glob, json, os, re
import numpy as np, pandas as pd

ap = argparse.ArgumentParser(); ap.add_argument("csv_dir"); ap.add_argument("--n", type=int, default=6000); ap.add_argument("--min-per-class", type=int, default=30)
ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", default="data/sample_raw.npz"); ap.add_argument("--files", nargs="*", default=None)
ap.add_argument("--dedupe", action=argparse.BooleanOptionalAction, default=True)
a = ap.parse_args()
files = a.files or sorted(os.path.basename(f) for f in glob.glob(os.path.join(a.csv_dir, "*.csv")))
def load_file(f):
    df = pd.read_csv(os.path.join(a.csv_dir, f), low_memory=False, encoding="latin-1"); df.columns = df.columns.str.strip()
    lab = [c for c in df.columns if c.lower() == "label"][0]; fe = [c for c in df.columns if c != lab]
    X = df[fe].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).astype(np.float64)
    y = df[lab].astype(str).str.strip().str.replace(r"^Web Attack.*?(Brute Force|XSS|Sql Injection)$", r"Web Attack - \1", regex=True)
    return X, y.to_numpy(), fe

# pass 1 (memory-light): labels, positions and 64-bit row hashes only
ys, days, orders, hf, hl, feat = [], [], [], [], [], None
for d, f in enumerate(files):
    X, y_, fe = load_file(f); feat = feat or fe; assert fe == feat, f"column mismatch in {f}"
    h = pd.util.hash_pandas_object(X, index=False).to_numpy(np.uint64); hf.append(h)
    hl.append(h * np.uint64(1000003) + pd.util.hash_array(y_.astype(object)).astype(np.uint64))   # features + label
    ys.append(y_); days.append(np.full(len(X), d)); orders.append(np.arange(len(X))); del X
y_raw = np.concatenate(ys); day = np.concatenate(days); order = np.concatenate(orders); hf = np.concatenate(hf); hl = np.concatenate(hl)
n_raw = len(y_raw); classes, y = np.unique(y_raw, return_inverse=True)
man = dict(n_raw_rows=int(n_raw), files=files, raw_counts={c: int(n) for c, n in zip(classes, np.bincount(y))}, dedupe=a.dedupe)
keep = np.ones(n_raw, bool)
if a.dedupe:
    dup = pd.Series(hl).duplicated(keep="first").to_numpy(); keep = ~dup; man["n_duplicates_removed"] = int(dup.sum())
    man["rows_in_feature_duplicate_groups_total"] = int(pd.Series(hf).duplicated(keep=False).sum())
    man["feature_duplicate_groups_with_conflicting_labels"] = int((pd.DataFrame({"h": hf, "y": y}).drop_duplicates().groupby("h").size() > 1).sum())
pool = np.where(keep)[0]; yp = y[pool]; counts = np.bincount(yp, minlength=len(classes))
man["pool_counts"] = {c: int(n) for c, n in zip(classes, counts)}; man["n_pool"] = int(len(pool))
rng = np.random.RandomState(a.seed)
alloc = np.minimum(counts, a.min_per_class); rest = a.n - alloc.sum()
alloc = np.minimum(counts, alloc + np.round(rest * counts / counts.sum()).astype(int))
alloc[np.argmax(counts)] += a.n - alloc.sum()             # round-off top-up on the majority class
idx = np.concatenate([pool[rng.choice(np.where(yp == c)[0], alloc[c], replace=False)] for c in range(len(classes))]); rng.shuffle(idx)
# pass 2: extract only the sampled rows
Xs = np.full((len(idx), len(feat)), np.nan); pos = {g: i for i, g in enumerate(idx)}; off = 0
for d, f in enumerate(files):
    X, _, _ = load_file(f); n = len(X); sel = idx[(idx >= off) & (idx < off + n)]
    Xs[[pos[g] for g in sel]] = X.to_numpy()[sel - off]; off += n; del X
man.update(n_sample=int(len(idx)), seed=a.seed, min_per_class=a.min_per_class, sample_counts={c: int(n) for c, n in zip(classes, np.bincount(y[idx], minlength=len(classes)))},
           nan_cells_in_sample=int(np.isnan(Xs).sum()), n_features=len(feat))
np.savez_compressed(a.out, X=Xs, y=y[idx], classes=classes, day=day[idx], order=order[idx], features=np.array(feat), files=np.array(files))
json.dump(man, open(a.out.replace(".npz", ".manifest.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in man.items() if k not in ("files",)}, indent=1))
