# How to Build a Multi-Factor Stock Screen in Python (Value + Momentum + Quality)

## What's the question?

Can combining multiple investment factors into a single composite score produce better stock selection than relying on any single factor alone? Single-factor screens — ranking stocks by price-to-earnings ratio, or by trailing returns, or by profitability — each capture one dimension of a stock's attractiveness. But a stock that is cheap may be cheap for a reason (declining business), and a stock with strong momentum may be overvalued. Multi-factor models, widely used by quantitative hedge funds since the early 1990s, attempt to identify companies that score well across multiple independent dimensions simultaneously.

## The approach

We construct a three-factor composite score using value, momentum, and quality:

- **Value** is measured by earnings yield (the inverse of the price-to-earnings ratio), where a higher yield indicates a cheaper stock relative to its earnings.
- **Momentum** is the compounded 6-month total return, capturing the persistence of recent price trends.
- **Quality** is measured by return on equity (ROE), defined as net income divided by shareholders' equity, which quantifies how effectively a company converts equity capital into profit.

Each factor is z-score normalized across the universe of 15 stocks (subtract the mean, divide by the standard deviation) so that all three factors are on the same scale regardless of their native units. The composite score is the weighted average of the three z-scores, with approximately equal weighting: 33% value, 34% momentum, 33% quality. Stocks are ranked by the composite score from highest (most attractive across all three dimensions) to lowest.

## Code

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

## Output

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

## What this tells us

XOM ranks first not because it leads any individual factor but because it scores above average on all three: reasonable earnings yield (0.046), the strongest 6-month momentum (+26.6%), and positive ROE. This illustrates the core principle of multi-factor investing — identifying stocks that are consistently above average rather than extreme on one dimension.

Two important caveats emerge from the data. First, AAPL's ROE of 1.519 (152%) and HD's ROE of 1.105 (111%) are mathematically correct but economically misleading. Both companies have aggressively repurchased shares, reducing their book equity to very small amounts. When net income of $112B (AAPL) is divided by book equity of approximately $62B, the resulting ROE is inflated by capital structure decisions rather than operating performance. A more robust quality metric for companies with buyback-depleted equity would be return on invested capital (ROIC), which uses total capital (debt plus equity) as the denominator.

Second, ABBV's last-place composite score (-1.67) is driven almost entirely by its negative ROE of -1.292, which results from negative shareholders' equity following the Allergan acquisition. This is an accounting artifact of acquisition accounting, not an indication of operating quality. MSFT scores poorly because its 6-month momentum is the weakest in the group at -18.4%, dragging its composite score down despite adequate value and quality metrics.

## So what?

Multi-factor screens are a starting point for analysis, not a finished investment process. The model presented here uses equal weighting and a small universe — both limitations that a production implementation would address. More critically, the ROE-based quality factor breaks down for companies with negative or near-zero book equity, which is increasingly common among large-cap companies with aggressive buyback programs. Practitioners should consider alternative quality metrics (ROIC, operating margin stability, accrual ratios) and test whether the composite score has predictive power out of sample before allocating capital based on the rankings.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
