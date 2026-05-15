# How to Calculate and Compare Stock Volatility in Python

## What's the question?

When evaluating a stock for a portfolio, the first risk metric to examine is volatility -- a statistical measure of how much a stock's price fluctuates over a given period. A stock with high volatility experiences large daily price swings, while a low-volatility stock moves in a narrower range. But a single annualized number only tells part of the story. Volatility changes over time, and the recent risk regime may differ substantially from the trailing average. How do you measure both the overall and current volatility for a set of stocks, and how do those numbers compare across sectors?

## The approach

Annualized volatility is calculated as the standard deviation of daily returns, multiplied by the square root of 252 (the approximate number of trading days in a year). This scaling converts a daily measure into an annual one, making it comparable across different time horizons.

To capture the current risk environment, we also compute 30-day rolling volatility -- the same calculation applied to a sliding 30-day window of returns. This reveals whether a stock is currently in a calm or turbulent period relative to its full-year average.

Four stocks are selected across different sectors: AAPL (technology), TSLA (consumer discretionary / high-growth), JNJ (healthcare / defensive), and JPM (financials). As a final step, the maximum drawdown -- the largest peak-to-trough decline in price -- is computed for the most volatile stock in the group.

## Code

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Pull 1 year of daily prices for 4 stocks across different sectors
tickers = ["AAPL", "TSLA", "JNJ", "JPM"]
df = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

# Calculate annualized volatility per ticker
vol = (
    df.groupby("ticker")["return_daily"]
    .std()
    .mul(np.sqrt(252))  # annualize daily std dev
    .sort_values(ascending=False)
    .rename("annualized_vol")
)
print("=== Annualized Volatility (1Y) ===")
print(vol.round(4).to_string())
print()

# Calculate 30-day rolling volatility for each ticker
df["rolling_vol_30d"] = (
    df.groupby("ticker")["return_daily"]
    .transform(lambda x: x.rolling(30).std() * np.sqrt(252))
)

# Show the most recent 30-day rolling vol for each
latest = (
    df.sort_values("date")
    .groupby("ticker")
    .tail(1)[["ticker", "date", "rolling_vol_30d"]]
    .sort_values("rolling_vol_30d", ascending=False)
)
print("=== Latest 30-Day Rolling Volatility ===")
print(latest.to_string(index=False))
print()

# Find the max drawdown date range for the most volatile stock
most_volatile = vol.idxmax()
mv_prices = df[df["ticker"] == most_volatile].sort_values("date")
mv_prices["cummax"] = mv_prices["close"].cummax()
mv_prices["drawdown"] = mv_prices["close"] / mv_prices["cummax"] - 1
worst_dd = mv_prices.loc[mv_prices["drawdown"].idxmin()]
print(f"=== {most_volatile} Max Drawdown (1Y) ===")
print(f"Date: {worst_dd['date'].strftime('%Y-%m-%d')}")
print(f"Drawdown: {worst_dd['drawdown']:.2%}")
```

## Output

```
=== Annualized Volatility (1Y) ===
ticker
TSLA    0.4723
AAPL    0.2323
JPM     0.2121
JNJ     0.1682

=== Latest 30-Day Rolling Volatility ===
ticker       date  rolling_vol_30d
  TSLA 2026-05-07         0.436583
  AAPL 2026-05-07         0.250997
   JPM 2026-05-07         0.244608
   JNJ 2026-05-07         0.158343

=== TSLA Max Drawdown (1Y) ===
Date: 2026-04-08
Drawdown: -29.93%
```

## What this tells us

TSLA's annualized volatility of 47% is more than double JNJ's 17%, which reflects the fundamental difference in business model uncertainty between a high-growth electric vehicle manufacturer and a diversified healthcare conglomerate. AAPL and JPM occupy the middle ground near 23% and 21%, respectively.

The rolling volatility reveals a notable shift in the current regime. JPM's recent 30-day volatility (24.5%) has climbed close to AAPL's (25.1%), despite having lower full-year volatility. This convergence suggests that financials are pricing in elevated macroeconomic uncertainty in the near term.

TSLA's maximum drawdown of approximately 30% on April 8 aligns with the broader tariff-driven market selloff during that period. A drawdown of this magnitude, while severe, is consistent with the stock's high volatility profile.

## So what?

Annualized volatility provides a single summary of a stock's risk over a full period, but rolling volatility is the more actionable measure for portfolio management. A stock's risk profile can shift substantially within a year, and position sizing decisions should reflect the current regime rather than an annual average. When two stocks with historically different risk profiles begin converging in their rolling volatility -- as JPM and AAPL do here -- it signals a change in the market's assessment of relative risk that may warrant rebalancing.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
