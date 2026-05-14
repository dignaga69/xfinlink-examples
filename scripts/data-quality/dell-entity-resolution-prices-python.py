# Full write-up: https://xfinlink.com/blog/dell-entity-resolution-prices-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Resolve DELL: two different companies -----------------------------------
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

# -- New Dell Technologies: first trading days (Dec 2018) --------------------
print("=== New Dell Technologies — First Trading Days (Dec 2018) ===")
first_days = xfl.prices("DELL", start="2018-12-28", end="2019-01-10", fields=["close", "volume"])
print(first_days[["date", "entity_name", "close", "volume"]].to_string(index=False))
print()

# -- Dell Technologies: recent (1 week) -------------------------------------
print("=== Dell Technologies — Recent (1 week) ===")
recent = xfl.prices("DELL", period="1w", fields=["close", "volume"])
print(recent[["date", "entity_name", "close", "volume"]].to_string(index=False))
print()

# -- Key insight -------------------------------------------------------------
first_close = first_days["close"].iloc[0]
last_close = recent["close"].iloc[-1]

print("=== Key Insight ===")
print(f"New Dell first close: ${first_close:.2f} (Dec 2018)")
print(f"Current close:        ${last_close:.2f}")
print()
print("These are DIFFERENT companies. Stitching them together would be wrong.")
print("Entity resolution prevents this — each entity has its own ID.")
