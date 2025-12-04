"""
Module: forecaster.py
Provides functionality to forecast future footfall (visitor counts) using time-series modeling.
"""
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_footfall(data: pd.DataFrame, store_id: str = None, periods: int = 7) -> pd.Series:
    """
    Forecast future footfall for a given store or overall (if store_id is None) for a specified number of days.
    Uses an ARIMA model on the historical daily footfall data.
    Returns a Pandas Series indexed by future dates with the forecasted footfall values.
    """
    # Filter data for the specified store, or aggregate if no specific store_id given
    if store_id:
        df_store = data[data['store_id'] == store_id].copy()
    else:
        # aggregate footfall across all stores per date
        df_store = data.groupby('date', as_index=False)['footfall'].sum()
    # Ensure data is sorted by date
    df_store = df_store.sort_values('date')
    # Use date as index for time series
    ts = df_store.set_index('date')['footfall']
    # Fit a simple ARIMA model (order can be tuned or selected via auto-ARIMA for real use)
    try:
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
    except Exception as e:
        # If the model fails to fit (e.g., not enough data), return an empty series
        print(f"Forecast model fitting failed: {e}")
        return pd.Series(dtype=float)
    # Forecast the specified number of future periods
    forecast_index = pd.date_range(start=ts.index.max() + pd.Timedelta(days=1), periods=periods, freq='D')
    forecast_series = model_fit.forecast(steps=periods)
    forecast_series.index = forecast_index  # set the index to the future dates
    forecast_series.name = 'forecast_footfall'
    return forecast_series
