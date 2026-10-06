"""Verify raw CIC-IDS2017 (MachineLearningCVE) CSVs: readability, shapes, labels, NaN/inf, constants, duplicates, time info.
  python -m src.acn.profile_raw <csv_dir>   -> results/raw/raw_profile.json, reports/RAW_DATA_PROFILE.md"""
import sys, glob, json, os
import numpy as np, pandas as pd

d = sys.argv[1]; files = sorted(glob.glob(f"{d}/*.csv")); prof = {"files": {}}; cols0 = None; allc = []; const = None
for f in files:
    df = pd.read_csv(f, low_memory=False, encoding="latin1"); df.columns = df.columns.str.strip()
    cols = list(df.columns); cols0 = cols0 or cols
    lab = df.iloc[:, -1].astype(str).str.strip(); X = df.iloc[:, :-1].apply(pd.to_numeric, errors="coerce")
    inf = int(np.isinf(X.to_numpy(dtype=float)).sum()); nan_raw = int(df.iloc[:, :-1].isna().sum().sum()); nan_all = int(X.isna().sum().sum())
    nunique = X.replace([np.inf, -np.inf], np.nan).nunique()
    prof["files"][os.path.basename(f)] = dict(rows=len(df), cols=len(cols), same_columns_as_first=cols == cols0, labels=lab.value_counts().to_dict(),
        inf_values=inf, nan_values_raw=nan_raw, nan_after_numeric_coercion=nan_all, rows_with_nan_or_inf=int((X.replace([np.inf, -np.inf], np.nan).isna().any(axis=1)).sum()),
        exact_duplicate_rows=int(df.duplicated().sum()), constant_features=[c for c in X.columns if nunique[c] <= 1], has_timestamp_col=any("time" in c.lower() for c in cols),
        has_flow_id_or_ip=any(k in c.lower() for c in cols for k in ("flow id", "source ip", "destination ip")),
        negative_values_in_features=int((X < 0).sum().sum()))
    allc.append(set(prof["files"][os.path.basename(f)]["constant_features"]))
    print(os.path.basename(f), prof["files"][os.path.basename(f)]["rows"], flush=True)
prof["columns"] = cols0; prof["n_features"] = len(cols0) - 1; prof["constant_in_all_files"] = sorted(set.intersection(*allc))
tot = {}
for v in prof["files"].values():
    for k, n in v["labels"].items(): tot[k] = tot.get(k, 0) + n
prof["total_rows"] = sum(v["rows"] for v in prof["files"].values()); prof["total_labels"] = dict(sorted(tot.items(), key=lambda kv: -kv[1]))
os.makedirs("results/raw", exist_ok=True); json.dump(prof, open("results/raw/raw_profile.json", "w"), indent=1)
print(json.dumps({k: v for k, v in prof.items() if k != "files"}, indent=1)[:3500])
