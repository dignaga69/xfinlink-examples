# How to Screen SaaS Stocks by Revenue Growth and Cash Flow in Python

## What's the question?

Revenue growth is the defining metric for software-as-a-service (SaaS) companies, where recurring subscription revenue compounds over time. But growth alone is insufficient for evaluation. A company growing revenue at 30% while burning cash is in a fundamentally different position than one growing at the same rate while generating positive operating cash flow. The question is: among high-growth cloud and SaaS companies, which are scaling efficiently -- converting revenue growth into cash generation -- and which are still spending more than they earn?

## The approach

Six publicly traded SaaS and cloud infrastructure companies are screened: Cloudflare (NET), Snowflake (SNOW), Datadog (DDOG), Zscaler (ZS), MongoDB (MDB), and CrowdStrike (CRWD). For each, three years of annual fundamentals are fetched to compute year-over-year revenue growth between the two most recent fiscal years. GAAP net income determines profitability status, and operating cash flow margin (OCF margin) -- defined as operating cash flow divided by revenue -- measures how efficiently the company converts top-line revenue into cash. OCF margin is preferred over free cash flow margin here because it isolates operational efficiency before capital expenditure decisions.

## Code

```python
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["DDOG", "ZS", "CRWD", "NET", "MDB", "SNOW"]

fundamentals = xfl.fundamentals(
    tickers,
    period="3y",
    fields=["revenue", "net_income", "operating_cash_flow"],
    period_type="annual",
)

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
```

## Output

```
=== SaaS / Cloud Growth Screen (YoY Revenue Growth) ===
  NET    CLOUDFLARE INC          rev=    $2168M  growth= 29.8%  profitable= NO  OCF_margin=27.8%
  SNOW   SNOWFLAKE INC           rev=    $4684M  growth= 29.2%  profitable= NO  OCF_margin=26.1%
  DDOG   DATADOG INC             rev=    $3427M  growth= 27.7%  profitable=YES  OCF_margin=30.6%
  ZS     ZSCALER INC             rev=    $2673M  growth= 23.3%  profitable= NO  OCF_margin=36.4%
  MDB    MONGODB INC             rev=    $2464M  growth= 22.8%  profitable= NO  OCF_margin=20.5%
  CRWD   CROWDSTRIKE HOLDINGS I  rev=    $4812M  growth= 21.7%  profitable= NO  OCF_margin=33.5%
```

## What this tells us

All six companies are growing revenue above 20% annually, confirming that the SaaS growth premium remains intact in this cohort. However, the gap between GAAP profitability and cash generation reveals an important nuance.

Datadog is the only company in the group that is GAAP profitable, and it also posts the highest OCF margin among the growth leaders (30.6% at 27.7% growth). This combination of profitability and growth places it in the "Rule of 40" territory -- a heuristic where the sum of revenue growth rate and profit margin should exceed 40% for a healthy SaaS business.

Zscaler presents the most interesting divergence: it is not GAAP profitable, yet its OCF margin of 36.4% is the highest in the group. The gap between GAAP profitability and operating cash flow is almost entirely explained by stock-based compensation (SBC), which is a non-cash expense under GAAP but does not reduce operating cash flow. Whether SBC represents a "real" cost depends on whether you view dilution as economically equivalent to a cash expense.

All six companies generate positive operating cash flow despite five being GAAP unprofitable. For subscription businesses, OCF is generally a more reliable health indicator than GAAP net income because subscription revenue is collected in advance (deferred revenue), creating a natural cash flow tailwind.

## So what?

When screening SaaS stocks, filtering by GAAP profitability alone would eliminate five of these six companies, all of which are generating substantial operating cash flow. A more informative screen combines revenue growth rate with OCF margin. Companies like Datadog and Zscaler that deliver both high growth and high cash conversion are typically valued at premium multiples for good reason -- they have demonstrated the ability to scale without proportional cash burn. The "profitable=NO" label is a GAAP artifact that obscures the underlying economics of the subscription model.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
