"""Feature spaces: original | PCA | Kernel PCA.  Preprocessing and reducers are fitted on TRAINING data only."""
import time
from dataclasses import dataclass
import numpy as np
from sklearn.decomposition import PCA, KernelPCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from .config import COMPONENTS, KERNELS


@dataclass(frozen=True)
class Space:
    method: str                 # 'orig' | 'pca' | 'kpca'
    kernel: str = ""            # kpca only
    n: int = 0                  # components (0 = all original features)

    @property
    def name(self):
        return "orig" if self.method == "orig" else (f"pca-{self.n}" if self.method == "pca" else f"kpca-{self.kernel}-{self.n}")


def all_spaces():
    s = [Space("orig")] + [Space("pca", n=n) for n in COMPONENTS]
    return s + [Space("kpca", k, n) for k in KERNELS for n in COMPONENTS]


def make_reducer(space, seed):
    if space.method == "pca":
        return PCA(n_components=space.n, random_state=seed)
    if space.method == "kpca":   # gamma = sklearn default 1/n_features (rbf); linear/cosine have no free parameter
        return KernelPCA(n_components=space.n, kernel=space.kernel, eigen_solver="auto", random_state=seed)
    return None


def fit_preprocess(Xtr, Xte):
    """Impute (mean) + standardise. Both fitted on the training fold only. Returns scaled arrays and timings."""
    t0 = time.perf_counter()
    imp = SimpleImputer(strategy="mean").fit(Xtr)
    sc = StandardScaler().fit(imp.transform(Xtr))
    Ztr = sc.transform(imp.transform(Xtr)); t_fit = time.perf_counter() - t0
    t0 = time.perf_counter(); Zte = sc.transform(imp.transform(Xte)); t_tr = time.perf_counter() - t0
    return Ztr, Zte, t_fit, t_tr


def fit_reduce(Ztr, Zte, space, seed):
    """Fit the reducer on training data, transform both. Returns arrays and (fit_time, transform_time)."""
    red = make_reducer(space, seed)
    if red is None:
        return Ztr, Zte, 0.0, 0.0
    t0 = time.perf_counter(); Rtr = red.fit_transform(Ztr); t_fit = time.perf_counter() - t0
    t0 = time.perf_counter(); Rte = red.transform(Zte); t_tr = time.perf_counter() - t0
    return Rtr, Rte, t_fit, t_tr
