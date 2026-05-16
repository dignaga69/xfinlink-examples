# Full write-up: https://xfinlink.com/blog/volatility-clustering-ljungbox-python

import xfinlink as xfl
import pandas as pd
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "XOM", "SPY"]

# -- Fetch 3Y daily returns -------------------------------------------------
df = xfl.prices(tickers, period="3y", fields=["return_daily"])

# -- Chart: SPY squared returns ---------------------------------------------
spy = df[df["ticker"] == "SPY"].copy()
spy["squared_return"] = spy["return_daily"] ** 2

fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(pd.to_datetime(spy["date"]), spy["squared_return"], width=1, color="#2563eb", alpha=0.7)
ax.set_title("SPY Squared Daily Returns (3Y) -- Volatility Clustering", fontsize=13)
ax.set_ylabel("Squared Return")
ax.set_xlabel("Date")
plt.tight_layout()
plt.savefig("volatility-clustering-ljungbox-python.png", dpi=150)
plt.close()
print("Chart saved: volatility-clustering-ljungbox-python.png\n")

# -- Ljung-Box test on squared returns -------------------------------------
print("=== Volatility Clustering: Ljung-Box Test on Squared Returns ===")
print("(Tests whether squared returns are autocorrelated -- i.e., whether large moves cluster together)")
print("(H0: no autocorrelation. If p < 0.05: reject H0 = volatility clusters.)")
print()
header = (
    f"{'Ticker':6s}  {'LB(10)':>8s}  {'p-value':>8s}  {'LB(20)':>8s}  "
    f"{'p-value':>8s}  {'Clusters?':>10s}"
)
print(header)
print("-" * 56)

lag1_results = {}

for ticker in tickers:
    r = df[df["ticker"] == ticker]["return_daily"].dropna()
    sq = r ** 2

    lb = acorr_ljungbox(sq, lags=[10, 20], return_df=True)
    lb10_stat = lb.loc[10, "lb_stat"]
    lb10_p = lb.loc[10, "lb_pvalue"]
    lb20_stat = lb.loc[20, "lb_stat"]
    lb20_p = lb.loc[20, "lb_pvalue"]

    clusters = "YES" if lb10_p < 0.05 else "NO"

    print(
        f"{ticker:6s}  {lb10_stat:>8.1f}  {lb10_p:>8.4f}  {lb20_stat:>8.1f}  "
        f"{lb20_p:>8.4f}  {clusters:>10s}"
    )

    # Lag-1 autocorrelation of squared returns
    lag1_results[ticker] = sq.autocorr(lag=1)

# -- Lag-1 autocorrelation summary ----------------------------------------
print("\n=== Lag-1 Autocorrelation of Squared Returns ===")
for ticker in tickers:
    print(f"  {ticker}: {lag1_results[ticker]:.3f}")
