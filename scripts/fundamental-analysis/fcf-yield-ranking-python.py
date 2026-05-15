# Full write-up: https://xfinlink.com/blog/fcf-yield-ranking-python

import xfinlink as xfl
import pandas as pd

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
# Large-cap stocks across sectors (JPM excluded -- banks lack traditional FCF)
tickers = ["AAPL", "MSFT", "XOM", "UNH", "PG", "HD", "ABBV", "MRK", "CAT"]

# -- Fetch FCF per share and PE ratio from metrics --------------------------
metrics = xfl.metrics(tickers, fields=["fcf_per_share", "pe_ratio"])

# -- Fetch latest price -----------------------------------------------------
prices = xfl.prices(tickers, period="1d")

# -- Merge and compute FCF yield --------------------------------------------
results = []

for ticker in tickers:
    m = metrics[metrics["ticker"] == ticker].iloc[-1]
    p = prices[prices["ticker"] == ticker].iloc[-1]

    fcf_ps = m["fcf_per_share"]
    price = p["close"]
    pe = m["pe_ratio"]

    if pd.isna(fcf_ps) or pd.isna(price) or price == 0:
        continue

    fcf_yield = fcf_ps / price
    e_yield = 1 / pe if pe and pe != 0 else 0.0

    results.append({
        "ticker": ticker,
        "fcf_per_share": fcf_ps,
        "price": price,
        "fcf_yield": fcf_yield,
        "pe": pe,
        "e_yield": e_yield,
    })

rdf = pd.DataFrame(results).sort_values("fcf_yield", ascending=False)

print("=== Free Cash Flow Yield Ranking (Latest Annual) ===")
header = f"{'Ticker':6s}  {'FCF/Share':>10s}  {'Price':>10s}  {'FCF Yield':>10s}  {'PE':>7s}  {'E Yield':>8s}"
print(header)
print("-" * 55)

for _, r in rdf.iterrows():
    print(
        f"{r['ticker']:6s}  {r['fcf_per_share']:>10.2f}  {r['price']:>10.2f}  "
        f"{r['fcf_yield']:>9.1%}  {r['pe']:>7.1f}  {r['e_yield']:>7.1%}"
    )
