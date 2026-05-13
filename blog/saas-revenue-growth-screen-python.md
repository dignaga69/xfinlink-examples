# How to Screen SaaS Stocks by Revenue Growth and Cash Flow in Python

Revenue growth is the lifeblood of SaaS companies. But growing fast while burning cash is different from growing fast while generating it. Screening by both growth rate and operating cash flow margin separates the scalers from the spenders.

## Code

See [`saas-revenue-growth-screen-python.py`](saas-revenue-growth-screen-python.py)

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

## Discussion

All 6 are growing 20%+ -- the SaaS growth premium is alive. DDOG is the standout: the only profitable company in the group, with the highest OCF margin (30.6%) and near-top growth (27.7%). ZS is the cash flow champion at 36.4% OCF margin despite not being GAAP profitable -- stock-based compensation is the gap. The "profitable=NO" label is GAAP net income; all 6 generate positive operating cash flow, which is the real health metric for subscription businesses.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
