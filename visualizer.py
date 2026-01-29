"""
Visualization Module
Creates plots and charts for analysis results
"""

import matplotlib.pyplot as plt
import numpy as np
from ma_strategy import calculate_moving_averages, generate_trading_signals


def create_combined_visualization(prices, optimal_weights, best_ma_combo, 
                                  buy_hold_return, ma_return, initial_capital,
                                  num_trades, idle_days, rf_earnings_pct,
                                  returns, cov_matrix, tickers):
    """
    Create a combined visualization with efficient frontier and strategy comparison.
    Shows all results in one figure with 2 columns.
    """
    lower_ma, higher_ma = best_ma_combo
    
    # Create main figure with 1 row, 2 columns
    fig = plt.figure(figsize=(20, 8))
    
    # ========================================================================
    # LEFT COLUMN: Efficient Frontier
    # ========================================================================
    ax1 = plt.subplot(1, 2, 1)
    
    # Generate random portfolios for visualization
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        
        # Calculate metrics
        portfolio_return = np.sum(returns.mean() * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        
        results[0, i] = portfolio_volatility
        results[1, i] = portfolio_return
        results[2, i] = portfolio_return / portfolio_volatility
    
    # Calculate optimal portfolio metrics
    opt_return = np.sum(returns.mean() * optimal_weights) * 252
    opt_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))) * np.sqrt(252)
    
    # Plot
    scatter = ax1.scatter(results[0, :], results[1, :], c=results[2, :], 
                cmap='viridis', marker='o', s=10, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Sharpe Ratio')
    ax1.scatter(opt_volatility, opt_return, marker='*', color='red', 
                s=500, label='Optimal Portfolio', zorder=5)
    
    # Add text box with portfolio details
    textstr = 'OPTIMAL PORTFOLIO\n' + '='*25 + '\n'
    for ticker, weight in zip(tickers, optimal_weights):
        textstr += f'{ticker}: {weight*100:.1f}%\n'
    textstr += f'\nAnnual Return: {opt_return*100:.1f}%\n'
    textstr += f'Volatility: {opt_volatility*100:.1f}%\n'
    textstr += f'Sharpe Ratio: {opt_return/opt_volatility:.2f}'
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')
    
    ax1.set_title('Efficient Frontier', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Volatility (Risk)', fontsize=11)
    ax1.set_ylabel('Expected Return', fontsize=11)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # RIGHT COLUMN: Strategy Comparison
    # ========================================================================
    ax2 = plt.subplot(1, 2, 2)
    
    # Portfolio value
    portfolio_value = (prices * optimal_weights).sum(axis=1)
    
    # Buy and hold returns
    buy_hold_returns = portfolio_value / portfolio_value.iloc[0]
    
    # MA strategy
    ma_data = calculate_moving_averages(portfolio_value, lower_ma, higher_ma)
    signals = generate_trading_signals(ma_data)
    signals = signals.dropna()
    
    # Calculate strategy equity curve
    daily_returns = portfolio_value.pct_change()
    strategy_returns = signals['Position'].shift(1) * daily_returns
    strategy_returns = strategy_returns.loc[signals.index].fillna(0)
    strategy_equity = (1 + strategy_returns).cumprod()
    
    # Plot equity curves
    ax2.plot(buy_hold_returns.index, buy_hold_returns.values, 
             label='Buy & Hold', linewidth=2.5, color='blue', alpha=0.7)
    ax2.plot(strategy_equity.index, strategy_equity.values, 
             label=f'MA Strategy ({lower_ma}/{higher_ma})', linewidth=2.5, 
             color='green', alpha=0.7)
    
    # Calculate dollar values
    buy_hold_final = initial_capital * (1 + buy_hold_return)
    ma_strategy_final = initial_capital * (1 + ma_return)
    rf_earnings_dollars = initial_capital * rf_earnings_pct
    
    # Create comprehensive text box with all metrics
    textstr = 'STRATEGY COMPARISON\n' + '='*40 + '\n\n'
    textstr += 'BUY-AND-HOLD STRATEGY:\n'
    textstr += f'  Return: {buy_hold_return*100:.2f}%\n'
    textstr += f'  Initial: ${initial_capital:,.0f}\n'
    textstr += f'  Final Value: ${buy_hold_final:,.0f}\n'
    textstr += f'  Profit: ${buy_hold_final - initial_capital:,.0f}\n\n'
    
    textstr += 'MOVING AVERAGE STRATEGY:\n'
    textstr += f'  Lower MA: {lower_ma} days\n'
    textstr += f'  Higher MA: {higher_ma} days\n'
    textstr += f'  Return: {ma_return*100:.2f}%\n'
    textstr += f'  Trades: {num_trades}\n'
    textstr += f'  Idle Days: {idle_days}\n'
    textstr += f'  Return/Trade: {(ma_return/num_trades)*100 if num_trades > 0 else 0:.2f}%\n\n'
    
    textstr += f'  RF Earnings: {rf_earnings_pct*100:.2f}%\n'
    textstr += f'  RF Earnings ($): ${rf_earnings_dollars:,.0f}\n\n'
    
    textstr += f'  Initial: ${initial_capital:,.0f}\n'
    textstr += f'  Final Value: ${ma_strategy_final:,.0f}\n'
    textstr += f'  Profit: ${ma_strategy_final - initial_capital:,.0f}\n\n'
    
    textstr += 'PERFORMANCE:\n'
    textstr += f'  Outperformance: {(ma_return - buy_hold_return)*100:.2f}%\n'
    textstr += f'  Extra Profit: ${ma_strategy_final - buy_hold_final:,.0f}'
    
    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9)
    ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', bbox=props, family='monospace')
    
    ax2.set_title('Strategy Performance Comparison', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=11)
    ax2.set_ylabel('Cumulative Return (Normalized)', fontsize=11)
    ax2.legend(fontsize=10, loc='lower right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complete_analysis.png', dpi=300, bbox_inches='tight')
    print("\nComplete analysis saved as 'complete_analysis.png'")
    plt.show()