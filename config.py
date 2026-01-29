"""
Configuration and User Input Module
Handles all user inputs at the start of the program
"""

def get_user_inputs():
    """
    Collect all user inputs at the beginning of the program.
    Returns: num_assets (int), tickers (list), step_size (int), risk_free_rate (float), initial_capital (float)
    """
    print("=" * 60)
    print("PORTFOLIO OPTIMIZER WITH MOVING AVERAGE STRATEGY")
    print("=" * 60)
    
    # Get number of assets
    num_assets = int(input("\nEnter the number of assets in your portfolio: "))
    
    # Get ticker symbols
    tickers = []
    print("\nEnter ticker symbols (as listed on Yahoo Finance):")
    for i in range(num_assets):
        ticker = input(f"  Asset {i+1}: ").upper().strip()
        tickers.append(ticker)
    
    # Get step size for moving average optimization
    step_size = int(input("\nEnter step size for moving average optimization (e.g., 1, 5, 10): "))
    
    # Get risk-free rate (annual percentage)
    risk_free_rate = float(input("\nEnter annual risk-free rate (e.g., 4.5 for 4.5%): ")) / 100
    
    # Get initial capital
    initial_capital = float(input("\nEnter initial capital amount (e.g., 10000): "))
    
    print("\n" + "=" * 60)
    print(f"Assets selected: {', '.join(tickers)}")
    print(f"MA step size: {step_size}")
    print(f"Risk-free rate: {risk_free_rate*100:.2f}%")
    print(f"Initial capital: ${initial_capital:,.2f}")
    print("=" * 60 + "\n")
    
    return num_assets, tickers, step_size, risk_free_rate, initial_capital