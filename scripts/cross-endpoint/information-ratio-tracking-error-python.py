# Full write-up: https://xfinlink.com/blog/information-ratio-tracking-error-python

import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "XOM", "JNJ", "JPM"]
benchmark = "SPY"

# -- Fetch 1Y daily returns -------------------------------------------------
df = xfl.prices(tickers + [benchmark], period="1y", fields=["return_daily"])
pivot = df.pivot_table(index="date", columns="ticker", values="return_daily").dropna()

# -- Benchmark annualized return --------------------------------------------
spy_total = (1 + pivot[benchmark]).prod() - 1
print(f"=== Information Ratio vs SPY (1Y) ===")
print(f"Benchmark (SPY) annualized return: {spy_total:.1%}")
print()

# -- Compute IR for each stock ----------------------------------------------
results = []

for ticker in tickers:
    stock_total = (1 + pivot[ticker]).prod() - 1
    active_daily = pivot[ticker] - pivot[benchmark]
    active_return = stock_total - spy_total
    tracking_error = active_daily.std() * np.sqrt(252)
    ir = active_return / tracking_error if tracking_error > 0 else 0.0
    hit_rate = (active_daily > 0).mean()

    results.append({
        "ticker": ticker,
        "total_return": stock_total,
        "active_return": active_return,
        "tracking_error": tracking_error,
        "ir": ir,
        "hit_rate": hit_rate,
    })

rdf = pd.DataFrame(results).sort_values("ir", ascending=False)

header = f"{'Ticker':6s}  {'Return':>8s}  {'Active':>7s}  {'TE':>7s}  {'IR':>6s}  {'Hit%':>5s}"
print(header)
print("-" * 44)

for _, r in rdf.iterrows():
    print(
        f"{r['ticker']:6s}  {r['total_return']:>+7.1%}  {r['active_return']:>+6.1%}  "
        f"{r['tracking_error']:>6.1%}  {r['ir']:>+5.2f}  "
        f"  {r['hit_rate']:>3.0%}"
    )

print()
print("IR interpretation:")
print("  > +0.5: strong outperformance | -0.5 to +0.5: noise | < -0.5: consistent underperformance")
