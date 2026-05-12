# How to Build a Multi-Factor Stock Screen in Python (Value + Momentum + Quality)

Single-factor screens (just P/E, or just momentum) miss the full picture. Combining value, momentum, and quality into a composite score is what quantitative hedge funds have done since the 1990s. The idea: a cheap stock with strong momentum and high ROE is a better bet than a stock that's only cheap. Here's a simple 3-factor screen across 15 large caps.

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL",
    "JPM", "JNJ", "XOM", "PG", "HD", "COST", "UNH", "LLY", "ABBV",
]

# Factor 1: Value (earnings yield)
metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["earnings_yield", "roe"], period="3y")
val = metrics.sort_values("period_end").groupby("ticker").tail(1)[["ticker", "earnings_yield", "roe"]].set_index("ticker")

# Factor 2: Momentum (6-month return)
prices = xfl.prices(tickers, period="6mo", fields=["return_daily"])
mom = prices.sort_values("date").groupby("ticker")["return_daily"].apply(
    lambda x: (1 + x).prod() - 1
).rename("momentum_6mo")

# Combine and z-score normalize
combined = val.join(mom, how="inner").dropna()
for col in ["earnings_yield", "momentum_6mo", "roe"]:
    combined[f"{col}_z"] = (combined[col] - combined[col].mean()) / combined[col].std()

combined["composite_score"] = (
    combined["earnings_yield_z"] * 0.33 +
    combined["momentum_6mo_z"] * 0.34 +
    combined["roe_z"] * 0.33
)
combined = combined.sort_values("composite_score", ascending=False)

print("=== 3-Factor Composite: Value + Momentum + Quality ===")
print("(Weights: 33% earnings yield, 34% 6mo momentum, 33% ROE)")
print()
for ticker, r in combined.iterrows():
    print(f"  {ticker:5s}  yield={r['earnings_yield']:.3f}  mom6m={r['momentum_6mo']:>+6.1%}  roe={r['roe']:.3f}  score={r['composite_score']:>+5.2f}")
print(f"\nTop pick: {combined.index[0]} (composite={combined.iloc[0]['composite_score']:+.2f})")
print(f"Bottom:   {combined.index[-1]} (composite={combined.iloc[-1]['composite_score']:+.2f})")
```

**Output:**

```
=== 3-Factor Composite: Value + Momentum + Quality ===
(Weights: 33% earnings yield, 34% 6mo momentum, 33% ROE)

  XOM    yield=0.046  mom6m=+26.6%  roe=0.111  score=+0.73
  JNJ    yield=0.050  mom6m=+17.5%  roe=0.329  score=+0.69
  AAPL   yield=0.026  mom6m= +8.6%  roe=1.519  score=+0.58
  JPM    yield=0.071  mom6m= -5.3%  roe=0.157  score=+0.42
  UNH    yield=0.035  mom6m=+19.5%  roe=0.120  score=+0.29
  NVDA   yield=0.023  mom6m=+10.2%  roe=0.763  score=+0.14
  HD     yield=0.046  mom6m=-15.9%  roe=1.105  score=+0.12
  PG     yield=0.048  mom6m= -1.5%  roe=0.306  score=+0.11
  META   yield=0.046  mom6m= -5.2%  roe=0.278  score=-0.03
  LLY    yield=0.023  mom6m= +0.0%  roe=0.778  score=-0.12
  AMZN   yield=0.027  mom6m= +8.3%  roe=0.189  score=-0.13
  GOOG   yield=0.028  mom6m= +0.5%  roe=0.318  score=-0.24
  COST   yield=0.018  mom6m= +9.2%  roe=0.278  score=-0.24
  MSFT   yield=0.033  mom6m=-18.4%  roe=0.296  score=-0.65
  ABBV   yield=0.012  mom6m= -7.3%  roe=-1.292  score=-1.67

Top pick: XOM (composite=+0.73)
Bottom:   ABBV (composite=-1.67)
```

XOM tops the composite ranking — not because it leads any single factor, but because it scores above average on all three: reasonable earnings yield (0.046), the strongest 6-month momentum (+26.6%), and positive ROE. This is the power of multi-factor screens: they surface stocks that are consistently good rather than extreme on one dimension. One caveat: AAPL's ROE of 1.519 (152%) looks extreme but it's real — Apple has deliberately shrunk its book equity to ~$62B through massive buybacks, so net income of $112B divided by a tiny equity base produces an inflated ROE. HD has the same dynamic at 110%. These aren't "quality" signals in the traditional sense — they're capital structure artifacts. A more robust quality factor would use ROIC instead. ABBV's last-place finish is driven by deeply negative ROE (-1.29, from negative equity post-Allergan), and MSFT scores poorly because its 6-month momentum is the worst in the group (-18.4%).

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
