import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Ensure project root is on sys.path so `backend` imports resolve when running from `dashboard/`.

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from backend.kpi_engine import kpi_calculator, forecaster
from backend.ingestion import ingestion_data
# Set page config (optional)
st.set_page_config(page_title="Store Footfall & Conversion Analyzer", layout="wide")

# Title
st.title("Store Footfall & Sales Conversion Analyzer")

# Ingest and load data
# (If data is already processed, we could directly read combined_data.csv. Here we run ingestion each time for simplicity.)
with st.spinner("Loading data..."):
    combined_df = ingestion_data.run_ingestion()

# Compute KPI columns
combined_df = kpi_calculator.add_kpi_columns(combined_df)

# Sidebar filters
st.sidebar.header("Filters")
# Store selection filter
stores = list(combined_df['store_id'].unique())
stores.sort()
store_option = st.sidebar.selectbox("Select Store", options=["All Stores"] + stores)
# Date range filter (optional: for demo we can use full range)
min_date = combined_df['date'].min()
max_date = combined_df['date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter data based on selections
df_filtered = combined_df.copy()
# Filter by store
if store_option and store_option != "All Stores":
    df_filtered = df_filtered[df_filtered['store_id'] == store_option]
# Filter by date range
if isinstance(date_range, list) or isinstance(date_range, tuple):
    start_date, end_date = date_range[0], date_range[1]
else:
    start_date, end_date = min_date, max_date
df_filtered = df_filtered[(df_filtered['date'] >= pd.to_datetime(start_date)) & 
                           (df_filtered['date'] <= pd.to_datetime(end_date))]

# Compute summary KPIs for the filtered data
summary = kpi_calculator.get_summary_kpis(df_filtered)

# Display top-level KPIs
st.subheader("Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Footfall", f"{summary['total_footfall']}")
col2.metric("Total Sales", f"{summary['total_sales']}")
col3.metric("Conversion Rate", f"{summary['conversion_rate']:.1f}%")
col4.metric("Loyalty Signup Rate", f"{summary['loyalty_rate']:.2f}%")

# Line charts for footfall and sales over time
st.subheader(f"Footfall and Sales Over Time — {store_option}")
# Prepare time series for plotting
ts_data = df_filtered.sort_values('date').set_index('date')
# Plot footfall vs sales
st.line_chart(ts_data[['footfall', 'sales']])

# Line chart for conversion rate over time
st.subheader(f"Conversion Rate Over Time — {store_option}")
st.line_chart(ts_data['conversion_rate'])

# Loyalty signups over time (optional additional chart)
st.subheader(f"Loyalty Sign-ups Over Time — {store_option}")
st.line_chart(ts_data['loyalty_signups'])

# Footfall Forecasting
st.subheader(f"Footfall Forecast (Next 7 Days) — {store_option}")
# Allow user to adjust forecast horizon
horizon = st.slider("Forecast horizon (days)", min_value=3, max_value=30, value=7)
# Generate forecast for the selected store (or all stores)
if store_option == "All Stores":
    forecast_series = forecaster.forecast_footfall(combined_df, store_id=None, periods=horizon)
else:
    forecast_series = forecaster.forecast_footfall(combined_df, store_id=store_option, periods=horizon)
# Combine recent actual data with forecast for plotting
if not forecast_series.empty:
    # Take the last week of actual footfall for continuity in chart
    recent_actual = df_filtered.set_index('date')['footfall'].dropna()
    if not recent_actual.empty:
        last_date = recent_actual.index.max()
    else:
        last_date = combined_df['date'].max()
        recent_actual = combined_df[combined_df['date'] <= last_date].set_index('date')['footfall']
    # Use last 7 days of actual for context (or fewer if not available)
    recent_actual = recent_actual.sort_index().last('7D')
    # Create a DataFrame to hold both actual and forecast
    forecast_df = pd.DataFrame({
        "Actual Footfall": recent_actual.reset_index(drop=True),
        "Forecast Footfall": forecast_series.reset_index(drop=True),
    })

    # forecast_df = pd.DataFrame({
    #     "Actual Footfall": recent_actual,
    #     "Forecast Footfall": forecast_series
    # })
    st.line_chart(forecast_df)
else:
    st.write("Forecast not available (insufficient data or model issue).")

st.write("*Note: Forecast is generated using a simple ARIMA model for demonstration purposes.*")
