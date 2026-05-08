# How to Compare Profitability Across Mega-Cap Tech Stocks in Python

Not all tech companies are equally profitable. NVDA prints a 56% net margin while AMZN barely clears 10%. Understanding the margin structure — where the money goes between gross profit and net income — reveals which companies have real pricing power and which are spending heavily to grow. Here's how to rank the Magnificent Six by margins, ROE, and ROIC.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== Mega-Cap Tech Profitability (Most Recent Annual) ===
ticker        entity_name period_end  gross_margin  operating_margin  net_margin      roe      roa
  NVDA        NVIDIA CORP 2026-01-25      0.710681          0.603817    0.556025 0.763333 0.580586
  MSFT     MICROSOFT CORP 2025-06-30      0.688237          0.456220    0.361460 0.296472 0.164510
  GOOG       ALPHABET INC 2025-12-31      0.596523          0.320326    0.328099 0.318279 0.222030
  META Meta Platforms Inc 2025-12-31      0.819994          0.414379    0.300837 0.278297 0.165176
  AAPL          Apple Inc 2025-09-27      0.469052          0.319708    0.269151 1.519130 0.311796
  AMZN     AMAZON COM INC 2025-12-31      0.502857          0.111553    0.108338 0.188948 0.094946

=== Return on Invested Capital (ROIC) Ranking ===
ticker        entity_name     roic
  NVDA        NVIDIA CORP 0.729972
  GOOG       ALPHABET INC 0.287458
  MSFT     MICROSOFT CORP 0.270354
  META Meta Platforms Inc 0.222181
  AMZN     AMAZON COM INC 0.166697
  AAPL          Apple Inc      NaN

=== Margin Efficiency (Gross - Net = overhead eaten) ===
  NVDA   gross=71.1%  net=55.6%  overhead=15.5%
  AAPL   gross=46.9%  net=26.9%  overhead=20.0%
  GOOG   gross=59.7%  net=32.8%  overhead=26.8%
  MSFT   gross=68.8%  net=36.1%  overhead=32.7%
  AMZN   gross=50.3%  net=10.8%  overhead=39.5%
  META   gross=82.0%  net=30.1%  overhead=51.9%
```

NVDA dominates every profitability metric — 56% net margin, 73% ROIC, and only 15.5% of its gross profit consumed by overhead. The margin efficiency ranking is the most revealing number here. META has the highest gross margin at 82% but the worst efficiency: 51.9 percentage points are consumed between gross profit and net income, mostly by massive R&D and infrastructure spending on AI. AAPL's efficiency is second only to NVDA despite having the lowest gross margin in the group — Apple doesn't waste money between the lines.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
