"""
src/evaluate.py

Model evaluation, metrics, and result reporting.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_recall_fscore_support,
)


def compute_per_class_metrics(y_true, y_pred, class_names=None):
    """
    Compute precision, recall, and F1 per class.

    Parameters
    ----------
    y_true : array-like
        True labels.
    y_pred : array-like
        Predicted labels.
    class_names : list, optional
        Names of classes (default: None).

    Returns
    -------
    dict
        Per-class metrics.
    """
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, zero_division=0
    )

    if class_names is None:
        class_names = [f"Class {i}" for i in range(len(precision))]

    results = {}
    for i, name in enumerate(class_names):
        results[name] = {
            "precision": precision[i],
            "recall": recall[i],
            "f1": f1[i],
            "support": support[i],
        }

    return results


def confusion_matrix_summary(y_true, y_pred, class_names=None):
    """
    Compute and display confusion matrix.

    Parameters
    ----------
    y_true : array-like
        True labels.
    y_pred : array-like
        Predicted labels.
    class_names : list, optional
        Names of classes.

    Returns
    -------
    pd.DataFrame
        Confusion matrix as DataFrame.
    """
    cm = confusion_matrix(y_true, y_pred)

    if class_names is None:
        class_names = [f"Class {i}" for i in range(cm.shape[0])]

    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)

    return cm_df


def feature_importance_summary(model, feature_names, top_k: int = 10):
    """
    Extract and summarize feature importances.

    Parameters
    ----------
    model : fitted model
        Model with feature_importances_ or coef_ attribute.
    feature_names : list
        Names of features.
    top_k : int, optional
        Number of top features to return (default: 10).

    Returns
    -------
    pd.DataFrame
        Top features ranked by importance.
    """
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        # For linear models, use absolute value of coefficients
        importances = np.abs(model.coef_[0])
    else:
        raise ValueError("Model does not have feature importances or coefficients")

    feature_importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    )
    feature_importance_df = feature_importance_df.sort_values(
        "importance", ascending=False
    )

    return feature_importance_df.head(top_k)


def print_evaluation_report(y_true, y_pred, model_name: str = "Model"):
    """
    Print a comprehensive evaluation report.

    Parameters
    ----------
    y_true : array-like
        True labels.
    y_pred : array-like
        Predicted labels.
    model_name : str, optional
        Name of model (default: "Model").
    """
    print(f"\n{'=' * 70}")
    print(f"Evaluation Report: {model_name}")
    print("=" * 70)

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))

    # Confusion matrix
    cm_df = confusion_matrix_summary(y_true, y_pred)
    print("\nConfusion Matrix:")
    print(cm_df)

    print("=" * 70)
