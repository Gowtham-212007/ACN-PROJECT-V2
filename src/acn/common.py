"""Shared helpers for table/figure scripts: load newest raw result files and aggregate."""
import glob, json
import numpy as np, pandas as pd
from .config import *


def newest(pattern):
    return sorted(f for f in glob.glob(f"{RAW_DIR}/{pattern}") if "smoke" not in f)[-1]


def load_cv():
    df = pd.read_csv(newest("cv_results_2*.csv"))
    df["space"] = np.where(df.dimensionality_method == "orig", "orig", np.where(df.dimensionality_method == "pca", "pca-" + df.components.astype(str),
                           "kpca-" + df.kernel + "-" + df.components.astype(str)))
    return df


METRICS = ["accuracy", "precision_macro", "recall_macro", "f1_macro", "f1_weighted", "balanced_accuracy", "mcc"]


def agg(df, by):
    g = df.groupby(by)[METRICS + ["train_time", "inference_time"]].agg(["mean", "std"])
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    return g.reset_index()


def pm(m, s, d=3):
    return f"{m:.{d}f}$\\pm${s:.{d}f}"


def best_config(df):
    g = df[df.classifier != "DUMMY"].groupby(["space", "classifier", "class_weight"]).f1_macro.mean().sort_values(ascending=False)
    return g.index[0], g.iloc[0]
