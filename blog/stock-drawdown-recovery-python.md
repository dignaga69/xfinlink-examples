# How to Calculate Max Drawdown and Recovery Time for Any Stock in Python

Max drawdown is the single best measure of downside risk — it tells you the worst peak-to-trough decline a stock experienced over a given period. Combined with recovery time, it answers the question every investor actually cares about: "If I bought at the worst possible moment, how bad would it get and how long until I'm whole again?" Here's how to calculate both for growth vs defensive stocks.

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

**Output:**

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

Growth stocks averaged a -21.3% max drawdown vs -12.8% for defensives — about 1.7x worse. TSLA's -29.9% drawdown from April 8 still hasn't recovered, while AAPL bounced back to its highs in just 37 days. The surprise is PG: usually the textbook "safe" stock, but it's down -18.7% from its January high and still hasn't recovered — worse than NVDA's -20.2%, which recovered in 25 days. Drawdown analysis often reveals that "safe" stocks aren't always safe, and "risky" stocks sometimes recover faster than you'd expect.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
