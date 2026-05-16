# Full write-up: https://xfinlink.com/blog/gm-bankruptcy-entity-resolution-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Resolve GM: two entities, one ticker -----------------------------------
info = xfl.resolve("GM")
entities = info["data"]["GM"]["entities"]

print("=== GM: Two Companies, One Ticker, One Bankruptcy ===")
print()

for e in entities:
    valid_from = e.get("ticker_valid_from", "?")
    valid_to = e.get("ticker_valid_to") or "present"
    name = e["name"]
    eid = e["entity_id"]
    print(f"{name} (pre-2009 bankruptcy)" if "Corporation" in name else f"{name}")
    print(f"  Entity ID: {eid}")
    print(f"  Ticker valid: {valid_from} to {valid_to}")

    # Check for S&P 500 membership
    memberships = e.get("index_membership", [])
    for m in memberships:
        if m.get("index") == "sp500":
            added = m.get("added", "?")
            removed = m.get("removed") or "current"
            print(f"   S&P 500: {added} to {removed}")
    print()

# -- New GM: annual fundamentals since IPO ---------------------------------
print("=== New GM: Revenue and Profitability Since IPO ===")
df = xfl.fundamentals(
    "GM",
    period_type="annual",
    fields=["revenue", "net_income"],
    period="10y",
)

df = df.sort_values("period_end")
for _, r in df.iterrows():
    rev_str = f"${r['revenue'] / 1e3:>5.0f}B" if r["revenue"] else "   N/A"
    ni_str = f"${r['net_income'] / 1e3:>4.0f}B" if r["net_income"] else "  N/A"
    print(
        f"  {str(r['period_end'])[:10]}  {r['entity_name']:<30s}  "
        f"rev={rev_str}  NI={ni_str}"
    )

# -- Key insight ------------------------------------------------------------
print()
print("=== Key Insight ===")
print("Old GM (entity 4): General Motors Corporation -- filed for bankruptcy June 2009.")
print("New GM (entity 5): General Motors Company -- IPO November 2010.")
print("Stitching their financials together would merge a bankrupt entity with its successor.")
print("Entity resolution keeps them separate.")
