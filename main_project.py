"""
Main Execution File
Portfolio Optimization with Moving Average Strategy

This is the entry point of the application.
Run this file to execute the entire analysis.
"""

from config import get_user_inputs
from data_handler import download_price_data
from portfolio_optimizer import plot_efficient_frontier
from ma_strategy import generate_ma_combinations
from backtester import optimize_ma_strategy
from visualizer import create_combined_visualization


def main():
    """
    Main function that orchestrates the entire workflow.
    """
    # Step 1: Get user inputs
    num_assets, tickers, step_size, risk_free_rate, initial_capital = get_user_inputs()
    
    # Step 2: Download price data
    prices = download_price_data(tickers)
    
    # Step 3: Calculate returns and covariance
    returns = prices.pct_change().dropna()
    cov_matrix = returns.cov()
    
    # Step 4: Plot efficient frontier and get optimal weights
    optimal_weights = plot_efficient_frontier(returns, cov_matrix, tickers)
    
    # Step 5: Generate MA combinations
    ma_combinations = generate_ma_combinations(step_size)
    
    # Step 6: Optimize MA strategy
    best_ma_combo, best_return, results_df, buy_hold_return, best_stats = optimize_ma_strategy(
        prices, optimal_weights, ma_combinations, risk_free_rate, initial_capital)
    
    # Step 7: Save results to CSV
    results_df.to_csv('ma_optimization_results.csv', index=False)
    print("Detailed results saved to 'ma_optimization_results.csv'\n")
    
    # Step 8: Create combined visualization with all data
    create_combined_visualization(
        prices, optimal_weights, best_ma_combo, 
        buy_hold_return, best_stats['ma_return'], initial_capital,
        best_stats['num_trades'], best_stats['idle_days'], 
        best_stats['rf_earnings_pct'], returns, cov_matrix, tickers
    )
    
    # Final summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("Files generated:")
    print("  1. complete_analysis.png - Combined visualization with all results")
    print("  2. ma_optimization_results.csv - Detailed MA optimization results")
    print("=" * 60)


if __name__ == "__main__":
    main()