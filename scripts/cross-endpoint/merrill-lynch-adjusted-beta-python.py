# Full write-up: https://xfinlink.com/blog/merrill-lynch-adjusted-beta-python

import xfinlink as xfl
import pandas as pd
import numpy as np
from scipy import stats

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "XOM", "JNJ", "PG", "JPM", "GS", "UNH"]
benchmark = "SPY"

# -- Fetch 1Y daily returns -------------------------------------------------
df = xfl.prices(tickers + [benchmark], period="1y", fields=["return_daily"])
returns = df.pivot_table(index="date", columns="ticker", values="return_daily").dropna()

# -- OLS regression + Merrill Lynch adjustment ------------------------------
market = returns[benchmark]
results = []

for ticker in tickers:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        market, returns[ticker]
    )
    adj_beta = (2 / 3) * slope + (1 / 3) * 1.0
    results.append({
        "ticker": ticker,
        "raw_beta": slope,
        "adj_beta": adj_beta,
        "r_squared": r_value ** 2,
        "shrinkage": slope - adj_beta,
    })

rdf = pd.DataFrame(results).sort_values("raw_beta", ascending=False)

print("=== Raw Beta vs Merrill Lynch Adjusted Beta (1Y vs SPY) ===")
print(f"{'Ticker':6s}  {'Raw Beta':>9s}  {'Adj Beta':>9s}  {'Shrinkage':>10s}  {'R²':>6s}")
print("-" * 46)
for _, r in rdf.iterrows():
    print(
        f"{r['ticker']:6s}  {r['raw_beta']:>9.3f}  {r['adj_beta']:>9.3f}  "
        f"{r['shrinkage']:>+10.3f}  {r['r_squared']:>6.3f}"
    )
print(f"\nAdjustment formula: Adj Beta = (2/3) * Raw Beta + (1/3) * 1.0")
print(f"Average raw beta:  {rdf['raw_beta'].mean():.3f}")
print(f"Average adj beta:  {rdf['adj_beta'].mean():.3f}")
