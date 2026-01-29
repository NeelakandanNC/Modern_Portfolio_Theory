"""
Backtesting Module
Tests moving average strategies and calculates performance metrics
"""

import pandas as pd
from ma_strategy import calculate_moving_averages, generate_trading_signals


def backtest_strategy(prices, optimal_weights, lower_ma, higher_ma, risk_free_rate):
    """
    Backtest the moving average strategy on the optimal portfolio.
    On idle days, earns risk-free rate instead of 0.
    Returns: total_return, number_of_trades, idle_days, risk_free_earnings
    """
    # Calculate portfolio value using optimal weights
    portfolio_value = (prices * optimal_weights).sum(axis=1)
    
    # Calculate moving averages on portfolio
    ma_data = calculate_moving_averages(portfolio_value, lower_ma, higher_ma)
    signals = generate_trading_signals(ma_data)
    
    # Drop NaN values from moving average calculation
    signals = signals.dropna()
    
    if len(signals) == 0:
        return 0, 0, 0, 0
    
    # Calculate daily returns
    daily_returns = portfolio_value.pct_change()
    
    # Calculate daily risk-free rate (assuming 252 trading days per year)
    daily_rf_rate = risk_free_rate / 252
    
    # Calculate strategy returns
    # When Position=1 (in market), get actual returns
    # When Position=0 (out of market), get risk-free rate
    strategy_returns = signals['Position'].shift(1) * daily_returns
    risk_free_returns = (1 - signals['Position'].shift(1)) * daily_rf_rate
    
    # Combine returns
    total_daily_returns = strategy_returns + risk_free_returns
    
    # Align indices
    total_daily_returns = total_daily_returns.loc[signals.index]
    
    # Calculate cumulative return
    cumulative_return = (1 + total_daily_returns.fillna(0)).prod() - 1
    
    # Count number of trades (buy or sell signals)
    num_trades = (signals['Signal'] != 0).sum()
    
    # Count idle days (when Position = 0, money sitting out of market)
    idle_days = (signals['Position'] == 0).sum()
    
    # Calculate total risk-free earnings during idle period
    # This is the cumulative return from risk-free rate during idle days
    risk_free_cumulative = (1 + daily_rf_rate) ** idle_days - 1
    
    return cumulative_return, num_trades, idle_days, risk_free_cumulative


def optimize_ma_strategy(prices, optimal_weights, ma_combinations, risk_free_rate, initial_capital):
    """
    Test all MA combinations and find the best performing one.
    Also calculate buy-and-hold return for comparison.
    Returns: best_combination, best_return, results_dataframe, buy_hold_return, best_stats
    """
    print("\nTesting moving average combinations...")
    print("This may take a few minutes...\n")
    
    # Calculate buy-and-hold return
    portfolio_value = (prices * optimal_weights).sum(axis=1)
    buy_hold_return = (portfolio_value.iloc[-1] / portfolio_value.iloc[0]) - 1
    
    results = []
    
    for i, (lower_ma, higher_ma) in enumerate(ma_combinations):
        if (i + 1) % 50 == 0:
            print(f"Tested {i + 1}/{len(ma_combinations)} combinations...")
        
        total_return, num_trades, idle_days, rf_earnings = backtest_strategy(
            prices, optimal_weights, lower_ma, higher_ma, risk_free_rate)
        
        results.append({
            'Lower_MA': lower_ma,
            'Higher_MA': higher_ma,
            'Total_Return': total_return,
            'Num_Trades': num_trades,
            'Idle_Days': idle_days,
            'RF_Earnings_Pct': rf_earnings,
            'Return_Per_Trade': total_return / num_trades if num_trades > 0 else 0
        })
    
    # Convert to DataFrame and sort by total return
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Total_Return', ascending=False)
    
    # Get best combination
    best = results_df.iloc[0]
    
    # Calculate dollar amounts
    buy_hold_final = initial_capital * (1 + buy_hold_return)
    ma_strategy_final = initial_capital * (1 + best['Total_Return'])
    rf_earnings_dollars = initial_capital * best['RF_Earnings_Pct']
    
    print("\n" + "=" * 60)
    print("BUY-AND-HOLD STRATEGY")
    print("=" * 60)
    print(f"Total Return: {buy_hold_return*100:.2f}%")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Value: ${buy_hold_final:,.2f}")
    print(f"Profit: ${buy_hold_final - initial_capital:,.2f}")
    print("=" * 60 + "\n")
    
    print("=" * 60)
    print("BEST MOVING AVERAGE COMBINATION")
    print("=" * 60)
    print(f"Lower MA: {int(best['Lower_MA'])} days")
    print(f"Higher MA: {int(best['Higher_MA'])} days")
    print(f"Total Return: {best['Total_Return']*100:.2f}%")
    print(f"Number of Trades: {int(best['Num_Trades'])}")
    print(f"Idle Days (Out of Market): {int(best['Idle_Days'])} days")
    if best['Num_Trades'] > 0:
        print(f"Return per Trade: {best['Return_Per_Trade']*100:.2f}%")
    print(f"\nRisk-Free Earnings (Idle Period): {best['RF_Earnings_Pct']*100:.2f}%")
    print(f"Risk-Free Earnings (Dollars): ${rf_earnings_dollars:,.2f}")
    print(f"\nInitial Capital: ${initial_capital:,.2f}")
    print(f"Final Value: ${ma_strategy_final:,.2f}")
    print(f"Profit: ${ma_strategy_final - initial_capital:,.2f}")
    print(f"\nOutperformance vs Buy-Hold: {(best['Total_Return'] - buy_hold_return)*100:.2f}%")
    print(f"Extra Profit vs Buy-Hold: ${ma_strategy_final - buy_hold_final:,.2f}")
    print("=" * 60 + "\n")
    
    # Package best stats for visualization
    best_stats = {
        'num_trades': int(best['Num_Trades']),
        'idle_days': int(best['Idle_Days']),
        'rf_earnings_pct': best['RF_Earnings_Pct'],
        'ma_return': best['Total_Return']
    }
    
    return (int(best['Lower_MA']), int(best['Higher_MA'])), best['Total_Return'], results_df, buy_hold_return, best_stats