# Portfolio Optimizer with Moving Average Strategy

A finance project that combines Modern Portfolio Theory with tactical timing strategies to optimize portfolio allocation and returns.

## What it does

Takes your stock picks, finds the mathematically optimal weights using efficient frontier analysis, then tests thousands of moving average combinations to see if active timing can beat simple buy-and-hold.

## How to use
```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install yfinance pandas numpy scipy matplotlib

# Run
python3 main.py
```

You'll be asked for:
- Stock tickers (e.g., AAPL, MSFT, GOOGL)
- Step size for MA testing (1 = slow/thorough, 10 = fast/rough)
- Risk-free rate (e.g., 4.5 for 4.5% T-bills)
- Initial capital amount

## What you get

One image showing:
- **Left**: Efficient frontier with your optimal portfolio weights
- **Right**: Buy-hold vs MA strategy comparison with all the numbers

Plus a CSV with every MA combination tested, sorted by performance.

## The interesting part

Most of the time, the MA strategy underperforms buy-and-hold. When it works, it's usually avoiding big drawdowns during crashes. Either way, you'll know if timing actually adds value for your specific portfolio.

## Files

- `main.py` - Entry point, run this
- `config.py` - User inputs
- `data_handler.py` - Yahoo Finance downloads
- `portfolio_optimizer.py` - Efficient frontier math
- `ma_strategy.py` - Moving average logic
- `backtester.py` - Strategy testing
- `visualizer.py` - Charts

## Notes

Yahoo Finance gives you data from the most recent stock's start date. So if you mix a 1990 stock with a 2020 IPO, you only get 2020-present. This is correct - you can't build a portfolio with stocks that didn't exist yet.

The risk-free rate assumes your idle cash earns that rate. In reality, you'd need to actually put it in T-bills or a money market fund.

Not financial advice. Just math on historical data.