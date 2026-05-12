# Full write-up: https://xfinlink.com/blog/balance-sheet-health-screening-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "JNJ", "XOM", "T"]

metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["current_ratio", "quick_ratio", "debt_to_equity", "debt_to_assets", "interest_coverage", "cash_per_share"],
                      period="3y")

latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.sort_values("current_ratio", ascending=False)

print("=== Balance Sheet Health: Liquidity Ratios ===")
print(latest[["ticker", "entity_name", "current_ratio", "quick_ratio", "cash_per_share"]].to_string(index=False))
print()

print("=== Leverage Ratios ===")
lev = latest.sort_values("debt_to_equity", ascending=True)
print(lev[["ticker", "entity_name", "debt_to_equity", "debt_to_assets", "interest_coverage"]].to_string(index=False))
print()

# Flag risky balance sheets: current ratio < 1 or debt/equity > 2
risky = latest[(latest["current_ratio"] < 1) | (latest["debt_to_equity"] > 2)]
print("=== Watch List: Weak Balance Sheets ===")
if len(risky) > 0:
    for _, r in risky.iterrows():
        flags = []
        if r["current_ratio"] < 1:
            flags.append(f"current_ratio={r['current_ratio']:.2f}")
        if r["debt_to_equity"] is not None and r["debt_to_equity"] > 2:
            flags.append(f"debt/equity={r['debt_to_equity']:.2f}")
        print(f"  {r['ticker']}: {', '.join(flags)}")
else:
    print("  All clear")
