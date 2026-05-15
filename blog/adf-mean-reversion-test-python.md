# Are Stock Prices Mean-Reverting? Augmented Dickey-Fuller Test in Python

## What's the question?

Mean reversion is the idea that asset prices tend to return to a long-run average over time. A stock that has fallen significantly will eventually recover. A stock that has risen sharply will eventually pull back. Many trading strategies depend on this assumption — pairs trading, Bollinger Band signals, and RSI-based entries all rely on prices reverting to some equilibrium.

The problem is that this assumption may not be correct. If stock prices follow a random walk — where each day's movement is independent and the series has no tendency to return to any particular level — then mean reversion strategies are attempting to exploit a pattern that does not exist.

The Augmented Dickey-Fuller (ADF) test provides a statistical answer. It tests whether a time series contains a unit root. A unit root indicates that the series is non-stationary: it wanders freely without a fixed mean to return to. If the test rejects the unit root hypothesis (p-value below 0.05), the series is stationary — it fluctuates around a stable average, and mean reversion has a mathematical basis.

The "augmented" component addresses a practical limitation. The original Dickey-Fuller test assumes each observation depends only on the previous one. Financial data typically exhibits autocorrelation across multiple lags. The augmented version includes additional lagged terms to account for this. The `autolag="AIC"` parameter selects the optimal number of lags automatically using the Akaike Information Criterion.

## The approach

We test 6 stocks across different sectors: AAPL and MSFT (technology), XOM (energy), JNJ (healthcare), NVDA (semiconductors), and PG (consumer staples). Sector diversity is important because mean reversion, if it exists, may appear in defensive sectors but not in high-growth ones.

For each stock, we run the ADF test on two series: raw closing prices and daily returns. This distinction is central. Prices and returns have fundamentally different statistical properties, and confusing the two is one of the most common errors in quantitative strategy design.

## Code

```python
import xfinlink as xfl
import pandas as pd
from statsmodels.tsa.stattools import adfuller

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "XOM", "JNJ", "NVDA", "PG"]
df = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

for ticker in tickers:
    t = df[df["ticker"] == ticker].sort_values("date")

    adf_price = adfuller(t["close"].dropna(), autolag="AIC")
    adf_return = adfuller(t["return_daily"].dropna(), autolag="AIC")

    price_tag = "STATIONARY" if adf_price[1] < 0.05 else "UNIT ROOT"
    return_tag = "STATIONARY" if adf_return[1] < 0.05 else "UNIT ROOT"

    print(f"{ticker}: price p={adf_price[1]:.4f} ({price_tag})  "
          f"return p={adf_return[1]:.4f} ({return_tag})")
```

## Output

```
AAPL:  price p=0.8803 (UNIT ROOT)   return p=0.0000 (STATIONARY)
MSFT:  price p=0.8325 (UNIT ROOT)   return p=0.0000 (STATIONARY)
XOM:   price p=0.8937 (UNIT ROOT)   return p=0.0000 (STATIONARY)
JNJ:   price p=0.6168 (UNIT ROOT)   return p=0.0000 (STATIONARY)
NVDA:  price p=0.5708 (UNIT ROOT)   return p=0.0000 (STATIONARY)
PG:    price p=0.4340 (UNIT ROOT)   return p=0.0000 (STATIONARY)
```

## What this tells us

The results are consistent across every sector. All 6 price series contain unit roots. P-values range from 0.43 (PG) to 0.89 (XOM), none approaching the 0.05 rejection threshold. Stock prices do not mean-revert.

This holds even for PG — Procter & Gamble, the most stable and defensive stock in the sample. If any equity were to exhibit mean-reverting prices, a low-volatility consumer staple would be the most likely candidate. Its p-value of 0.43 confirms that the random walk property is not a function of volatility or sector. It is structural. Markets incorporate available information into prices continuously, so future price movements are driven by new information, which is by definition unpredictable. There is no fixed level for prices to return to.

Daily returns present the opposite result. Every p-value is 0.0000 — strongly stationary. Returns fluctuate around a stable mean near zero. This follows directly from the mathematical relationship between prices and returns. If prices are integrated of order 1 (a random walk), then returns — the first difference of prices — are integrated of order 0 (stationary). Differencing removes the unit root.

This duality is foundational in quantitative finance. Portfolio theory, the Capital Asset Pricing Model, factor models, and options pricing all assume stationary returns, not stationary prices. The ADF test provides empirical verification of this assumption.

## So what?

A strategy that buys when price falls below a moving average and sells when it crosses above is implicitly assuming prices are stationary. The evidence above indicates they are not. The strategy may produce occasional gains, but it lacks statistical support.

Mean reversion strategies can be effective, but not on raw prices. The key is to construct derived series that are stationary: the spread between two correlated stocks in a pairs trade, the ratio of a stock's price to its sector ETF, or the z-score of price relative to a rolling mean. These constructed series can exhibit stationarity, and the ADF test is the standard method for confirming this before committing capital.

The test requires three lines of code. If the p-value indicates a unit root, mean reversion should not be assumed. If it indicates stationarity, there is a statistical basis to proceed. This verification should be standard practice in any quantitative workflow.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
