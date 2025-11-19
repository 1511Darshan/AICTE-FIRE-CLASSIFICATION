"""
src/train.py

Model training, hyperparameter tuning, and validation.
"""

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from xgboost import XGBClassifier


def train_logistic_regression(X_train, y_train, random_state: int = 42):
    """
    Train a Logistic Regression model.

    Parameters
    ----------
    X_train : array-like
        Training features.
    y_train : array-like
        Training labels.
    random_state : int, optional
        Random seed (default: 42).

    Returns
    -------
    LogisticRegression
        Fitted model.
    """
    model = LogisticRegression(
        max_iter=1000, random_state=random_state, multi_class="multinomial"
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train, random_state: int = 42, n_estimators: int = 100):
    """
    Train a Random Forest model.

    Parameters
    ----------
    X_train : array-like
        Training features.
    y_train : array-like
        Training labels.
    random_state : int, optional
        Random seed (default: 42).
    n_estimators : int, optional
        Number of trees (default: 100).

    Returns
    -------
    RandomForestClassifier
        Fitted model.
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        max_depth=15,
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train, random_state: int = 42, n_estimators: int = 100):
    """
    Train an XGBoost model.

    Parameters
    ----------
    X_train : array-like
        Training features.
    y_train : array-like
        Training labels.
    random_state : int, optional
        Random seed (default: 42).
    n_estimators : int, optional
        Number of boosting rounds (default: 100).

    Returns
    -------
    XGBClassifier
        Fitted model.
    """
    model = XGBClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        max_depth=6,
        learning_rate=0.1,
        verbosity=0,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, model_name: str = "Model"):
    """
    Evaluate model performance.

    Parameters
    ----------
    model : fitted model
        Trained model.
    X_test : array-like
        Test features.
    y_test : array-like
        Test labels.
    model_name : str, optional
        Name of model for display (default: "Model").

    Returns
    -------
    dict
        Metrics dictionary.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

    print(f"\n{'=' * 60}")
    print(f"Model: {model_name}")
    print(f"{'=' * 60}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"F1 (macro): {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    return {"accuracy": accuracy, "f1": f1, "predictions": y_pred}


def cross_validate_model(model, X, y, cv: int = 5):
    """
    Perform cross-validation on a model.

    Parameters
    ----------
    model : unfitted model
        Model to validate.
    X : array-like
        Features.
    y : array-like
        Labels.
    cv : int, optional
        Number of folds (default: 5).

    Returns
    -------
    dict
        Cross-validation scores.
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print(f"Cross-validation scores: {scores}")
    print(f"Mean CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

    return {"scores": scores, "mean": scores.mean(), "std": scores.std()}
