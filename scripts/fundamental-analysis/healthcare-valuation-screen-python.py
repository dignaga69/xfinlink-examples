# Full write-up: https://xfinlink.com/blog/healthcare-valuation-screen-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# ── 10 healthcare stocks ─────────────────────────────────────────────
tickers = ["UNH", "LLY", "JNJ", "ABBV", "MRK", "PFE", "TMO", "ABT", "AMGN", "BMY"]

# ── Fetch 3Y of annual metrics ───────────────────────────────────────
metrics = xfl.metrics(
    tickers,
    period="3y",
    fields=["pe_ratio", "ps_ratio", "dividend_yield", "roe"],
    period_type="annual",
)

# ── Extract latest annual values per ticker ──────────────────────────
print("=== Healthcare Sector Valuation Screen ===")

results = []
for ticker in tickers:
    m = metrics[metrics["ticker"] == ticker].sort_values("period_end")
    if m.empty:
        continue

    latest = m.iloc[-1]
    results.append({
        "ticker": ticker,
        "entity_name": latest.get("entity_name", ticker),
        "pe_ratio": latest["pe_ratio"],
        "ps_ratio": latest["ps_ratio"],
        "dividend_yield": latest["dividend_yield"],
        "roe": latest["roe"],
    })

# Sort by PE ascending (cheapest first)
results.sort(key=lambda x: x["pe_ratio"] if x["pe_ratio"] else 999)

for r in results:
    name = r["entity_name"][:22]
    div_pct = r["dividend_yield"] * 100 if r["dividend_yield"] else 0
    roe_pct = r["roe"] * 100 if r["roe"] else 0
    print(
        f"  {r['ticker']:<6} {name:<22}"
        f"  PE={r['pe_ratio']:5.1f}"
        f"  P/S={r['ps_ratio']:5.1f}"
        f"  yield={div_pct:4.1f}%"
        f"  ROE={roe_pct:+6.1f}%"
    )

# Note on ABBV
print()
print("Note: ABBV has negative ROE (-129.2%) — likely negative equity from acquisitions")
