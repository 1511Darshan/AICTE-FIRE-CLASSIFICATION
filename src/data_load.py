"""
src/data_load.py

Data loading and I/O utilities for MODIS fire data.
Handles reading, concatenating, and basic validation of CSV files.
"""

import os
from typing import Optional

import pandas as pd


def load_modis_csv(filepath: str) -> pd.DataFrame:
    """
    Load a single MODIS CSV file.

    Parameters
    ----------
    filepath : str
        Path to MODIS CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded MODIS data.

    Raises
    ------
    FileNotFoundError
        If file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)
    return df


def load_modis_batch(
    directory: str, pattern: str = "modis_*.csv"
) -> pd.DataFrame:
    """
    Load and concatenate multiple MODIS CSV files from a directory.

    Parameters
    ----------
    directory : str
        Directory containing MODIS CSV files.
    pattern : str, optional
        Glob pattern for file matching (default: "modis_*.csv").

    Returns
    -------
    pd.DataFrame
        Concatenated MODIS data from all matching files.

    Notes
    -----
    Resets index after concatenation.
    """
    import glob

    files = sorted(glob.glob(os.path.join(directory, pattern)))

    if not files:
        raise FileNotFoundError(
            f"No files matching '{pattern}' found in {directory}"
        )

    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    return df


def save_modis_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Save MODIS dataframe to CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Data to save.
    filepath : str
        Output file path.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"✓ Saved {len(df)} records to {filepath}")


def validate_columns(df: pd.DataFrame, required_cols: Optional[list] = None) -> bool:
    """
    Validate that required columns are present in the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate.
    required_cols : list, optional
        List of required column names. If None, uses MODIS standard columns.

    Returns
    -------
    bool
        True if all required columns present, False otherwise.
    """
    if required_cols is None:
        required_cols = [
            "latitude",
            "longitude",
            "brightness",
            "frp",
            "confidence",
            "type",
        ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        print(f"⚠ Missing columns: {missing}")
        return False

    return True


def basic_stats(df: pd.DataFrame) -> None:
    """
    Print basic statistics about the MODIS dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze.
    """
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nFire type distribution:\n{df['type'].value_counts().sort_index()}")
    print(f"\nConfidence statistics:\n{df['confidence'].describe()}")
