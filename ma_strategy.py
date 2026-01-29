"""
Moving Average Strategy Module
Implements moving average crossover strategy logic
"""

import pandas as pd
from itertools import product


def generate_ma_combinations(step_size):
    """
    Generate all valid moving average combinations.
    Lower MA ranges from step_size to 50.
    Higher MA ranges from step_size to 200.
    Ensures lower_ma < higher_ma always.
    Returns: list of tuples (lower_ma, higher_ma)
    """
    lower_ma_range = range(step_size, 51, step_size)
    higher_ma_range = range(step_size, 201, step_size)
    
    combinations = []
    for lower, higher in product(lower_ma_range, higher_ma_range):
        if lower < higher:  # Ensure lower MA is always less than higher MA
            combinations.append((lower, higher))
    
    print(f"Generated {len(combinations)} MA combinations")
    return combinations


def calculate_moving_averages(prices, lower_period, higher_period):
    """
    Calculate two moving averages for the given periods.
    Returns: DataFrame with both MAs
    """
    ma_data = pd.DataFrame(index=prices.index)
    ma_data['Price'] = prices
    ma_data['MA_Lower'] = prices.rolling(window=lower_period).mean()
    ma_data['MA_Higher'] = prices.rolling(window=higher_period).mean()
    
    return ma_data


def generate_trading_signals(ma_data):
    """
    Generate buy/sell signals based on moving average crossover.
    Buy when lower MA crosses above higher MA (Golden Cross).
    Sell when lower MA crosses below higher MA (Death Cross).
    Returns: DataFrame with signals
    """
    signals = ma_data.copy()
    
    # 1 when lower MA > higher MA (bullish), 0 otherwise
    signals['Position'] = 0
    signals.loc[signals['MA_Lower'] > signals['MA_Higher'], 'Position'] = 1
    
    # Generate trading signals: 1 for buy, -1 for sell, 0 for hold
    signals['Signal'] = signals['Position'].diff()
    
    return signals