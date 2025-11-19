"""
src/features.py

Feature engineering and selection for MODIS fire classification.
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.preprocessing import StandardScaler


def engineer_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract temporal features from acq_date and acq_time.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'acq_date' and 'acq_time' columns.

    Returns
    -------
    pd.DataFrame
        Data with new temporal features:
        - month, day_of_year, day_of_week, hour, is_night

    Notes
    -----
    Assumes acq_time is in HHMM format (string or int).
    """
    df = df.copy()

    if "acq_date" in df.columns:
        df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")
        df["month"] = df["acq_date"].dt.month
        df["day_of_year"] = df["acq_date"].dt.dayofyear
        df["day_of_week"] = df["acq_date"].dt.dayofweek

    if "acq_time" in df.columns:
        # Convert HHMM to hour
        df["hour"] = (df["acq_time"] // 100).astype(int)
        # Mark night-time fires (21:00–05:00)
        df["is_night"] = ((df["hour"] >= 21) | (df["hour"] < 5)).astype(int)

    return df


def engineer_thermal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create thermal signature features from brightness channels.

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'brightness' and 'brightness_t31' columns.

    Returns
    -------
    pd.DataFrame
        Data with new thermal features:
        - brightness_diff: brightness - brightness_t31
        - brightness_ratio: brightness / brightness_t31
        - thermal_anomaly: normalized brightness
    """
    df = df.copy()

    if "brightness" in df.columns and "brightness_t31" in df.columns:
        # Temperature difference (fire signature)
        df["brightness_diff"] = df["brightness"] - df["brightness_t31"]

        # Ratio (avoids division by zero)
        df["brightness_ratio"] = np.where(
            df["brightness_t31"] > 0,
            df["brightness"] / df["brightness_t31"],
            0,
        )

        # Normalized brightness (0–1)
        brightness_min = df["brightness"].min()
        brightness_max = df["brightness"].max()
        if brightness_max > brightness_min:
            df["thermal_anomaly"] = (
                df["brightness"] - brightness_min
            ) / (brightness_max - brightness_min)

    return df


def engineer_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create spatial features (distance-based, clustering).

    Parameters
    ----------
    df : pd.DataFrame
        Data with 'latitude' and 'longitude' columns.

    Returns
    -------
    pd.DataFrame
        Data with spatial features:
        - lat_bins, lon_bins: Spatial coarse binning
    """
    df = df.copy()

    if "latitude" in df.columns:
        # Coarse latitude binning (every ~2 degrees)
        df["lat_bin"] = pd.cut(df["latitude"], bins=15, labels=False)

    if "longitude" in df.columns:
        # Coarse longitude binning
        df["lon_bin"] = pd.cut(df["longitude"], bins=15, labels=False)

    return df


def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all feature engineering steps.

    Parameters
    ----------
    df : pd.DataFrame
        Raw MODIS data.

    Returns
    -------
    pd.DataFrame
        Data with all engineered features.
    """
    print("=" * 60)
    print("Engineering features...")
    print("=" * 60)

    df = engineer_temporal_features(df)
    print("✓ Temporal features created")

    df = engineer_thermal_features(df)
    print("✓ Thermal features created")

    df = engineer_spatial_features(df)
    print("✓ Spatial features created")

    print("=" * 60)
    print(f"Feature engineering complete: {df.shape[1]} total columns")
    print("=" * 60)

    return df


def select_best_features(
    X: pd.DataFrame,
    y: pd.Series,
    k: int = 10,
    method: str = "f_classif",
) -> tuple:
    """
    Select top K features using feature selection methods.

    Parameters
    ----------
    X : pd.DataFrame
        Features.
    y : pd.Series
        Target.
    k : int, optional
        Number of features to select (default: 10).
    method : str, optional
        Method: "f_classif" or "mutual_info" (default: "f_classif").

    Returns
    -------
    tuple
        (selected_features_list, selector_object)

    Notes
    -----
    Assumes X is already numeric and scaled.
    """
    if method == "f_classif":
        selector = SelectKBest(score_func=f_classif, k=min(k, X.shape[1]))
    elif method == "mutual_info":
        selector = SelectKBest(
            score_func=mutual_info_classif, k=min(k, X.shape[1])
        )
    else:
        raise ValueError(f"Unknown method: {method}")

    selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()].tolist()

    return selected_features, selector


def scale_features(X: pd.DataFrame, fit=True, scaler=None) -> tuple:
    """
    Scale features using StandardScaler.

    Parameters
    ----------
    X : pd.DataFrame
        Features to scale.
    fit : bool, optional
        If True, fit scaler on data (default: True).
    scaler : StandardScaler, optional
        Pre-fitted scaler (if fit=False).

    Returns
    -------
    tuple
        (scaled_data, scaler)
    """
    if scaler is None:
        scaler = StandardScaler()

    if fit:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)

    return pd.DataFrame(X_scaled, columns=X.columns, index=X.index), scaler
