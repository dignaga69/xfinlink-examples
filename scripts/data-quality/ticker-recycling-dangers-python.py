# Full write-up: https://xfinlink.com/blog/ticker-recycling-dangers-python
import xfinlink as xfl

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
