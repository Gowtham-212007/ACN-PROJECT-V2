"""Build an analysis-ready .npz from the RAW CIC-IDS2017 MachineLearningCSV files (run this on a machine that has them).
Differences from the original prepare_data.py:
  * NO imputation here - NaN (and inf -> NaN) are kept, the CV pipeline imputes inside each training fold (no leakage).
  * Keeps `day` (source file index) and `order` (original row position inside the file) for chronological splits.
    (Row position is used instead of parsing 'Timestamp': the CSV timestamps have no AM/PM marker and cannot be ordered reliably.)
  * N is configurable (Experiment B: e.g. --n 5000 / 10000; kernel matrix memory grows as n^2 * 8 bytes).
  python -m src.acn.prepare_raw MachineLearningCVE --n 5000 --out data/sample_5000.npz        # NOT executed in the authoring sandbox
"""
import argparse, glob, os
import numpy as np, pandas as pd

ap = argparse.ArgumentParser(); ap.add_argument("csv_dir"); ap.add_argument("--n", type=int, default=5000); ap.add_argument("--min-per-class", type=int, default=10)
ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", default="data/sample_raw.npz"); ap.add_argument("--files", nargs="*", default=None)
a = ap.parse_args()
files = a.files or sorted(os.path.basename(f) for f in glob.glob(os.path.join(a.csv_dir, "*.csv")))
frames = []
for d, f in enumerate(files):
    df = pd.read_csv(os.path.join(a.csv_dir, f), low_memory=False, encoding="latin-1"); df.columns = df.columns.str.strip()
    df["__day"], df["__order"] = d, np.arange(len(df)); frames.append(df)
df = pd.concat(frames, ignore_index=True)
lab = [c for c in df.columns if c.lower() == "label"][0]
feat = [c for c in df.columns if c not in (lab, "__day", "__order")]
X = df[feat].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).to_numpy(float)
y_raw = df[lab].astype(str).str.strip().to_numpy(); classes, y = np.unique(y_raw, return_inverse=True)
counts = np.bincount(y); rng = np.random.RandomState(a.seed)
alloc = np.minimum(counts, a.min_per_class); rest = a.n - alloc.sum()
alloc = np.minimum(counts, alloc + np.round(rest * counts / counts.sum()).astype(int)); alloc[np.argmax(counts)] += a.n - alloc.sum()
idx = np.concatenate([rng.choice(np.where(y == c)[0], alloc[c], replace=False) for c in range(len(classes))]); rng.shuffle(idx)
np.savez_compressed(a.out, X=X[idx], y=y[idx], classes=classes, day=df["__day"].to_numpy()[idx], order=df["__order"].to_numpy()[idx], features=np.array(feat), files=np.array(files))
print(f"saved {a.out}: {len(idx)} rows from {len(df)} flows, {len(feat)} features, {len(classes)} classes"); print(dict(zip(classes, np.bincount(y[idx]))))
