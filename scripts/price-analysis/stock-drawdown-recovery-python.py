# Full write-up: https://xfinlink.com/blog/stock-drawdown-recovery-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
