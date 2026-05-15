# How to Track Companies Through Ticker Changes, Bankruptcies, and Renames in Python

## What's the question?

A ticker symbol is not a permanent identifier. It is a label assigned by a stock exchange, and exchanges routinely reassign the same symbol to different companies over time. The ticker "FB" has been used by four separate companies since 1971. "GM" maps to two distinct legal entities separated by a bankruptcy. "DELL" was assigned to Dell Inc before its 2013 privatization and then to a different corporate entity, Dell Technologies, upon re-listing in 2018. If a data pipeline treats ticker symbols as stable identifiers, it will silently merge data from unrelated companies into a single time series. How do you detect and resolve these cases?

## The approach

Entity resolution is the process of mapping a ticker symbol to the specific company it represented during a given time period. Each company is assigned a permanent entity_id -- a stable identifier that persists through ticker changes, name changes, and exchange transfers. By resolving a ticker, you can see every company that has ever used that symbol, along with the exact date range each assignment was valid.

Five cases are examined: FB (four companies across five decades), GM (pre- and post-bankruptcy entities), META (the rename destination after Facebook changed its ticker), DELL (privatization and re-listing), and a batch resolution call that demonstrates handling of valid, historical, and nonexistent tickers.

## Code

```python
import xfinlink as xfl

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# === Example 1: FB — one ticker, four companies over 50 years ===
print("=== FB: Ticker Recycling Across 4 Companies ===")
fb = xfl.resolve("FB")
for entity in fb["data"]["FB"]["entities"]:
    valid_to = entity.get("ticker_valid_to") or "present"
    print(f"  {entity['name']}")
    print(f"    Ticker valid: {entity['ticker_valid_from']} → {valid_to}")
print()

# === Example 2: GM — bankruptcy splits one company into two entities ===
print("=== GM: Pre- and Post-Bankruptcy ===")
gm = xfl.resolve("GM")
for entity in gm["data"]["GM"]["entities"]:
    valid_to = entity.get("ticker_valid_to") or "present"
    idx = entity.get("index_membership", [])
    sp500 = [m for m in idx if m.get("index") == "SP500"]
    sp_str = ""
    if sp500:
        added = sp500[0].get("added", "?")
        removed = sp500[0].get("removed") or "current"
        sp_str = f" | S&P 500: {added} → {removed}"
    print(f"  {entity['name']}")
    print(f"    Entity ID: {entity['entity_id']} | Valid: {entity['ticker_valid_from']} → {valid_to}{sp_str}")
print()

# === Example 3: META — tracing the FB → META rename ===
print("=== META vs FB: The Rename ===")
meta = xfl.resolve("META")
for entity in meta["data"]["META"]["entities"]:
    valid_to = entity.get("ticker_valid_to") or "present"
    print(f"  {entity['name']}")
    print(f"    META valid: {entity['ticker_valid_from']} → {valid_to}")
print()

# === Example 4: DELL — private buyout and re-IPO ===
print("=== DELL: Went Private (2013) → Re-listed (2018) ===")
dell = xfl.resolve("DELL")
for entity in dell["data"]["DELL"]["entities"]:
    valid_to = entity.get("ticker_valid_to") or "present"
    print(f"  {entity['name']}")
    print(f"    Entity ID: {entity['entity_id']} | Valid: {entity['ticker_valid_from']} → {valid_to}")
print()

# === Example 5: Batch resolve — quick check for multiple tickers ===
print("=== Batch Resolve: Which tickers are valid? ===")
batch = xfl.resolve(["AAPL", "ENRON", "INVALID123"])
resolved = batch["meta"]["tickers_resolved"]
unresolved = batch["meta"]["tickers_unresolved"]
print(f"  Resolved:   {resolved}")
print(f"  Unresolved: {unresolved}")
```

## Output

```
=== FB: Ticker Recycling Across 4 Companies ===
  BANKBOSTON CORP
    Ticker valid: 1971-01-07 → 1983-04-03
  FALCON BUILDING PRODUCTS INC
    Ticker valid: 1994-11-03 → 1997-06-17
  F B R ASSET INVESTMENT CORP
    Ticker valid: 1999-09-29 → 2003-03-28
  Meta Platforms Inc
    Ticker valid: 2012-05-18 → 2022-06-08

=== GM: Pre- and Post-Bankruptcy ===
  General Motors Corporation (pre-2009 bankruptcy)
    Entity ID: 4 | Valid: 1962-07-02 → 2009-06-01
  General Motors Company
    Entity ID: 5 | Valid: 2010-11-18 → present | S&P 500: 2013-06-07 → current

=== META vs FB: The Rename ===
  Meta Platforms Inc
    META valid: 2022-06-09 → present

=== DELL: Went Private (2013) → Re-listed (2018) ===
  DELL INC
    Entity ID: 10408 | Valid: 1988-06-22 → 2013-10-29
  DELL TECHNOLOGIES INC
    Entity ID: 65047 | Valid: 2018-12-28 → present

=== Batch Resolve: Which tickers are valid? ===
  Resolved:   ['AAPL']
  Unresolved: ['ENRON', 'INVALID123']
```

## What this tells us

The FB case demonstrates the most common form of ticker recycling. Four entirely unrelated companies -- a bank (BankBoston), a manufacturer (Falcon Building Products), a financial services firm (FBR Asset Investment), and a social media platform (Meta Platforms) -- all traded under the same symbol at different times. A naive query for "FB" historical prices without date-range filtering would return a composite time series spanning four different businesses across four different industries.

The GM case illustrates how a bankruptcy creates two separate legal entities under the same brand. General Motors Corporation (entity_id 4) ceased trading on June 1, 2009, when it filed for Chapter 11 bankruptcy. General Motors Company (entity_id 5) began trading on November 18, 2010, as a distinct corporate successor. These are different companies with different shareholders, different balance sheets, and different entity identifiers.

The DELL case shows a gap in market data caused by a leveraged buyout (a transaction in which a company is taken private using borrowed funds). Dell Inc was delisted in October 2013 and Dell Technologies re-listed in December 2018. The five-year gap means any continuous price series for "DELL" contains a structural break.

## So what?

Any quantitative workflow that uses ticker symbols as merge keys -- backtesting, factor modeling, screening -- is vulnerable to data contamination from ticker recycling. The entity_id provides a stable identifier that follows the actual company through ticker changes, name changes, and corporate restructurings. When building historical analyses, resolve each ticker to its entity_id first, then scope data queries to the correct entity and date range. If a data source does not support entity resolution, its historical data should be treated as potentially contaminated for any ticker that has existed for more than a decade.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
