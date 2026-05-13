# Full write-up: https://xfinlink.com/blog/energy-sector-volatility-python

import numpy as np
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# ── 6 energy stocks ──────────────────────────────────────────────────
tickers = ["XOM", "CVX", "COP", "SLB", "EOG", "MPC"]

# ── Fetch 1Y of daily data ───────────────────────────────────────────
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

# ── Compute volatility metrics per ticker ─────────────────────────────
print("=== Energy Sector Volatility Profile (1Y) ===")

results = []
for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").reset_index(drop=True)
    if df.empty:
        continue

    entity_name = df["entity_name"].iloc[0]
    returns = df["return_daily"].dropna()

    # Annualized volatility (std of daily returns * sqrt(252))
    ann_vol = returns.std() * np.sqrt(252)

    # 30-day rolling volatility (latest window)
    rolling_vol = returns.tail(30).std() * np.sqrt(252)

    # Max drawdown
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = ((cum - peak) / peak).min()

    # 1Y compound return
    ret_1y = (1 + returns).prod() - 1

    results.append({
        "ticker": ticker,
        "entity_name": entity_name,
        "ann_vol": ann_vol,
        "rolling_vol_30d": rolling_vol,
        "max_drawdown": drawdown,
        "return_1y": ret_1y,
    })

# Sort by annualized vol descending
results.sort(key=lambda x: x["ann_vol"], reverse=True)

for r in results:
    print(
        f"  {r['ticker']:<6} {r['entity_name']:<26}"
        f"  vol={r['ann_vol']:.1%}"
        f"  30d_vol={r['rolling_vol_30d']:.1%}"
        f"  drawdown={r['max_drawdown']:+.1%}"
        f"  return={r['return_1y']:+.1%}"
    )

# Sector average
avg_vol = np.mean([r["ann_vol"] for r in results])
print(f"\nSector avg volatility: {avg_vol:.1%}")
