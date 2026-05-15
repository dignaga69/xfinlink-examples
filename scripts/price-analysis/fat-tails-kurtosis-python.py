# Full write-up: https://xfinlink.com/blog/fat-tails-kurtosis-python

import xfinlink as xfl
import pandas as pd
import numpy as np
from scipy import stats as sp_stats

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "XOM", "JNJ", "SPY"]

# -- Fetch 3Y daily returns -------------------------------------------------
df = xfl.prices(tickers, period="3y", fields=["return_daily"])

# -- Kurtosis analysis ------------------------------------------------------
print("=== Fat Tails in Financial Returns: Kurtosis Analysis (3Y) ===")
header = (
    f"{'Ticker':6s}  {'Kurtosis':>9s}  {'Excess':>7s}  {'Skewness':>9s}  "
    f"{'JB Stat':>8s}  {'JB p':>7s}  {'Normal?':>8s}"
)
print(header)
print("-" * 62)

for ticker in tickers:
    r = df[df["ticker"] == ticker]["return_daily"].dropna()
    kurt = sp_stats.kurtosis(r, fisher=False)       # Pearson kurtosis
    excess = kurt - 3.0
    skew = sp_stats.skew(r)
    jb_stat, jb_p = sp_stats.jarque_bera(r)
    is_normal = "YES" if jb_p > 0.05 else "NO"
    print(
        f"{ticker:6s}  {kurt:>9.2f}  {excess:>+7.2f}  {skew:>+9.3f}  "
        f"{jb_stat:>8.1f}  {jb_p:>7.4f}  {is_normal:>8s}"
    )

# -- Summary stats -----------------------------------------------------------
all_excess = []
n_reject = 0
obs = None

for ticker in tickers:
    r = df[df["ticker"] == ticker]["return_daily"].dropna()
    obs = len(r)
    kurt = sp_stats.kurtosis(r, fisher=False)
    all_excess.append(kurt - 3.0)
    _, jb_p = sp_stats.jarque_bera(r)
    if jb_p < 0.05:
        n_reject += 1

print(f"\nAverage excess kurtosis: {np.mean(all_excess):+.2f} (normal = 0)")
print(f"Stocks rejecting normality (JB test, p<0.05): {n_reject}/{len(tickers)} = {n_reject/len(tickers):.0%}")
print(f"Observations per stock: {obs}")

# -- 3-Sigma event count ----------------------------------------------------
print(f"\n=== 3-Sigma Events: Expected vs Actual (3Y) ===")

for ticker in ["NVDA", "TSLA", "SPY"]:
    r = df[df["ticker"] == ticker]["return_daily"].dropna()
    sigma = r.std()
    n_3sig = (r.abs() > 3 * sigma).sum()
    expected = len(r) * 0.0027
    ratio = n_3sig / expected if expected > 0 else 0
    print(
        f"  {ticker}: {n_3sig} events (expected {expected:.1f} under normality) "
        f"= {ratio:.1f}x more"
    )
