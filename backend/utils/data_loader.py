"""
Module: data_loader.py
Utility functions for loading and saving data.
"""
import pandas as pd

def load_data(path: str, parse_dates: list = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame. Optionally parse specified columns as dates.
    """
    return pd.read_csv(path, parse_dates=parse_dates)

def save_data(df: pd.DataFrame, path: str) -> None:
    """
    Save a DataFrame to a CSV file. Index is not saved (index=False).
    """
    df.to_csv(path, index=False)
