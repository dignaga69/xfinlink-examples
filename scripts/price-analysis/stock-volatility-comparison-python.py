# Full write-up: https://xfinlink.com/blog/stock-volatility-comparison-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("YOUR_API_KEY")

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
