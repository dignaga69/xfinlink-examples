# Why Ticker Symbols Are Unreliable: The Recycling Problem Every Quant Should Know

## What's the question?

Ticker symbols are the most visible identifiers in financial markets, but they are also among the least reliable. A ticker is not a permanent label for a company; it is a temporary assignment by a stock exchange that can be revoked, reassigned, or recycled at any time. The symbol "FB" has been assigned to four completely different companies since 1971. "GM" maps to two separate legal entities on either side of a bankruptcy filing. If a quantitative analysis uses ticker symbols as the primary key for joining or filtering data, it risks silently combining price, fundamental, and reference data from unrelated companies into a single record -- and no error will be raised because the join key matches. How widespread is this problem, and what does a correct solution look like?

## The approach

We examine four tickers with documented recycling histories: FB (four companies across five decades), DELL (two entities separated by a privatization), GM (two entities separated by a bankruptcy), and TWX (two entities with overlapping usage). For each ticker, the resolve endpoint returns every company that has ever used that symbol, along with the exact date range of each assignment and a permanent entity_id.

To demonstrate the practical consequence, we show what happens when a naive data pull for "FB" is issued without entity resolution, then contrast it with a scoped query that uses date-range filtering to retrieve only Meta Platforms' price data.

## Code

```python
import xfinlink as xfl

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Tickers that have been genuinely recycled between different companies
recycled = ["FB", "DELL", "GM", "TWX"]

print("=== Ticker Recycling: One Symbol, Multiple Companies ===")
print()

for ticker in recycled:
    info = xfl.resolve(ticker)
    entities = info["data"][ticker]["entities"]
    print(f'{ticker} — {len(entities)} entit{"y" if len(entities) == 1 else "ies"}')
    for e in entities:
        valid_from = e.get("ticker_valid_from", "?")
        valid_to = e.get("ticker_valid_to") or "present"
        print(f'  {e["name"]}')
        print(f'    {valid_from} → {valid_to} (entity_id={e["entity_id"]})')
    print()

# Show the practical danger
print('=== The Danger: Naive Data Pulls ===')
print('If you query 30 years of "FB" price data without entity resolution,')
print("you could get a time series mixing:")
print("  1971-1983: BankBoston Corp (banking)")
print("  1994-1997: Falcon Building Products (manufacturing)")
print("  1999-2003: FBR Asset Investment (finance)")
print("  2012-2022: Meta Platforms (social media)")
print()
print("These are 4 completely unrelated companies.")
print("Backtesting on this data would be meaningless.")
print()

# Show how xfinlink handles this: prices scoped to the correct entity
print('=== Safe Pull: FB prices scoped to Meta only (2021-2022) ===')
fb_prices = xfl.prices("FB", start="2021-01-04", end="2021-01-08", fields=["close"])
if len(fb_prices) > 0:
    print(fb_prices[["ticker", "entity_name", "date", "close"]].to_string(index=False))
else:
    print("(No data — FB ticker was Meta in this range, entity resolution applied)")
```

## Output

```
=== Ticker Recycling: One Symbol, Multiple Companies ===

FB — 4 entities
  BANKBOSTON CORP
    1971-01-07 → 1983-04-03 (entity_id=809)
  FALCON BUILDING PRODUCTS INC
    1994-11-03 → 1997-06-17 (entity_id=17829)
  F B R ASSET INVESTMENT CORP
    1999-09-29 → 2003-03-28 (entity_id=28677)
  Meta Platforms Inc
    2012-05-18 → 2022-06-08 (entity_id=2)

DELL — 2 entities
  DELL INC
    1988-06-22 → 2013-10-29 (entity_id=10408)
  DELL TECHNOLOGIES INC
    2018-12-28 → present (entity_id=65047)

GM — 2 entities
  General Motors Corporation (pre-2009 bankruptcy)
    1962-07-02 → 2009-06-01 (entity_id=4)
  General Motors Company
    2010-11-18 → present (entity_id=5)

TWX — 2 entities
  TIME WARNER INC
    1989-12-11 → present (entity_id=14682)
  A O L INC
    2003-10-16 → 2018-06-14 (entity_id=33763)

=== The Danger: Naive Data Pulls ===
If you query 30 years of "FB" price data without entity resolution,
you could get a time series mixing:
  1971-1983: BankBoston Corp (banking)
  1994-1997: Falcon Building Products (manufacturing)
  1999-2003: FBR Asset Investment (finance)
  2012-2022: Meta Platforms (social media)

These are 4 completely unrelated companies.
Backtesting on this data would be meaningless.

=== Safe Pull: FB prices scoped to Meta only (2021-2022) ===
ticker        entity_name       date     close
    FB Meta Platforms Inc 2021-01-04 268.94000
    FB Meta Platforms Inc 2021-01-05 270.97000
    FB Meta Platforms Inc 2021-01-06 263.31000
    FB Meta Platforms Inc 2021-01-07 268.73999
    FB Meta Platforms Inc 2021-01-08 267.57001
```

## What this tells us

The four tickers examined expose distinct categories of recycling risk. FB represents pure recycling: four companies in four different industries (banking, manufacturing, financial services, and social media) shared the same two-character symbol across non-overlapping time periods. A naive data query would stitch together price data from a 1970s bank and a 2010s social media company into a single time series, producing a return calculation that is arithmetically correct but economically meaningless.

GM illustrates the bankruptcy discontinuity problem. General Motors Corporation (entity_id 4) was liquidated in 2009. General Motors Company (entity_id 5) is a different legal entity with different shareholders, a different capital structure, and a different balance sheet. The ticker is the same, but the underlying company is not. Treating pre-2009 and post-2010 GM data as a continuous series introduces a structural break that distorts any long-horizon return or risk calculation.

DELL shows the privatization gap. Dell Inc was delisted in October 2013 and Dell Technologies re-listed in December 2018. The five-year gap during which no "DELL" traded means any data vendor that fills gaps by interpolation or carries forward stale data will produce fabricated returns for a period when the stock did not exist in public markets.

TWX presents an overlapping usage case, where Time Warner and AOL both used the ticker during partially overlapping periods following their merger and subsequent separation. This creates ambiguity that can only be resolved by examining the entity_id and validity dates.

## So what?

Ticker recycling is not an edge case affecting obscure securities. It occurs regularly in the large-cap universe, affecting household names like Facebook, General Motors, and Dell. Any data pipeline, backtest, or analytical workflow that uses ticker symbols as merge keys without entity resolution is vulnerable to data contamination. The entity_id provides the solution: a permanent identifier assigned to each distinct legal entity that persists through ticker changes, name changes, and exchange transfers. When building historical analyses, the correct pattern is to resolve each ticker to its entity_id first, then scope all subsequent data queries to the entity rather than the symbol. If a data source does not support entity resolution, every long-horizon query should be audited for recycling contamination.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
