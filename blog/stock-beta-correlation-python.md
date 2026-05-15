# How to Calculate Stock Beta and Correlation in Python

## What's the question?

Beta is a measure of how sensitive a stock's returns are to movements in the overall market. A beta of 1.0 means the stock moves in lockstep with the market; a beta of 2.0 means it amplifies market moves by a factor of two; a beta near zero means the stock is largely indifferent to broad market conditions. Beta is the central parameter in the Capital Asset Pricing Model (CAPM), the foundational theory that relates expected return to systematic risk. Combined with correlation and volatility, beta quantifies both the direction and magnitude of a stock's relationship with the market. How do these measures differ across sectors, and what do they reveal about portfolio diversification?

## The approach

Beta is computed as the covariance of a stock's daily returns with the market's daily returns, divided by the variance of the market's returns. SPY (the SPDR S&P 500 ETF) serves as the market proxy. The correlation matrix shows the pairwise linear relationship between all stocks and the market, while annualized volatility and annualized return provide context for interpreting each stock's risk-return profile.

Five stocks are selected to span a range of expected beta values: AAPL and NVDA (technology), XOM (energy), PG (consumer staples), and JPM (financials). Three years of daily returns are used to ensure a statistically meaningful sample.

## Code

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

## Output

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

## What this tells us

NVDA's beta of 2.08 confirms that it amplifies market movements by approximately two times, which is consistent with both its 118% annualized return during the AI-driven rally and the severity of its drawdowns during selloffs. Beta captures both sides of market sensitivity -- the upside and the downside are symmetric in expectation.

The correlation matrix reveals the diversification structure of this portfolio. NVDA and PG have a correlation of -0.158, meaning they tend to move in opposite directions. This negative correlation makes them natural hedges for each other within a portfolio. XOM is also nearly uncorrelated with the technology stocks (0.126 with AAPL, -0.041 with NVDA), confirming that energy remains an effective diversifier against a tech-heavy allocation.

PG's beta of 0.15 and correlation of 0.13 with SPY make it the most defensive stock in the group, with almost no systematic risk exposure. However, the cost of that defensiveness is visible in the near-zero annualized return (0.7% over three years).

## So what?

Beta is the starting point for portfolio construction because it quantifies how much market risk each position contributes. A portfolio with a weighted-average beta of 1.0 will track the market; shifting toward lower-beta stocks reduces drawdowns but sacrifices upside participation. The correlation matrix adds the diversification dimension: two stocks can both have high beta but still diversify each other if their correlation is low. When constructing a multi-asset portfolio, examine both beta (exposure to the market factor) and pairwise correlations (exposure to idiosyncratic co-movement) to achieve genuine diversification rather than simply holding multiple names that move together.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
