"""
Portfolio Optimization Module
Implements Modern Portfolio Theory and Efficient Frontier
"""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def calculate_portfolio_metrics(weights, returns, cov_matrix):
    """
    Calculate portfolio return and volatility given weights.
    Returns: portfolio_return, portfolio_volatility
    """
    # Annualized portfolio return
    portfolio_return = np.sum(returns.mean() * weights) * 252
    
    # Annualized portfolio volatility (standard deviation)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    
    return portfolio_return, portfolio_volatility


def optimize_portfolio(returns, cov_matrix, target_return=None):
    """
    Find optimal portfolio weights using mean-variance optimization.
    If target_return is provided, optimize for that return level.
    Otherwise, optimize for maximum Sharpe ratio.
    Returns: optimal weights array
    """
    num_assets = len(returns.columns)
    
    # Objective function: minimize negative Sharpe ratio (maximize Sharpe)
    def negative_sharpe(weights):
        ret, vol = calculate_portfolio_metrics(weights, returns, cov_matrix)
        return -ret / vol  # Negative because we minimize
    
    # Constraints: weights sum to 1
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    
    # Bounds: each weight between 0 and 1 (no short selling)
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    # Initial guess: equal weights
    initial_weights = np.array([1/num_assets] * num_assets)
    
    # Optimize
    result = minimize(negative_sharpe, initial_weights, method='SLSQP', 
                     bounds=bounds, constraints=constraints)
    
    return result.x


def plot_efficient_frontier(returns, cov_matrix, tickers):
    """
    Generate and plot the efficient frontier.
    Returns: optimal_weights for max Sharpe ratio portfolio
    """
    print("\nCalculating Efficient Frontier...")
    
    # Find optimal portfolio (max Sharpe ratio)
    optimal_weights = optimize_portfolio(returns, cov_matrix)
    opt_return, opt_volatility = calculate_portfolio_metrics(
        optimal_weights, returns, cov_matrix)
    
    # Display optimal portfolio in terminal
    print("\n" + "=" * 60)
    print("OPTIMAL PORTFOLIO (Maximum Sharpe Ratio)")
    print("=" * 60)
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight*100:.2f}%")
    print(f"\nExpected Annual Return: {opt_return*100:.2f}%")
    print(f"Annual Volatility: {opt_volatility*100:.2f}%")
    print(f"Sharpe Ratio: {opt_return/opt_volatility:.2f}")
    print("=" * 60 + "\n")
    
    return optimal_weights