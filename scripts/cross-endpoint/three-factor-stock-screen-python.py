# Full write-up: https://xfinlink.com/blog/three-factor-stock-screen-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
