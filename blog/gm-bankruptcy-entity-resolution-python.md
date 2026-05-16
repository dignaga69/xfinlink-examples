# GM Before and After Bankruptcy: Why Entity Resolution Matters for Financial Data

## What's the question?

General Motors Corporation filed for Chapter 11 bankruptcy on June 1, 2009 -- the largest industrial bankruptcy in U.S. history at the time. The company was liquidated, its viable assets were transferred to a new legal entity, and General Motors Company conducted an IPO on November 18, 2010. Both entities traded under the ticker "GM." Most financial databases treat them as one continuous company. They are not. The old GM was liquidated. The new GM inherited selected assets and liabilities but is a distinct legal entity with a different capital structure, different shareholders, and different accounting history. Mixing their financial data produces a phantom time series that represents no real company.

## The approach

Use xfl.resolve("GM") to identify the two entities and their validity dates. Examine the entity_id, ticker validity periods, and S&P 500 membership for each. Then pull 10 years of annual fundamentals for the new GM (the current holder of the ticker) to show the post-IPO revenue and profitability trajectory.

## Code

See [`gm-bankruptcy-entity-resolution-python.py`](gm-bankruptcy-entity-resolution-python.py)

## Output

```
=== GM: Two Companies, One Ticker, One Bankruptcy ===

General Motors Corporation (pre-2009 bankruptcy)
  Entity ID: 4
  Ticker valid: 1962-07-02 to 2009-06-01

General Motors Company
  Entity ID: 5
  Ticker valid: 2010-11-18 to present
   S&P 500: 2013-06-07 to current

=== New GM: Revenue and Profitability Since IPO ===
  2016-12-31  General Motors Company          rev= $149B  NI=  $9B
  2017-12-31  General Motors Company          rev= $146B  NI= $-4B
  2018-12-31  General Motors Company          rev= $133B  NI=  $8B
  2019-12-31  General Motors Company          rev= $123B  NI=  $7B
  2020-12-31  General Motors Company          rev= $109B  NI=  $6B
  2021-12-31  General Motors Company          rev= $114B  NI= $10B
  2022-12-31  General Motors Company          rev= $144B  NI= $10B
  2023-12-31  General Motors Company          rev= $158B  NI= $10B
  2024-12-31  General Motors Company          rev= $172B  NI=  $6B
  2025-12-31  General Motors Company          rev= $168B  NI=  $3B

=== Key Insight ===
Old GM (entity 4): General Motors Corporation -- filed for bankruptcy June 2009.
New GM (entity 5): General Motors Company -- IPO November 2010.
Stitching their financials together would merge a bankrupt entity with its successor.
Entity resolution keeps them separate.
```

## What this tells us

The entity data correctly separates old GM (entity 4, valid 1962-2009) from new GM (entity 5, valid 2010-present). The 17-month gap between the last trading day of old GM and the IPO of new GM is the bankruptcy restructuring period. New GM's fundamental trajectory shows a company that peaked at $172B revenue in 2024 and $10B net income in 2021-2023, with a notable decline to $168B revenue and $3B net income in 2025 -- potentially reflecting EV transition costs and competitive pressure.

## So what?

For any analysis that spans the 2009 bankruptcy -- long-term returns, growth rates, valuation multiples, financial ratios -- using a single continuous "GM" series produces incorrect results. The entity_id system ensures that queries for GM after 2010 return only new GM data, and queries before 2009 return only old GM data. Any data vendor that does not maintain entity-level identifiers will silently mix these two companies.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
