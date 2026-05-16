# Full write-up: https://xfinlink.com/blog/capm-cost-of-equity-python

import xfinlink as xfl
import pandas as pd
import numpy as np
from scipy import stats

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "JPM", "XOM", "UNH", "PG", "JNJ"]
benchmark = "SPY"
rf = 0.043        # 10-year Treasury yield (annualized)
erp = 0.055       # equity risk premium (long-run estimate)

# -- Fetch 3Y daily returns -------------------------------------------------
df = xfl.prices(tickers + [benchmark], period="3y", fields=["return_daily"])
returns = df.pivot_table(index="date", columns="ticker", values="return_daily").dropna()

# -- OLS regression for beta estimation ------------------------------------
market = returns[benchmark]
results = []

for ticker in tickers:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        market, returns[ticker]
    )
    cost_of_equity = rf + slope * erp
    results.append({
        "ticker": ticker,
        "beta": slope,
        "beta_se": std_err,
        "r_squared": r_value ** 2,
        "cost_of_equity": cost_of_equity,
    })

rdf = pd.DataFrame(results).sort_values("cost_of_equity", ascending=False)

# -- Print results ---------------------------------------------------------
print("=== CAPM Cost of Equity Estimation ===")
print(f"Risk-free rate (Rf): {rf:.1%}  |  Equity risk premium (ERP): {erp:.1%}")
print(f"Formula: Ke = Rf + Beta x ERP = {rf:.1%} + Beta x {erp:.1%}")
print()
print(f"{'Ticker':6s}  {'Beta':>6s}  {'Beta SE':>8s}  {'R\u00b2':>8s}  {'Cost of Equity':>15s}")
print("-" * 46)

for _, r in rdf.iterrows():
    print(
        f"{r['ticker']:6s}  {r['beta']:>6.2f}  {r['beta_se']:>8.3f}  "
        f"{r['r_squared']:>8.3f}  {r['cost_of_equity']:>14.1%}"
    )

median_ke = rdf["cost_of_equity"].median()
min_ke = rdf["cost_of_equity"].min()
max_ke = rdf["cost_of_equity"].max()
print(f"\nMedian cost of equity: {median_ke:.1%}")
print(f"Range: {min_ke:.1%} to {max_ke:.1%}")
