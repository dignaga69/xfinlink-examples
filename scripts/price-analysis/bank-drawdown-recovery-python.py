# Full write-up: https://xfinlink.com/blog/bank-drawdown-recovery-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- 5 major bank stocks -------------------------------------------------
tickers = ["BAC", "GS", "MS", "WFC", "C"]

# -- Fetch 1Y of daily data ----------------------------------------------
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

# -- Compute drawdown metrics per ticker ----------------------------------
print("=== Bank Stock Drawdown Analysis (1Y) ===")

results = []
for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").reset_index(drop=True)
    if df.empty:
        continue

    entity_name = df["entity_name"].iloc[0]
    returns = df["return_daily"].dropna()
    closes = df["close"]

    # Cumulative return series
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak

    # Max drawdown and date
    max_dd = drawdown.min()
    max_dd_idx = drawdown.idxmin()
    max_dd_date = df.loc[max_dd_idx, "date"]

    # Recovery: how many trading days from max drawdown back to prior peak
    post_dd = drawdown.iloc[max_dd_idx:]
    recovered = post_dd[post_dd >= 0]
    if len(recovered) > 0:
        recovery_idx = recovered.index[0]
        recovery_days = recovery_idx - max_dd_idx
        recovery_str = f"{recovery_days:5d}d"
    else:
        recovery_str = "not yet"

    # Current drawdown (last value in drawdown series)
    current_dd = drawdown.iloc[-1]

    # 1Y compound return
    ret_1y = (1 + returns).prod() - 1

    results.append({
        "ticker": ticker,
        "entity_name": entity_name,
        "max_dd": max_dd,
        "max_dd_date": max_dd_date,
        "recovery": recovery_str,
        "current_dd": current_dd,
        "return_1y": ret_1y,
    })

# Sort by max drawdown (deepest first)
results.sort(key=lambda x: x["max_dd"])

for r in results:
    name = r["entity_name"][:22]
    print(
        f"  {r['ticker']:<6} {name:<22}"
        f"  max_dd={r['max_dd']:+.1%}"
        f"  on {r['max_dd_date']}"
        f"  recovery={r['recovery']}"
        f"  now={r['current_dd']:+.1%}"
        f"  1y={r['return_1y']:+.1%}"
    )

# Sector average
import numpy as np
avg_dd = np.mean([r["max_dd"] for r in results])
print(f"\nAvg max drawdown: {avg_dd:.1%}")
