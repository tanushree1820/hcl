"""
Module: footfall_data.py
Provides functions to ingest and preprocess footfall (visitor count) data.
"""
import pandas as pd

def load_footfall_data(csv_path: str) -> pd.DataFrame:
    """
    Load footfall data from a CSV file.
    Ensures the 'date' column is parsed as datetime and data is sorted by date.
    Returns a DataFrame with columns: ['date', 'store_id', 'footfall'].
    """
    df = pd.read_csv(csv_path, parse_dates=['date'])
    # Ensure proper sorting by date (and store if multiple stores per date)
    df = df.sort_values(['date', 'store_id']).reset_index(drop=True)
    # (Optional) data cleaning could be done here (e.g., handling missing values or outliers)
    return df
