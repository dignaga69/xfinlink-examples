# How to Screen Tech Stocks by Revenue Growth in Python

Revenue growth is the top-line signal that matters most for growth stocks — it tells you if the company is actually getting bigger, regardless of margin tricks or one-time gains. Screening by YoY revenue growth and comparing it to earnings growth reveals which companies are scaling profitably and which are growing at the expense of profitability.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# 10 large-cap tech/growth stocks
tickers = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META",
    "CRM", "ADBE", "NOW", "PLTR",
]

# Get revenue and net income for the last 3 annual periods
fund = xfl.fundamentals(tickers, period_type="annual", fields=["revenue", "net_income"], period="3y")

# Keep the 2 most recent annual periods per ticker to compute YoY growth
recent = fund.sort_values("period_end").groupby("ticker").tail(2)

growth = []
for ticker in recent["ticker"].unique():
    rows = recent[recent["ticker"] == ticker].sort_values("period_end")
    if len(rows) < 2:
        continue
    prev, curr = rows.iloc[0], rows.iloc[1]
    if prev["revenue"] and prev["revenue"] > 0:
        rev_growth = (curr["revenue"] - prev["revenue"]) / prev["revenue"]
    else:
        rev_growth = None
    if prev["net_income"] and prev["net_income"] != 0:
        ni_growth = (curr["net_income"] - prev["net_income"]) / abs(prev["net_income"])
    else:
        ni_growth = None
    growth.append({
        "ticker": ticker,
        "entity_name": curr["entity_name"],
        "revenue": curr["revenue"],
        "rev_growth": rev_growth,
        "ni_growth": ni_growth,
    })

gdf = pd.DataFrame(growth).sort_values("rev_growth", ascending=False)

print("=== Revenue Growth Ranking (YoY, Most Recent Annual) ===")
for _, r in gdf.iterrows():
    rev_m = f"{r['revenue']/1e3:.0f}B" if r["revenue"] else "N/A"
    rg = f"{r['rev_growth']:.1%}" if r["rev_growth"] is not None else "N/A"
    ng = f"{r['ni_growth']:.1%}" if r["ni_growth"] is not None else "N/A"
    print(f"  {r['ticker']:5s}  rev={rev_m:>7s}  rev_growth={rg:>8s}  ni_growth={ng:>8s}")
print()

# Flag: high revenue growth but declining earnings
traps = gdf[(gdf["rev_growth"].notna()) & (gdf["rev_growth"] > 0.05) & (gdf["ni_growth"].notna()) & (gdf["ni_growth"] < 0)]
print("=== Growth Traps: Revenue Up but Earnings Down ===")
if len(traps) > 0:
    for _, r in traps.iterrows():
        print(f"  {r['ticker']}: revenue +{r['rev_growth']:.1%} but net income {r['ni_growth']:.1%}")
else:
    print("  None found — all growers are also earning more")
```

**Output:**

```
=== Revenue Growth Ranking (YoY, Most Recent Annual) ===
  NVDA   rev=   216B  rev_growth=   65.5%  ni_growth=   64.7%
  PLTR   rev=     4B  rev_growth=   56.2%  ni_growth=  251.6%
  META   rev=   201B  rev_growth=   22.2%  ni_growth=   -3.1%
  NOW    rev=    13B  rev_growth=   20.9%  ni_growth=   22.7%
  GOOG   rev=   403B  rev_growth=   15.1%  ni_growth=   32.0%
  MSFT   rev=   282B  rev_growth=   14.9%  ni_growth=   15.5%
  AMZN   rev=   717B  rev_growth=   12.4%  ni_growth=   31.1%
  ADBE   rev=    24B  rev_growth=   10.5%  ni_growth=   28.2%
  CRM    rev=    38B  rev_growth=    8.7%  ni_growth=   49.8%
  AAPL   rev=   416B  rev_growth=    6.4%  ni_growth=   19.5%

=== Growth Traps: Revenue Up but Earnings Down ===
  META: revenue +22.2% but net income -3.1%
```

NVDA leads with 65.5% revenue growth — and its earnings kept pace at +64.7%, showing the growth is real and profitable. PLTR is the outlier story: 56% revenue growth with 252% earnings growth, meaning it flipped from marginally profitable to highly profitable at scale. The one flag is META: revenue grew 22% but net income actually declined 3.1%, likely due to massive AI infrastructure spending. That's not necessarily bad — it might be strategic investment — but it's the kind of divergence a growth screen should catch.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
