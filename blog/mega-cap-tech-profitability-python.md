# How to Compare Profitability Across Mega-Cap Tech Stocks in Python

## What's the question?

The six largest technology companies by market capitalization -- Apple, Microsoft, Alphabet, Meta, Amazon, and NVIDIA -- are often grouped together, but their profitability structures are fundamentally different. NVIDIA converts 56% of its revenue into net income, while Amazon converts just 11%. The gap between gross margin and net margin reveals where money is consumed between the top line and the bottom line: operating expenses, research and development, sales and marketing, taxes, and interest. Which of these companies have genuine pricing power, and which are investing heavily at the expense of current profitability?

## The approach

Three margin metrics provide the profitability waterfall. Gross margin (revenue minus cost of goods sold, divided by revenue) measures pricing power and production efficiency. Operating margin (operating income divided by revenue) shows what remains after operating expenses. Net margin (net income divided by revenue) is the final measure of profitability after all expenses, taxes, and interest.

The spread between gross margin and net margin -- which we term overhead absorption -- quantifies how much of the initial pricing advantage is consumed by the company's cost structure. A company with high gross margin but low net margin is spending heavily on activities between production and the bottom line.

Two capital efficiency metrics complement the margin analysis: return on equity (ROE, net income divided by shareholders' equity) and return on invested capital (ROIC, a measure of how efficiently a company generates returns on all capital deployed, including debt).

## Code

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

## Output

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

## What this tells us

NVIDIA dominates every profitability metric: 56% net margin, 73% ROIC, and only 15.5 percentage points of overhead absorption. This reflects the economics of a semiconductor design company during a period of unprecedented demand for its products -- high pricing power, fabless manufacturing (NVIDIA designs chips but outsources fabrication), and massive operating leverage as revenue scales against a relatively fixed cost base.

The overhead absorption ranking reveals structural differences that net margin alone obscures. Meta has the highest gross margin of any company in the group at 82%, yet it absorbs 51.9 percentage points between gross profit and net income -- the worst efficiency in the group. The gap is driven by massive capital expenditure on AI infrastructure and R&D, an investment strategy that compresses current profitability in pursuit of future capabilities.

Apple presents the inverse pattern. It has the lowest gross margin in the group (46.9%) because hardware manufacturing carries higher cost of goods sold than software or advertising. However, Apple's overhead absorption is just 20 percentage points, second only to NVIDIA. Apple operates with exceptional cost discipline between the production line and the bottom line.

## So what?

Gross margin measures pricing power; the gross-to-net spread measures organizational efficiency. A company with high gross margin and high overhead absorption is spending aggressively, which may reflect either strategic investment (as in Meta's AI buildout) or structural inefficiency. When evaluating technology companies, examine the full margin waterfall rather than any single metric. Net margin alone does not distinguish between a company that earns less because its products command lower prices (AAPL) and one that earns less because it spends more between the gross and net lines (META).

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
