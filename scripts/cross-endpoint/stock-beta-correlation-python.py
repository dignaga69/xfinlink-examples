# Full write-up: https://xfinlink.com/blog/stock-beta-correlation-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("xfl_91cda643688e76bd182665c64ca6aedc")

# Pull 3 years of daily returns for 5 stocks + SPY (market proxy)
tickers = ["AAPL", "NVDA", "XOM", "PG", "JPM", "SPY"]
df = xfl.prices(tickers, period="3y", fields=["close", "return_daily"])

# Pivot returns into a wide table: columns = tickers, rows = dates
returns = df.pivot_table(index="date", columns="ticker", values="return_daily")

# Drop dates with any missing values (ensures aligned returns)
returns = returns.dropna()

# Calculate correlation matrix
corr = returns.corr()
print("=== Correlation Matrix (3Y Daily Returns) ===")
print(corr.round(3).to_string())
print()

# Calculate beta for each stock vs SPY
# Beta = Cov(stock, market) / Var(market)
market = returns["SPY"]
market_var = market.var()

betas = {}
for ticker in ["AAPL", "NVDA", "XOM", "PG", "JPM"]:
    cov = returns[ticker].cov(market)
    beta = cov / market_var
    betas[ticker] = round(beta, 3)

beta_df = pd.DataFrame.from_dict(betas, orient="index", columns=["beta"])
beta_df = beta_df.sort_values("beta", ascending=False)

# Add annualized vol and return for context
for ticker in beta_df.index:
    r = returns[ticker]
    beta_df.loc[ticker, "ann_vol"] = round(r.std() * np.sqrt(252), 3)
    beta_df.loc[ticker, "ann_return"] = round((1 + r.mean()) ** 252 - 1, 3)
    beta_df.loc[ticker, "corr_spy"] = round(r.corr(market), 3)

print("=== Beta, Volatility, and Return vs SPY (3Y) ===")
print(beta_df.to_string())
print()

# Risk-return interpretation
highest_beta = beta_df.index[0]
lowest_beta = beta_df.index[-1]
print(f"Highest beta: {highest_beta} ({beta_df.loc[highest_beta, 'beta']}) — most sensitive to market moves")
print(f"Lowest beta:  {lowest_beta} ({beta_df.loc[lowest_beta, 'beta']}) — most defensive")
