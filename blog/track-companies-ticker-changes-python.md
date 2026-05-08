# How to Track Companies Through Ticker Changes, Bankruptcies, and Renames in Python

If you've ever pulled historical stock data and gotten weird results for tickers like FB, GM, or DELL, you've hit the ticker recycling problem. The same ticker symbol gets reused by completely different companies over time — "FB" was used by four separate companies before Meta. Most data APIs ignore this entirely, silently mixing data from different companies. Here's how to handle it correctly.

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

**Output:**

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

The key insight is that a ticker is not an identity — it's a label that gets reassigned. "FB" wasn't just Facebook; it was BankBoston Corp in the 1970s, Falcon Building Products in the 1990s, and FBR Asset Investment in the early 2000s. If you naively pull "FB" historical data without entity resolution, you could be mixing price data from a bank, a manufacturing company, and a social media platform into a single time series. The resolve endpoint gives you the entity_id — a stable identifier that follows the actual company through ticker changes, name changes, and exchange transfers.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
