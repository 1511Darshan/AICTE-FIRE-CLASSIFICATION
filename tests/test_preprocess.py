"""
tests/test_preprocess.py

Unit tests for preprocessing functions.
"""

import numpy as np
import pandas as pd
import pytest

from src.preprocess import (
    clean_modis_data,
    convert_dtypes,
    handle_missing_values,
    remove_outliers,
)


@pytest.fixture
def sample_data():
    """Create a sample MODIS dataset for testing."""
    return pd.DataFrame(
        {
            "latitude": [10.0, 20.0, 30.0, 40.0, 50.0],
            "longitude": [60.0, 70.0, 80.0, 90.0, 95.0],
            "brightness": [310, 320, 330, 340, 350],
            "brightness_t31": [290, 295, 300, 305, 310],
            "frp": [10.0, 20.0, 30.0, 100.0, 500.0],  # Last one is outlier
            "confidence": [50, 75, 80, 90, 99],
            "type": [0, 1, 0, 2, 3],
        }
    )


def test_clean_modis_data(sample_data):
    """Test cleaning by confidence threshold."""
    df_clean = clean_modis_data(sample_data, confidence_threshold=75)
    
    # Should remove rows with confidence < 75
    assert len(df_clean) == 4
    assert (df_clean["confidence"] >= 75).all()


def test_convert_dtypes(sample_data):
    """Test data type conversion."""
    # Convert to string (worst case)
    df_str = sample_data.astype(str)
    
    df_converted = convert_dtypes(df_str)
    
    # Check numeric columns are numeric
    assert pd.api.types.is_numeric_dtype(df_converted["brightness"])
    assert pd.api.types.is_numeric_dtype(df_converted["frp"])
    assert pd.api.types.is_integer_dtype(df_converted["type"])


def test_handle_missing_values(sample_data):
    """Test handling of missing values."""
    # Introduce missing values
    df_missing = sample_data.copy()
    df_missing.loc[0, "frp"] = np.nan
    df_missing.loc[1, "brightness"] = np.nan
    
    # Drop strategy
    df_dropped = handle_missing_values(df_missing, strategy="drop")
    assert len(df_dropped) == 3  # 5 - 2
    
    # Mean strategy
    df_imputed = handle_missing_values(df_missing, strategy="mean")
    assert not df_imputed.isna().any().any()


def test_remove_outliers_iqr(sample_data):
    """Test outlier removal using IQR method."""
    df_clean = remove_outliers(sample_data, column="frp", method="iqr", threshold=1.5)
    
    # FRP = 500 should be removed (outlier)
    assert len(df_clean) == 4
    assert df_clean["frp"].max() < 100  # Max FRP is now 30


def test_remove_outliers_zscore(sample_data):
    """Test outlier removal using z-score method."""
    df_clean = remove_outliers(sample_data, column="frp", method="zscore", threshold=2.0)
    
    # FRP = 500 should be removed
    assert len(df_clean) <= 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
