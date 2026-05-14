# Full write-up: https://xfinlink.com/blog/adf-mean-reversion-test-python

import numpy as np
from statsmodels.tsa.stattools import adfuller
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Fetch 1Y daily prices for six stocks -----------------------------------
tickers = ["AAPL", "MSFT", "XOM", "JNJ", "NVDA", "PG"]
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print("=== Augmented Dickey-Fuller Test: Are Stock Prices Mean-Reverting? ===")
print("(H0: unit root exists = non-stationary = trending/random walk)")
print("(If p < 0.05: reject H0 → stationary → mean-reverting)")
print()

header = (
    f"{'Ticker':<9}"
    f"{'Price ADF':>9}   {'Price p':>7}   {'Result':>12}  |  "
    f"{'Return ADF':>10}   {'Return p':>8}   {'Result':>12}"
)
print(header)
print("-" * len(header))

prices_stationary = 0
returns_stationary = 0

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").copy()
    df = df.dropna(subset=["close", "return_daily"])

    close = df["close"].values
    returns = df["return_daily"].values

    # ADF on raw prices
    adf_price, p_price, *_ = adfuller(close, autolag="AIC")
    price_result = "STATIONARY" if p_price < 0.05 else "UNIT ROOT"
    if p_price < 0.05:
        prices_stationary += 1

    # ADF on daily returns
    adf_ret, p_ret, *_ = adfuller(returns, autolag="AIC")
    ret_result = "STATIONARY" if p_ret < 0.05 else "UNIT ROOT"
    if p_ret < 0.05:
        returns_stationary += 1

    print(
        f"{ticker:<9}"
        f"{adf_price:9.3f}   {p_price:7.4f}   {price_result:>12}  |  "
        f"{adf_ret:10.3f}   {p_ret:8.4f}   {ret_result:>12}"
    )

print()
print(f"Prices stationary:  {prices_stationary}/{len(tickers)} (expect 0 — prices follow random walks)")
print(f"Returns stationary: {returns_stationary}/{len(tickers)} (expect all — returns are i.i.d.)")
