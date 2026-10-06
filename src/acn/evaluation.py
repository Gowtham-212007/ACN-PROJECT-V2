"""All metrics. Macro-F1 is the PRIMARY model-selection criterion (class-aware)."""
import numpy as np
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score,
                             matthews_corrcoef, precision_recall_fscore_support, precision_score, recall_score)


def metrics(y_true, y_pred, n_classes):
    lab = np.arange(n_classes)
    return dict(
        accuracy=accuracy_score(y_true, y_pred),
        precision_macro=precision_score(y_true, y_pred, labels=lab, average="macro", zero_division=0),
        recall_macro=recall_score(y_true, y_pred, labels=lab, average="macro", zero_division=0),
        f1_macro=f1_score(y_true, y_pred, labels=lab, average="macro", zero_division=0),
        f1_weighted=f1_score(y_true, y_pred, labels=lab, average="weighted", zero_division=0),
        balanced_accuracy=balanced_accuracy_score(y_true, y_pred),
        mcc=matthews_corrcoef(y_true, y_pred))


def per_class(y_true, y_pred, classes):
    lab = np.arange(len(classes))
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=lab, zero_division=0)
    return [dict(cls=classes[i], precision=p[i], recall=r[i], f1=f[i], support=int(s[i])) for i in lab]


def cm(y_true, y_pred, n_classes):
    return confusion_matrix(y_true, y_pred, labels=np.arange(n_classes))
