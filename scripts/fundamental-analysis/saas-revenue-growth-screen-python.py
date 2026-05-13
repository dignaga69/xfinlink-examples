# Full write-up: https://xfinlink.com/blog/saas-revenue-growth-screen-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- 6 SaaS / cloud stocks -----------------------------------------------
tickers = ["DDOG", "ZS", "CRWD", "NET", "MDB", "SNOW"]

# -- Fetch 3Y of quarterly fundamentals ----------------------------------
fundamentals = xfl.fundamentals(
    tickers,
    period="3y",
    fields=["revenue", "net_income", "operating_cash_flow"],
    period_type="annual",
)

# -- Compute YoY revenue growth, profitability, OCF margin ----------------
print("=== SaaS / Cloud Growth Screen (YoY Revenue Growth) ===")

results = []
for ticker in tickers:
    df = fundamentals[fundamentals["ticker"] == ticker].sort_values("period_end")
    if len(df) < 2:
        continue

    entity_name = df["entity_name"].iloc[-1]
    latest = df.iloc[-1]
    prior = df.iloc[-2]

    revenue = latest["revenue"]
    revenue_prior = prior["revenue"]
    growth = (revenue - revenue_prior) / revenue_prior if revenue_prior else 0

    net_income = latest["net_income"]
    profitable = net_income > 0 if net_income is not None else False

    ocf = latest["operating_cash_flow"]
    ocf_margin = ocf / revenue if revenue and ocf else 0

    results.append({
        "ticker": ticker,
        "entity_name": entity_name,
        "revenue": revenue,
        "growth": growth,
        "profitable": profitable,
        "ocf_margin": ocf_margin,
    })

# Sort by growth descending
results.sort(key=lambda x: x["growth"], reverse=True)

for r in results:
    name = r["entity_name"][:22]
    prof = "YES" if r["profitable"] else " NO"
    print(
        f"  {r['ticker']:<6} {name:<22}"
        f"  rev=${r['revenue'] / 1e6:>8,.0f}M"
        f"  growth={r['growth']:5.1%}"
        f"  profitable={prof}"
        f"  OCF_margin={r['ocf_margin']:.1%}"
    )
