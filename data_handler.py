"""
Data Handling Module
Downloads and processes price data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd


def download_price_data(tickers):
    """
    Download maximum available historical price data from Yahoo Finance.
    Returns: DataFrame with adjusted close prices for all tickers
    """
    print("Downloading price data from Yahoo Finance...")
    
    # Download data with maximum period available
    # period='max' gets all available historical data
    data = yf.download(tickers, period='max', auto_adjust=True)['Close']
    
    # If only one ticker, convert Series to DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])
    
    # Drop rows with any missing values
    data = data.dropna()
    
    print(f"\nData downloaded successfully!")
    print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Total days: {len(data)}")
    print(f"\nFirst few rows:")
    print(data.head())
    
    return data