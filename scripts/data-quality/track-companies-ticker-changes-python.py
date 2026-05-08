# Full write-up: https://xfinlink.com/blog/track-companies-ticker-changes-python
import xfinlink as xfl

xfl.set_api_key("YOUR_API_KEY")

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
