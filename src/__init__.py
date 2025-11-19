"""
src/__init__.py

Package initialization for the fire classification project.
"""

__version__ = "0.1.0"
__author__ = "Darshan"
__description__ = "Classification of Fire Types in India Using MODIS Satellite Data"

# Import key modules for convenience
from . import data_load, preprocess, features, train, evaluate

__all__ = ["data_load", "preprocess", "features", "train", "evaluate"]
