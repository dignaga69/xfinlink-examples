# Full write-up: https://xfinlink.com/blog/mega-cap-tech-profitability-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

# Compare profitability across mega-cap tech
tickers = ["AAPL", "MSFT", "GOOGL", "META", "AMZN", "NVDA"]

metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["gross_margin", "operating_margin", "net_margin", "roe", "roa", "roic"],
                      period="3y")

# Keep most recent per ticker
latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.sort_values("net_margin", ascending=False)

print("=== Mega-Cap Tech Profitability (Most Recent Annual) ===")
cols = ["ticker", "entity_name", "period_end", "gross_margin", "operating_margin", "net_margin", "roe", "roa"]
print(latest[cols].to_string(index=False))
print()

# Who's most capital-efficient? ROIC ranking
roic_rank = latest.sort_values("roic", ascending=False)
print("=== Return on Invested Capital (ROIC) Ranking ===")
print(roic_rank[["ticker", "entity_name", "roic"]].to_string(index=False))
print()

# Margin spread: gross - net = how much gets eaten by OpEx + taxes
latest_copy = latest.copy()
latest_copy["margin_spread"] = latest_copy["gross_margin"] - latest_copy["net_margin"]
spread = latest_copy.sort_values("margin_spread")
print("=== Margin Efficiency (Gross - Net = overhead eaten) ===")
for _, row in spread.iterrows():
    print(f"  {row['ticker']:5s}  gross={row['gross_margin']:.1%}  net={row['net_margin']:.1%}  overhead={row['margin_spread']:.1%}")
