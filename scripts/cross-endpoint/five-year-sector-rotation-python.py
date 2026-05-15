# Full write-up: https://xfinlink.com/blog/five-year-sector-rotation-python

import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
sectors = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLI": "Industrials",
    "XLY": "ConsDisc",
    "XLP": "ConsStaples",
    "XLU": "Utilities",
}
rf_annual = 0.03  # 3% avg risk-free rate over 5Y period

# -- Fetch 5Y daily returns -------------------------------------------------
tickers = list(sectors.keys())
df = xfl.prices(tickers, start="2021-01-01", end="2025-12-31", fields=["return_daily"])

# -- Compute performance metrics per sector ----------------------------------
results = []

for ticker in tickers:
    r = df[df["ticker"] == ticker]["return_daily"].dropna()
    total_return = (1 + r).prod() - 1
    n_years = len(r) / 252
    ann_return = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0
    ann_vol = r.std() * np.sqrt(252)
    sharpe = (ann_return - rf_annual) / ann_vol if ann_vol > 0 else 0

    results.append({
        "sector": sectors[ticker],
        "ticker": ticker,
        "total_return": total_return,
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
    })

rdf = pd.DataFrame(results).sort_values("total_return", ascending=False)

print("=== 5-Year Sector Total Return Ranking (2021-2025) ===")
header = f"{'Sector':14s}  {'Ticker':>6s}  {'5Y Total':>9s}  {'Ann Ret':>8s}  {'Ann Vol':>8s}  {'Sharpe':>7s}"
print(header)
print("-" * 60)

for _, r in rdf.iterrows():
    print(
        f"{r['sector']:14s}  {r['ticker']:>6s}  {r['total_return']:>+8.1%}  "
        f"{r['ann_return']:>+7.1%}  {r['ann_vol']:>7.1%}  {r['sharpe']:>+6.2f}"
    )

best = rdf.iloc[0]
worst = rdf.iloc[-1]
spread = best["total_return"] - worst["total_return"]
print(f"\n5-year sector spread: {spread:.0%} ({best['sector']} vs {worst['sector']})")
