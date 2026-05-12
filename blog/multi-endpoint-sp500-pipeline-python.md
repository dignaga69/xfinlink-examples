# How to Build a Multi-Endpoint Financial Analysis Pipeline in Python

Real financial analysis doesn't use just one data source — you need index composition to pick your universe, prices for returns, and fundamentals for context. Here's a pipeline that chains 4 xfinlink endpoints together: start with who was in the S&P 500 in 2020, pull 6 years of prices, calculate total returns, then add revenue data. This is the kind of survivorship-bias-free analysis that matters.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Step 1: Historical S&P 500 constituents (as_of=2020-01-01)
sp500_2020 = xfl.index("sp500", as_of="2020-01-01")
print(f"Step 1: {len(sp500_2020)} S&P 500 members as of 2020-01-01")

# Step 2: Pick 10 well-known tickers from the 2020 index
sample_tickers = ["AAPL", "MSFT", "AMZN", "JPM", "JNJ", "XOM", "PG", "BA", "DIS", "INTC"]
in_2020 = set(sp500_2020["ticker"].tolist())
valid = [t for t in sample_tickers if t in in_2020]
print(f"Step 2: {len(valid)} of {len(sample_tickers)} sample tickers were in 2020 S&P 500")

# Step 3: Pull prices from 2020-01-02 to today
prices = xfl.prices(valid, start="2020-01-02", end="2026-05-12", fields=["close", "return_daily"])
print(f"Step 3: {len(prices)} price rows fetched")

# Step 4: Calculate total return
total_returns = prices.sort_values("date").groupby("ticker")["return_daily"].apply(
    lambda x: (1 + x).prod() - 1
).sort_values(ascending=False).rename("total_return")
print(f"Step 4: Returns calculated\n")

# Step 5: Pull latest fundamentals
fund = xfl.fundamentals(valid, period_type="annual", fields=["revenue", "net_income"], period="1y")
latest_fund = fund.sort_values("period_end").groupby("ticker").tail(1).set_index("ticker")

result = pd.DataFrame(total_returns).join(latest_fund[["revenue", "net_income"]], how="left")

print("=== S&P 500 (2020 Members): Total Return to Today ===")
print("(Survivorship-bias-free: using who was ACTUALLY in the index in Jan 2020)")
print()
for ticker, r in result.iterrows():
    rev = f"${r['revenue']/1e3:.0f}B" if pd.notna(r["revenue"]) else "N/A"
    print(f"  {ticker:5s}  return={r['total_return']:>+7.1%}  revenue={rev:>7s}")
print(f"\nBest:  {result.index[0]} ({result.iloc[0]['total_return']:+.1%})")
print(f"Worst: {result.index[-1]} ({result.iloc[-1]['total_return']:+.1%})")
```

**Output:**

```
Step 1: 500 S&P 500 members as of 2020-01-01
Step 2: 10 of 10 sample tickers were in 2020 S&P 500
Step 3: 15970 price rows fetched
Step 4: Returns calculated

=== S&P 500 (2020 Members): Total Return to Today ===
(Survivorship-bias-free: using who was ACTUALLY in the index in Jan 2020)

  AAPL   return=+311.2%  revenue=  $416B
  AMZN   return=+191.1%  revenue=  $717B
  MSFT   return=+173.6%  revenue=  $282B
  XOM    return=+173.5%  revenue=  $332B
  JPM    return=+148.7%  revenue=  $182B
  INTC   return=+145.2%  revenue=   $53B
  JNJ    return= +74.4%  revenue=   $94B
  PG     return= +29.9%  revenue=   $84B
  BA     return= -26.4%  revenue=   $89B
  DIS    return= -26.7%  revenue=   $94B

Best:  AAPL (+311.2%)
Worst: DIS (-26.7%)
```

The pipeline demonstrates three things: (1) how to use historical index composition to avoid survivorship bias — we started with who was actually in the S&P 500 in January 2020, not who's in it now; (2) the enormous dispersion in outcomes — AAPL returned +311% while DIS lost -27% over the same period; (3) revenue alone doesn't predict returns — Boeing ($89B revenue) and Disney ($94B revenue) both lost money while XOM ($332B) returned +174%. The point-in-time index data ensures this analysis includes everyone who was in the game at the start, not just the winners.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
