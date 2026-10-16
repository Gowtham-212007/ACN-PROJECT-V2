"""Data loading. The cached sample stores already-numeric features; see reports/RESEARCH_AUDIT.md for its limits."""
import numpy as np
from .config import SAMPLE_NPZ


def load_sample(path=SAMPLE_NPZ):
    d = np.load(path, allow_pickle=True)
    X, y = d["X"].astype(float), d["y"].astype(int)
    classes = [str(c).replace("�", "-") for c in d["classes"]]   # repair mangled en-dash in web-attack labels
    meta = {k: d[k] for k in d.files if k not in ("X", "y", "classes")}   # e.g. 'day', 'order' for raw-derived files
    return X, y, classes, meta


def class_table(y, classes):
    n = np.bincount(y, minlength=len(classes))
    return [(classes[i], int(n[i]), 100.0 * n[i] / n.sum()) for i in range(len(classes))]
