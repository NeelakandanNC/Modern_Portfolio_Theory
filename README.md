# Modern Portfolio Creator and Analyzer

This script is an interactive tool for creating and analyzing a stock portfolio using the Modern Portfolio Theory approach. It leverages financial data from Yahoo Finance to help users build a market-cap-weighted portfolio, analyze its performance, and visualize key metrics.

## Features
- **User Input:** Enter a list of stock tickers to include in your portfolio.
- **Data Download:** Fetches historical price data (since 2000) for all selected stocks.
- **Data Cleaning:** Trims data to the common period where all stocks have available data.
- **Market Cap Weighting:** Calculates each stock's weight in the portfolio based on its market capitalization.
- **Portfolio Performance:** Computes portfolio returns, cumulative returns, annualized return, and volatility.
- **Risk Metrics:** Calculates maximum drawdown and beta (vs. SPY benchmark) for each stock and the portfolio.
- **Visualization:** Generates charts for stock prices, portfolio performance, risk vs. return, market caps, max drawdown, and beta.

## How to Use
1. **Run the Script:**
   - Make sure you have Python 3.x installed.
   - Install required packages: `yfinance`, `pandas`, `matplotlib`, `numpy`, `scipy`.
   - Run the script in a terminal: `python modern_portfolio_creator_and_analyser.py`
2. **Input Tickers:**
   - When prompted, enter stock tickers separated by commas (e.g., `AAPL,MSFT,GOOGL`).
3. **View Results:**
   - The script will download data, perform analysis, and display results and charts.

## Requirements
- Python 3.x
- yfinance
- pandas
- matplotlib
- numpy
- scipy

Install dependencies with:
```
pip install yfinance pandas matplotlib numpy scipy
```

## Notes
- The script uses market capitalization to weight stocks in the portfolio.
- If market cap data is missing for a ticker, it will be excluded from the portfolio.
- The benchmark for beta calculation is SPY (S&P 500 ETF).
- Results may be unreliable if limited historical data is available for the selected tickers.

## License
This script is provided for educational and informational purposes only. Use at your own risk.
