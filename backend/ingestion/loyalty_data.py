"""
Module: loyalty_data.py
Functions to ingest and preprocess customer loyalty data (e.g., new loyalty sign-ups).
"""
import pandas as pd

def load_loyalty_data(csv_path: str) -> pd.DataFrame:
    """
    Load loyalty data from a CSV file.
    Parses 'date' as datetime. Expects columns: ['date', 'store_id', 'loyalty_signups'].
    Returns a DataFrame sorted by date (and store).
    """
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df = df.sort_values(['date', 'store_id']).reset_index(drop=True)
    # Any necessary cleaning (e.g., handle missing or negative signups) can be done here.
    return df
