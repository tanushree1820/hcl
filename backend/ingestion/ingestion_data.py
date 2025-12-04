"""
Module: data_ingestion.py
Combines footfall, sales, and loyalty datasets into a single processed DataFrame.
"""
import pandas as pd
from backend.ingestion.football_data import load_footfall_data
from backend.ingestion.sales_data import load_sales_data
from backend.ingestion.loyalty_data import load_loyalty_data
from backend.utils.data_loader import save_data

def combine_data(footfall_df: pd.DataFrame, sales_df: pd.DataFrame, loyalty_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge footfall, sales, and loyalty DataFrames on ['date','store_id'].
    Fills missing values with 0 (e.g., if a day had footfall but no sales or vice versa).
    Returns a combined DataFrame with columns: ['date', 'store_id', 'footfall', 'sales', 'loyalty_signups'].
    """
    # Merge datasets incrementally
    data = pd.merge(footfall_df, sales_df, on=['date', 'store_id'], how='outer')
    data = pd.merge(data, loyalty_df, on=['date', 'store_id'], how='outer')
    # Fill missing numeric values with 0 (assuming no data means zero sales/footfall/signups for that day/store)
    data['footfall'] = data['footfall'].fillna(0).astype(int)
    data['sales'] = data['sales'].fillna(0).astype(int)
    data['loyalty_signups'] = data['loyalty_signups'].fillna(0).astype(int)
    # Sort combined data by date and store_id
    data = data.sort_values(['date', 'store_id']).reset_index(drop=True)
    return data

def run_ingestion(raw_data_dir: str = "data/raw", output_dir: str = "data/processed") -> pd.DataFrame:
    """
    Load all raw datasets, combine them, and save the processed combined dataset as a CSV.
    Returns the combined DataFrame.
    """
    # Define file paths
    footfall_file = f"{raw_data_dir}/footfall.csv"
    sales_file = f"{raw_data_dir}/sales.csv"
    loyalty_file = f"{raw_data_dir}/loyalty.csv"
    # Load each dataset
    footfall_df = load_footfall_data(footfall_file)
    sales_df = load_sales_data(sales_file)
    loyalty_df = load_loyalty_data(loyalty_file)
    # Combine datasets
    combined_df = combine_data(footfall_df, sales_df, loyalty_df)
    # Save to processed CSV for record or downstream use
    output_path = f"{output_dir}/combined_data.csv"
    save_data(combined_df, output_path)
    return combined_df

# If run as a script, perform the ingestion and output the processed data
if __name__ == "__main__":
    combined = run_ingestion()
    print(f"Data ingestion complete. Combined data shape: {combined.shape}")
