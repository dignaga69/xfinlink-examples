# Why Ticker Symbols Are Unreliable: The Recycling Problem Every Quant Should Know

Most financial data APIs treat ticker symbols as stable identifiers. They're not. "FB" has been assigned to four completely different companies since 1971. "GM" maps to two separate legal entities across a bankruptcy. If you build a backtest on raw ticker data, you could be mixing banks with social media companies in the same time series — and your code wouldn't raise a single error. Here's how to detect and handle this.

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

**Output:**

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

The `entity_id` is what makes this safe — xfinlink returns 809 for BankBoston, 17829 for Falcon Building Products, 28677 for FBR Asset Investment, and 2 for Meta Platforms. When you pull prices for "FB" in the 2021 date range, entity resolution ensures you only get Meta's data, not a stitched-together Frankenstein time series. The same pattern applies to DELL (Dell Inc went private in 2013, Dell Technologies re-listed in 2018 as a separate entity) and GM (old GM was liquidated in bankruptcy, new GM is a different company). If your data vendor doesn't have entity resolution, your backtests have a hidden data integrity problem.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
