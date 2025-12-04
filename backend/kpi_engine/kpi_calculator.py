"""
Module: kpi_calculator.py
Defines functions to calculate key performance indicators (KPIs) such as conversion rate and loyalty signup rate.
"""
import pandas as pd

def add_kpi_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add KPI columns to the dataset in-place:
      - conversion_rate: percentage of visitors who made a purchase (sales/footfall * 100).
      - loyalty_rate: percentage of visitors who signed up for loyalty program (loyalty_signups/footfall * 100).
    Returns the DataFrame with new columns.
    """
    # To avoid division by zero, handle cases where footfall is 0
    data['conversion_rate'] = 0.0
    data['loyalty_rate'] = 0.0
    mask_footfall = data['footfall'] > 0
    data.loc[mask_footfall, 'conversion_rate'] = data.loc[mask_footfall, 'sales'] / data.loc[mask_footfall, 'footfall'] * 100.0
    data.loc[mask_footfall, 'loyalty_rate'] = data.loc[mask_footfall, 'loyalty_signups'] / data.loc[mask_footfall, 'footfall'] * 100.0
    return data

def get_summary_kpis(data: pd.DataFrame) -> dict:
    """
    Compute aggregate summary KPIs for a given dataset (e.g., one store or filtered timeframe):
      - total_footfall
      - total_sales
      - overall_conversion_rate (overall sales/footfall *100)
      - overall_loyalty_rate (overall loyalty_signups/footfall *100)
    Returns a dictionary of summary metrics.
    """
    total_visitors = int(data['footfall'].sum())
    total_sales = int(data['sales'].sum())
    total_signups = int(data['loyalty_signups'].sum())
    overall_conv = (total_sales / total_visitors * 100.0) if total_visitors > 0 else 0.0
    overall_loyalty = (total_signups / total_visitors * 100.0) if total_visitors > 0 else 0.0
    return {
        "total_footfall": total_visitors,
        "total_sales": total_sales,
        "conversion_rate": overall_conv,
        "loyalty_rate": overall_loyalty
    }
