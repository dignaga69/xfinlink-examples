# Full write-up: https://xfinlink.com/blog/dividend-yield-screening-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

# Dividend aristocrats and other well-known dividend payers
tickers = [
    "JNJ", "PG", "KO", "PEP", "MCD",
    "MMM", "T", "VZ", "XOM", "CVX",
    "ABBV", "IBM", "HD", "WMT", "LOW",
]

# Get dividend yield and payout metrics
metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["dividend_yield", "pe_ratio", "roe", "fcf_per_share", "earnings_yield"],
                      period="3y")

# Keep most recent period per ticker
latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.dropna(subset=["dividend_yield"])
latest = latest.sort_values("dividend_yield", ascending=False)

print("=== Dividend Yield Ranking (Annual, Most Recent) ===")
cols = ["ticker", "entity_name", "period_end", "dividend_yield", "pe_ratio", "roe"]
print(latest[cols].to_string(index=False))
print()

# Calculate a simple quality score: yield > 2%, PE < 25, ROE > 15%
quality = latest[
    (latest["dividend_yield"] > 0.02) &
    (latest["pe_ratio"] > 0) &
    (latest["pe_ratio"] < 25) &
    (latest["roe"] > 0.15)
].copy()
print("=== Quality Dividend Stocks (yield>2%, PE<25, ROE>15%) ===")
print(quality[cols].to_string(index=False) if len(quality) > 0 else "None found")
