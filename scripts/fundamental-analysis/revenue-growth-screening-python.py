# Full write-up: https://xfinlink.com/blog/revenue-growth-screening-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
