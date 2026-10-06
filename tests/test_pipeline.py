"""Sanity tests: (1) no leakage-by-construction equivalence with sklearn Pipeline, (2) linear Kernel PCA == PCA."""
import numpy as np
from sklearn.decomposition import PCA, KernelPCA
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.acn.data import load_sample
from src.acn.features import Space, fit_preprocess, fit_reduce
from src.acn.models import make_classifier

X, y, classes, _ = load_sample()
tr, te = next(StratifiedKFold(5, shuffle=True, random_state=42).split(X, y))


def test_shared_reducer_equals_sklearn_pipeline():
    for sp, red in [(Space("pca", n=10), PCA(10, random_state=42)),
                    (Space("kpca", "rbf", 10), KernelPCA(10, kernel="rbf", random_state=42))]:
        Ztr, Zte, *_ = fit_preprocess(X[tr], X[te]); Rtr, Rte, *_ = fit_reduce(Ztr, Zte, sp, 42)
        mine = make_classifier("DT", False, 42).fit(Rtr, y[tr]).predict(Rte)
        pipe = make_pipeline(SimpleImputer(), StandardScaler(), red, make_classifier("DT", False, 42)).fit(X[tr], y[tr])
        assert np.array_equal(mine, pipe.predict(X[te])), sp.name


def test_linear_kpca_matches_pca_up_to_sign():
    Ztr, Zte, *_ = fit_preprocess(X[tr], X[te])
    A, B = PCA(10, random_state=0).fit(Ztr).transform(Zte), KernelPCA(10, kernel="linear", random_state=0).fit(Ztr).transform(Zte)
    assert np.allclose(np.abs(A), np.abs(B), atol=1e-6)


def test_test_rows_never_in_train():
    assert not set(tr) & set(te)
