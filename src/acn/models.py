"""Classifier factory. Hyper-parameters are FIXED (identical to the original repo); nothing is tuned on test data."""
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def make_classifier(code, balanced=False, seed=0):
    cw = "balanced" if balanced else None
    if code == "LR":
        return LogisticRegression(max_iter=2000, solver="lbfgs", class_weight=cw, random_state=seed)
    if code == "KNN":
        return KNeighborsClassifier(n_neighbors=5)
    if code == "SVM":
        return SVC(kernel="rbf", C=1.0, gamma="scale", class_weight=cw, random_state=seed)
    if code == "DT":
        return DecisionTreeClassifier(criterion="entropy", class_weight=cw, random_state=seed)
    if code == "RF":
        return RandomForestClassifier(n_estimators=100, class_weight=cw, random_state=seed, n_jobs=1)
    if code == "DUMMY":
        return DummyClassifier(strategy="most_frequent")
    raise ValueError(code)


def hyper_config(clf):
    return {k: v for k, v in clf.get_params().items() if k in
            ("C", "gamma", "kernel", "n_neighbors", "criterion", "n_estimators", "max_iter", "class_weight", "strategy")}
