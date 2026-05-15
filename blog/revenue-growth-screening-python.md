# How to Screen Tech Stocks by Revenue Growth in Python

## What's the question?

Revenue growth -- the year-over-year percentage change in total sales -- is the most direct measure of whether a business is expanding. Unlike earnings, which can increase through cost-cutting, asset disposals, or favorable accounting treatments, revenue growth reflects actual demand for a company's products and services. However, revenue growth in isolation is insufficient as an investment signal. A company can grow revenue rapidly while its earnings decline, either because it is investing aggressively in future capacity (strategic spending) or because its cost structure is deteriorating (margin erosion). Among ten large-cap technology companies, which are growing the fastest, and does that growth translate into proportionate earnings improvement?

## The approach

The two most recent annual periods for each company are retrieved from the xfinlink fundamentals endpoint, and year-over-year growth rates are computed for both revenue and net income. Comparing these two rates reveals three distinct operating patterns: profitable scaling (both metrics grow at similar rates), leveraged profitability (earnings growth substantially exceeds revenue growth, indicating margin expansion), and investment-phase growth (revenue grows while earnings contract, indicating heavy reinvestment). A "growth trap" flag identifies companies where revenue increased by more than 5% but net income declined -- a divergence that warrants investigation into whether the earnings pressure stems from strategic capital deployment or structural cost problems.

## Code

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

## Output

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

## What this tells us

NVIDIA leads the ranking at 65.5% revenue growth with net income growing at a nearly identical 64.7%. This parallel movement indicates that the company is scaling without margin compression -- each incremental dollar of revenue contributes proportionately to earnings. This pattern is characteristic of a business with strong pricing power and a cost structure that scales efficiently with volume.

Palantir demonstrates the most pronounced operating leverage in the group. Revenue grew 56.2% while net income expanded 251.6%, indicating that the company has crossed an inflection point where its largely fixed cost base (primarily engineering and sales personnel) absorbs incremental revenue at minimal marginal cost. This dynamic is typical of enterprise software businesses that reach sufficient scale to amortize their development costs across a growing customer base.

Meta is the only company flagged by the growth trap screen. Revenue increased 22.2% while net income declined 3.1%, a divergence driven by substantial capital expenditure on AI infrastructure including data centers and custom silicon. Determining whether this represents a strategic investment with future returns or a structural margin decline requires monitoring whether the spending translates into revenue acceleration in subsequent periods.

The remaining seven companies exhibit a mature growth profile in which earnings growth exceeds revenue growth. Alphabet, Amazon, Adobe, and Salesforce all demonstrate this margin expansion pattern, indicating improving operational efficiency at scale. Apple, though posting the lowest revenue growth at 6.4%, grew earnings at 19.5% -- a 3x ratio that reflects significant cost discipline and share buyback accretion.

## So what?

Revenue growth is most informative when evaluated alongside earnings growth as a quality filter. The ratio between the two -- sometimes termed operating leverage -- distinguishes companies where growth is accretive to profitability from those where it is dilutive. A company growing revenue at 20% with declining earnings is in a fundamentally different position than one growing revenue at 10% with earnings expanding at 30%. When constructing a growth screen, flag any company where revenue growth and earnings growth diverge materially, and investigate the underlying cause before interpreting the revenue figure as a positive signal.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
