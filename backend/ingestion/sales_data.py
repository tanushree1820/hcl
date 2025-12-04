"""
Module: sales_data.py
Functions to ingest and preprocess sales transaction data.
"""
import pandas as pd

def load_sales_data(csv_path: str) -> pd.DataFrame:
    """
    Load sales data from a CSV file.
    Parses 'date' as datetime. Expects columns: ['date', 'store_id', 'sales'] where 'sales' is number of transactions.
    Returns a DataFrame sorted by date (and store).
    """
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df = df.sort_values(['date', 'store_id']).reset_index(drop=True)
    # Fill or clean data as needed (e.g., ensure sales are non-negative integers)
    return df
