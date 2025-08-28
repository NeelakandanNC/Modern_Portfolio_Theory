import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# 1. Get tickers from user input
print("=== Modern Portfolio Creator and Analyzer ===")
print("Enter stock tickers separated by commas (e.g., AAPL,MSFT,GOOGL)")
print("Example tech stocks: NVDA,AMD,INTC,CSCO,AVGO,GLW,DELL,STX,WDC,VRT,CAT,ETN")

while True:
    user_input = input("\nEnter stock tickers: ").strip()
    if user_input:
        # Clean up the input and create tickers list
        tickers = [ticker.strip().upper() for ticker in user_input.split(',')]
        tickers = [t for t in tickers if t]  # Remove empty strings
        
        if len(tickers) >= 2:
            print(f"Selected tickers: {tickers}")
            break
        else:
            print("Please enter at least 2 stock tickers.")
    else:
        print("Please enter some stock tickers.")

# 2. Download max historical data
print(f"\nDownloading data for {len(tickers)} tickers...")
try:
    data = yf.download(tickers, start="2000-01-01")['Close']
    
    # Check if data was successfully downloaded
    if data.empty:
        print("Error: No data could be downloaded. Please check your ticker symbols.")
        exit()
    
    # If only one ticker, ensure it's a DataFrame
    if len(tickers) == 1:
        data = data.to_frame()
        data.columns = tickers
    
    print("Data download completed!")
    
except Exception as e:
    print(f"Error downloading data: {e}")
    print("Please check your internet connection and ticker symbols.")
    exit()

# 3. Trim to the earliest date where all tickers have data
initial_data_points = len(data)
data_before_trim = data.copy()

# Check how much data is available for each ticker
print(f"\nData availability check:")
for ticker in tickers:
    if ticker in data.columns:
        valid_data = data[ticker].dropna()
        print(f"{ticker}: {len(valid_data)} data points from {valid_data.index[0].date()} to {valid_data.index[-1].date()}")
    else:
        print(f"{ticker}: No data available")

start_date = data.dropna(how='any').index[0]
data = data.loc[start_date:]
final_data_points = len(data)

print(f"\nTrimmed data to common period: {start_date.date()} to {data.index[-1].date()}")
print(f"Data points after trimming: {final_data_points}")

if final_data_points < 50:
    print("Warning: Very limited data available. Results may not be reliable.")
elif final_data_points < 250:
    print("Warning: Limited data available (less than 1 year). Consider using tickers with longer history.")

# 4. Stock returns (%)
returns = data.pct_change() * 100

# 5. Market caps & weights
print(f"\nCalculating market caps and portfolio weights...")
market_caps = {}
for t in tickers:
    try:
        ticker_info = yf.Ticker(t).info
        market_cap = ticker_info.get('marketCap', np.nan)
        if not np.isnan(market_cap):
            market_caps[t] = market_cap
            print(f"{t}: ${market_cap/1e9:.2f}B market cap")
        else:
            print(f"{t}: Market cap not available")
    except Exception as e:
        print(f"{t}: Error retrieving market cap - {e}")

if not market_caps:
    print("Error: No market cap data available for any tickers.")
    exit()

valid = [t for t in tickers if t in market_caps]
caps = pd.Series({t: market_caps[t] for t in valid})
weights = caps / caps.sum()

print(f"\nPortfolio weights (market cap weighted):")
for ticker in valid:
    print(f"{ticker}: {weights[ticker]:.1%}")

if len(valid) < len(tickers):
    excluded = [t for t in tickers if t not in valid]
    print(f"\nNote: Excluded from portfolio due to missing market cap data: {excluded}")

# 6. Portfolio returns & cumulative "price"
print(f"\nCalculating portfolio performance...")
port_ret = (returns[valid].multiply(weights, axis=1)).sum(axis=1)
port_price = (1 + port_ret/100).cumprod()

# Calculate some basic portfolio statistics
portfolio_total_return = (port_price.iloc[-1] - 1) * 100
portfolio_annualized_return = ((port_price.iloc[-1] ** (252 / len(port_price))) - 1) * 100
portfolio_volatility = port_ret.std() * np.sqrt(252)

print(f"Portfolio total return: {portfolio_total_return:.2f}%")
print(f"Portfolio annualized return: {portfolio_annualized_return:.2f}%")
print(f"Portfolio annualized volatility: {portfolio_volatility:.2f}%")

# 7. Max drawdown
def max_drawdown(prices: pd.Series) -> float:
    peak = prices.cummax()
    dd = (prices - peak) / peak
    return dd.min() * 100  # as percentage

stock_drawdowns = {t: max_drawdown(data[t]) for t in valid}
port_drawdown = max_drawdown(port_price)

# 8. Beta calculation
print(f"\nDownloading benchmark data (SPY)...")
benchmark = yf.download('SPY', start=start_date)['Close']
bm_ret = benchmark.pct_change() * 100

def calculate_beta(asset_ret: pd.Series, bench_ret: pd.Series) -> float:
    df = pd.concat([asset_ret, bench_ret], axis=1, join='inner').dropna()
    x = df.iloc[:,1]  # benchmark
    y = df.iloc[:,0]  # asset
    slope, _, _, _, _ = linregress(x, y)
    return slope

betas = {t: calculate_beta(returns[t], bm_ret) for t in valid}
port_beta = calculate_beta(port_ret, bm_ret)

print(f"\nBeta calculations (vs SPY):")
for ticker in valid:
    print(f"{ticker}: {betas[ticker]:.2f}")
print(f"Portfolio: {port_beta:.2f}")

# 9. Plotting (2 rows × 3 columns)
print(f"\nGenerating charts...")
fig, axs = plt.subplots(2, 3, figsize=(18, 10))

# (0,0) Stock Prices
for t in valid:
    axs[0,0].plot(data.index, data[t], label=t)
axs[0,0].set_title("Stock Prices Over Time")
axs[0,0].legend(loc='upper left', fontsize='small', ncol=2)
axs[0,0].grid(True)

# (0,1) Portfolio Performance (cumulative %)
axs[0,1].plot(port_price.index, (port_price - 1)*100, color='black')
axs[0,1].set_title("Portfolio Cumulative Return (%)")
axs[0,1].set_ylabel("Cumulative Return (%)")
axs[0,1].grid(True)

# (0,2) Risk vs Return
mean_ret = returns[valid].mean()
std_ret  = returns[valid].std()
axs[0,2].scatter(std_ret, mean_ret, color='blue')
for t in valid:
    axs[0,2].annotate(t, (std_ret[t], mean_ret[t]), fontsize=8)
axs[0,2].scatter(port_ret.std(), port_ret.mean(), color='red', marker='*', s=150, label='Portfolio')
axs[0,2].set_title("Mean vs Std Dev (%)")
axs[0,2].set_xlabel("Std Dev (%)")
axs[0,2].set_ylabel("Mean Return (%)")
axs[0,2].legend()
axs[0,2].grid(True)

# (1,0) Market Caps
axs[1,0].bar(valid, caps[valid]/1e9, color='teal')
axs[1,0].set_title("Market Cap (USD billions)")
axs[1,0].set_ylabel("Billions USD")
axs[1,0].tick_params(axis='x', rotation=90)
axs[1,0].grid(True)

# (1,1) Max Drawdown
dd_vals = {**stock_drawdowns, 'Portfolio': port_drawdown}
axs[1,1].bar(dd_vals.keys(), dd_vals.values(), color='orange')
axs[1,1].set_title("Max Drawdown (%)")
axs[1,1].tick_params(axis='x', rotation=90)
axs[1,1].grid(True)

# (1,2) Beta
beta_vals = {**betas, 'Portfolio': port_beta}
axs[1,2].bar(beta_vals.keys(), beta_vals.values(), color='green')
axs[1,2].set_title("Beta vs SPY")
axs[1,2].tick_params(axis='x', rotation=90)
axs[1,2].grid(True)

plt.tight_layout()
plt.show()

print(f"\nAnalysis complete!")
