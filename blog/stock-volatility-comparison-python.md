# How to Calculate and Compare Stock Volatility in Python

Volatility is the most important risk metric in finance — it tells you how much a stock's price moves day to day. If you're building a portfolio, screening for trades, or just trying to understand risk, annualized volatility is the number to watch. Here's how to calculate it for any stock using daily returns.

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

**Output:**

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

TSLA's annualized volatility at 47% is more than double JNJ's 17% — exactly the kind of spread you'd expect between a high-beta growth stock and a consumer staples defensive name. The max drawdown of ~30% on April 8 lines up with the broader tariff-driven selloff. Rolling volatility is useful because it shows you the *current* risk regime, not just the average over the year — JPM's recent 30-day vol has actually climbed close to AAPL's, suggesting financials are pricing in more macro uncertainty.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
