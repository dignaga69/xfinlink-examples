# How to Calculate Max Drawdown and Recovery Time for Any Stock in Python

## What's the question?

Standard volatility measures treat upside and downside risk symmetrically, but investors experience them differently. A 20% gain and a 20% loss have asymmetric consequences: the loss requires a 25% subsequent gain just to break even. Maximum drawdown -- the largest peak-to-trough decline in a stock's price over a given period -- captures the worst-case loss scenario an investor would have experienced. Combined with recovery time (the number of days from the trough back to the previous peak), it answers a concrete question: if you bought at the worst possible moment, how severe was the loss and how long did it take to recover?

## The approach

For each stock, we compute the running cumulative maximum of the closing price, then calculate the drawdown at each date as the percentage difference between the current price and the cumulative maximum. The minimum drawdown value represents the maximum drawdown. Recovery time is measured as the number of calendar days from the drawdown trough until the stock first reaches or exceeds its previous peak.

Six stocks are divided into two groups -- growth (NVDA, TSLA, AAPL) and defensive (JNJ, PG, KO) -- to test whether the conventional wisdom holds that defensive stocks experience shallower drawdowns and faster recoveries.

## Code

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Compare drawdown profiles across growth vs defensive stocks
tickers = ["NVDA", "TSLA", "AAPL", "JNJ", "PG", "KO"]
df = xfl.prices(tickers, period="1y", fields=["close"])

results = []
for ticker in tickers:
    t = df[df["ticker"] == ticker].sort_values("date").copy()
    t["cummax"] = t["close"].cummax()
    t["drawdown"] = t["close"] / t["cummax"] - 1

    max_dd = t["drawdown"].min()
    max_dd_date = t.loc[t["drawdown"].idxmin(), "date"].strftime("%Y-%m-%d")

    # Recovery: how long from max drawdown to new high?
    dd_idx = t["drawdown"].idxmin()
    after_dd = t.loc[dd_idx:]
    recovered = after_dd[after_dd["drawdown"] >= 0]
    if len(recovered) > 0:
        recovery_days = (recovered.iloc[0]["date"] - t.loc[dd_idx, "date"]).days
        recovery_str = f"{recovery_days}d"
    else:
        recovery_str = "not yet"

    current_dd = t["drawdown"].iloc[-1]
    results.append({
        "ticker": ticker,
        "max_drawdown": f"{max_dd:.1%}",
        "max_dd_date": max_dd_date,
        "recovery": recovery_str,
        "current_dd": f"{current_dd:.1%}",
    })

result_df = pd.DataFrame(results)
print("=== 1-Year Drawdown Analysis: Growth vs Defensive ===")
print(result_df.to_string(index=False))
print()

# Average drawdown by group
growth = [r for r in results if r["ticker"] in ["NVDA", "TSLA", "AAPL"]]
defensive = [r for r in results if r["ticker"] in ["JNJ", "PG", "KO"]]
g_avg = np.mean([float(r["max_drawdown"].strip("%")) / 100 for r in growth])
d_avg = np.mean([float(r["max_drawdown"].strip("%")) / 100 for r in defensive])
print(f"Growth avg max drawdown:    {g_avg:.1%}")
print(f"Defensive avg max drawdown: {d_avg:.1%}")
print(f"Growth stocks drew down {abs(g_avg / d_avg):.1f}x more than defensive stocks")
```

## Output

```
=== 1-Year Drawdown Analysis: Growth vs Defensive ===
ticker max_drawdown max_dd_date recovery current_dd
  NVDA       -20.2%  2026-03-30      25d      -2.4%
  TSLA       -29.9%  2026-04-08  not yet     -15.9%
  AAPL       -13.8%  2026-03-30      37d      -0.0%
   JNJ       -10.5%  2026-05-07  not yet     -10.5%
    PG       -18.7%  2026-01-07  not yet     -14.0%
    KO        -9.2%  2025-09-26      56d      -3.8%

Growth avg max drawdown:    -21.3%
Defensive avg max drawdown: -12.8%
Growth stocks drew down 1.7x more than defensive stocks
```

## What this tells us

On average, the growth stocks experienced drawdowns 1.7 times deeper than the defensive stocks (-21.3% versus -12.8%), which aligns with the conventional relationship between beta and downside risk. However, the individual cases reveal more nuance.

TSLA's -29.9% drawdown from April 8 remains unrecovered, while NVDA's -20.2% drawdown recovered in just 25 days. The difference in recovery speed between two high-beta stocks reflects the market's differing assessments of their fundamental trajectories rather than their risk profiles alone.

PG presents the most instructive case. Typically classified as a defensive stock, it experienced a -18.7% drawdown from its January high that has not yet recovered. This drawdown is nearly as severe as NVDA's (-20.2%), which did recover. The result demonstrates that sector classification is not a guarantee of downside protection in any specific period. Defensive stocks tend to draw down less on average, but individual defensive names can experience drawdowns comparable to growth stocks during periods of sector rotation or company-specific headwinds.

## So what?

Maximum drawdown is a more intuitive risk metric than volatility for evaluating the investor experience, because it measures the actual worst-case loss rather than a statistical average of daily moves. When constructing a portfolio, pair drawdown analysis with recovery time to understand the full risk profile: a deep drawdown that recovers in 25 days (NVDA) has different practical implications than a moderate drawdown that persists for months (PG). Position sizing based on historical maximum drawdown, rather than volatility alone, produces portfolios that are better calibrated to the losses an investor will actually face.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
