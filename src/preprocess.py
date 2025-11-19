"""
src/preprocess.py

Data preprocessing and cleaning for MODIS fire data.
Handles missing values, outliers, type casting, and feature engineering.
"""

import pandas as pd
import numpy as np


def clean_modis_data(df: pd.DataFrame, confidence_threshold: int = 50) -> pd.DataFrame:
    """
    Clean MODIS data by filtering low-confidence detections and removing duplicates.

    Parameters
    ----------
    df : pd.DataFrame
        Raw MODIS data.
    confidence_threshold : int, optional
        Minimum confidence level (0–100) to retain (default: 50).

    Returns
    -------
    pd.DataFrame
        Cleaned data.

    Notes
    -----
    - Removes duplicates
    - Filters by confidence threshold
    - Resets index
    """
    # Remove duplicates
    df = df.drop_duplicates()

    # Filter by confidence
    initial_count = len(df)
    df = df[df["confidence"] >= confidence_threshold]
    removed = initial_count - len(df)
    print(f"✓ Removed {removed} records with confidence < {confidence_threshold}")

    # Reset index
    df = df.reset_index(drop=True)

    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Data with potential missing values.
    strategy : str, optional
        Strategy: "drop" (remove rows), "mean" (impute with mean), etc.
        Default: "drop".

    Returns
    -------
    pd.DataFrame
        Data with missing values handled.
    """
    initial_count = len(df)

    if strategy == "drop":
        df = df.dropna()
    elif strategy == "mean":
        df = df.fillna(df.mean(numeric_only=True))
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    removed = initial_count - len(df)
    if removed > 0:
        print(f"✓ Handled {removed} rows with missing values ({strategy})")

    return df.reset_index(drop=True)


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert data types to appropriate formats.

    Parameters
    ----------
    df : pd.DataFrame
        Raw data.

    Returns
    -------
    pd.DataFrame
        Data with corrected types.
    """
    # Numeric columns
    numeric_cols = [
        "latitude",
        "longitude",
        "brightness",
        "brightness_t31",
        "frp",
        "confidence",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Integer columns
    int_cols = ["type", "confidence"]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype("int32")

    # Date conversion
    if "acq_date" in df.columns:
        df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")

    return df


def remove_outliers(
    df: pd.DataFrame, column: str, method: str = "iqr", threshold: float = 3.0
) -> pd.DataFrame:
    """
    Remove outliers from a numeric column.

    Parameters
    ----------
    df : pd.DataFrame
        Data.
    column : str
        Column name to filter.
    method : str, optional
        Method: "iqr" (interquartile range) or "zscore" (z-score).
        Default: "iqr".
    threshold : float, optional
        IQR multiplier (for method='iqr') or z-score threshold (default: 3.0).

    Returns
    -------
    pd.DataFrame
        Data without outliers.
    """
    initial_count = len(df)

    if method == "iqr":
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        df = df[(df[column] >= lower) & (df[column] <= upper)]

    elif method == "zscore":
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        df = df[z_scores < threshold]

    else:
        raise ValueError(f"Unknown method: {method}")

    removed = initial_count - len(df)
    if removed > 0:
        print(f"✓ Removed {removed} outliers from '{column}' ({method})")

    return df.reset_index(drop=True)


def normalize_features(
    df: pd.DataFrame, columns: list, method: str = "minmax"
) -> pd.DataFrame:
    """
    Normalize numeric features.

    Parameters
    ----------
    df : pd.DataFrame
        Data.
    columns : list
        Columns to normalize.
    method : str, optional
        Method: "minmax" (0–1) or "zscore" (mean=0, std=1).
        Default: "minmax".

    Returns
    -------
    pd.DataFrame
        Data with normalized features.
    """
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            continue

        if method == "minmax":
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)

        elif method == "zscore":
            mean_val = df[col].mean()
            std_val = df[col].std()
            if std_val > 0:
                df[col] = (df[col] - mean_val) / std_val
        else:
            raise ValueError(f"Unknown method: {method}")

    return df


def full_preprocessing_pipeline(
    df: pd.DataFrame, confidence_threshold: int = 50
) -> pd.DataFrame:
    """
    Run the full preprocessing pipeline.

    Parameters
    ----------
    df : pd.DataFrame
        Raw MODIS data.
    confidence_threshold : int, optional
        Minimum confidence (default: 50).

    Returns
    -------
    pd.DataFrame
        Fully preprocessed data.

    Notes
    -----
    Steps:
    1. Convert data types
    2. Clean (remove duplicates, filter by confidence)
    3. Handle missing values
    4. Remove outliers (FRP only)
    """
    print("=" * 60)
    print("Running preprocessing pipeline...")
    print("=" * 60)

    df = convert_dtypes(df)
    print("✓ Data types converted")

    df = clean_modis_data(df, confidence_threshold=confidence_threshold)

    df = handle_missing_values(df, strategy="drop")

    # Remove FRP outliers (use IQR method)
    if "frp" in df.columns:
        df = remove_outliers(df, "frp", method="iqr", threshold=3.0)

    print("=" * 60)
    print(f"Preprocessing complete: {len(df)} records retained")
    print("=" * 60)

    return df
