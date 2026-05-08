# How to Calculate Stock Beta and Correlation in Python

Beta tells you how much a stock moves relative to the market — a beta of 2 means the stock moves roughly twice as much as the S&P 500 on any given day. It's the core metric for portfolio risk management and the capital asset pricing model (CAPM). Here's how to calculate beta, correlation, and annualized volatility for any stock using 3 years of daily returns.

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== Correlation Matrix (3Y Daily Returns) ===
ticker   AAPL    JPM   NVDA     PG    SPY    XOM
ticker                                          
AAPL    1.000  0.310  0.351  0.143  0.664  0.126
JPM     0.310  1.000  0.263  0.063  0.607  0.258
NVDA    0.351  0.263  1.000 -0.158  0.644 -0.041
PG      0.143  0.063 -0.158  1.000  0.134  0.088
SPY     0.664  0.607  0.644  0.134  1.000  0.200
XOM     0.126  0.258 -0.041  0.088  0.200  1.000

=== Beta, Volatility, and Return vs SPY (3Y) ===
       beta  ann_vol  ann_return  corr_spy
NVDA  2.076    0.489       1.185     0.644
AAPL  1.130    0.258       0.228     0.664
JPM   0.911    0.227       0.360     0.607
XOM   0.301    0.228       0.156     0.200
PG    0.151    0.171       0.007     0.134

Highest beta: NVDA (2.076) — most sensitive to market moves
Lowest beta:  PG (0.151) — most defensive
```

NVDA's beta of 2.08 means it amplifies market moves by roughly 2x — which explains both its 118% annualized return during the AI boom and its sharp drawdowns during selloffs. The most interesting number in the correlation matrix is the -0.158 between NVDA and PG: these two stocks are slightly negatively correlated, meaning they naturally hedge each other. PG's beta of 0.15 makes it the classic defensive position — near-zero market sensitivity, but also near-zero return over 3 years. XOM's low beta (0.30) and low correlation with tech (0.13 with AAPL, -0.04 with NVDA) confirms energy still acts as a diversifier in a tech-heavy portfolio.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
