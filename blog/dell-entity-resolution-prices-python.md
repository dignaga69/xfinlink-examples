# DELL: Why Stitching Historical Price Data Together Is Wrong

## What's the question?

Dell Inc. went private in October 2013 through a leveraged buyout. Five years later, Dell Technologies re-entered public markets in December 2018 as a structurally different company -- one that had absorbed EMC Corporation and held a controlling stake in VMware, producing a revenue mix, capital structure, and operating profile with no continuity to the original Dell Inc. Both entities traded under the ticker "DELL." A data provider that concatenates these two price histories into a single time series creates a fictitious continuity: return calculations, drawdown analysis, backtests, and factor regressions built on that series would all be contaminated by a price jump that represents a corporate restructuring, not a market movement. How does entity resolution prevent this contamination?

## The approach

The xfinlink entity resolution system assigns each distinct corporate entity a permanent, unique identifier (entity_id) that persists regardless of ticker changes, delistings, or re-IPOs. The resolve endpoint is queried for "DELL" to reveal the full entity lineage: two separate entries with non-overlapping validity windows. The prices endpoint is then called for two time periods -- Dell Technologies' first trading days in December 2018 and its most recent week -- to confirm that both queries return data exclusively for entity_id 65047 (Dell Technologies Inc.) with no leakage from entity_id 10408 (Dell Inc.).

## Code

```python
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

info = xfl.resolve("DELL")
entities = info["data"]["DELL"]["entities"]

print("=== DELL: Two Companies, One Ticker ===")
print()

for e in entities:
    valid_from = e.get("ticker_valid_from", "?")
    valid_to = e.get("ticker_valid_to") or "present"
    print(f"  {e['name']}")
    print(f"    Entity ID: {e['entity_id']} | Valid: {valid_from} → {valid_to}")
    print()

print("=== New Dell Technologies — First Trading Days (Dec 2018) ===")
first_days = xfl.prices("DELL", start="2018-12-28", end="2019-01-10", fields=["close", "volume"])
print(first_days[["date", "entity_name", "close", "volume"]].to_string(index=False))
print()

print("=== Dell Technologies — Recent (1 week) ===")
recent = xfl.prices("DELL", period="1w", fields=["close", "volume"])
print(recent[["date", "entity_name", "close", "volume"]].to_string(index=False))
print()

first_close = first_days["close"].iloc[0]
last_close = recent["close"].iloc[-1]

print("=== Key Insight ===")
print(f"New Dell first close: ${first_close:.2f} (Dec 2018)")
print(f"Current close:        ${last_close:.2f}")
print()
print("These are DIFFERENT companies. Stitching them together would be wrong.")
print("Entity resolution prevents this — each entity has its own ID.")
```

## Output

```
=== DELL: Two Companies, One Ticker ===

  DELL INC
    Entity ID: 10408 | Valid: 1988-06-22 → 2013-10-29

  DELL TECHNOLOGIES INC
    Entity ID: 65047 | Valid: 2018-12-28 → present

=== New Dell Technologies — First Trading Days (Dec 2018) ===
      date           entity_name  close  volume
2018-12-31 DELL TECHNOLOGIES INC  48.87 5818707
2019-01-02 DELL TECHNOLOGIES INC  47.12 6108745
2019-01-03 DELL TECHNOLOGIES INC  45.13 6902591
2019-01-04 DELL TECHNOLOGIES INC  46.02 8906759
2019-01-07 DELL TECHNOLOGIES INC  46.32 4925854
2019-01-08 DELL TECHNOLOGIES INC  46.87 7286293

=== Dell Technologies — Recent (1 week) ===
      date           entity_name  close   volume
2026-05-07 DELL TECHNOLOGIES INC 230.27  4842310
2026-05-08 DELL TECHNOLOGIES INC 260.46 12046171
2026-05-11 DELL TECHNOLOGIES INC 247.04 11195114
2026-05-12 DELL TECHNOLOGIES INC 238.94  7124144
2026-05-13 DELL TECHNOLOGIES INC 243.87  4985109

=== Key Insight ===
New Dell first close: $48.87 (Dec 2018)
Current close:        $243.87

These are DIFFERENT companies. Stitching them together would be wrong.
Entity resolution prevents this — each entity has its own ID.
```

## What this tells us

The resolve endpoint identifies two distinct entities behind the "DELL" ticker, separated by a five-year gap during which no public company traded under that symbol. Dell Inc. (entity_id 10408, valid 1988-2013) was a personal computer manufacturer. Dell Technologies (entity_id 65047, valid 2018-present) is an enterprise IT conglomerate encompassing the original PC business, EMC's storage division, and -- until its 2021 spinoff -- a controlling stake in VMware. Despite sharing a ticker and a founder, the two entities have incomparable financial statements, capital structures, and revenue compositions.

The price queries confirm clean separation across both time periods. Every row returned for December 2018 and May 2026 identifies "DELL TECHNOLOGIES INC" with entity_id 65047. No data from Dell Inc. contaminates the series. Querying "DELL" with `as_of="2012-01-01"` would return Dell Inc. data exclusively, because the temporal filter restricts resolution to the entity that was valid at that date.

Without entity resolution, a request for the full "DELL" price history would produce a time series jumping from Dell Inc.'s final pre-privatization close (approximately $13.65 in October 2013) to Dell Technologies' first post-IPO close ($48.87 in December 2018) -- a 258% phantom gain spanning a five-year period when no stock traded. Any return calculation, volatility estimate, or backtest covering this window would be mathematically invalid.

## So what?

Ticker recycling -- the reuse of the same symbol by different corporate entities -- is among the most common and least visible sources of data error in quantitative finance. It affects privatizations and re-IPOs (DELL), bankruptcies (GM before and after 2009), rebrands (FB to META), and exchange delistings. Any analysis spanning multiple years should treat entity-level identifiers, not tickers, as the primary key for joining data across time. The entity_id field guarantees that price series, fundamental data, and derived analytics remain bound to a single corporate entity regardless of how many times a ticker has been reassigned.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
