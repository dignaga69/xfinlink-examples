# Full write-up: https://xfinlink.com/blog/reit-dividend-valuation-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- 6 REITs across sub-sectors -------------------------------------------
tickers = ["O", "AMT", "VICI", "PSA", "WELL", "EQR"]

# -- Fetch 3Y of annual metrics ------------------------------------------
metrics = xfl.metrics(
    tickers,
    period="3y",
    fields=["pe_ratio", "pb_ratio", "dividend_yield", "debt_to_equity"],
    period_type="annual",
)

# -- Extract latest annual values per ticker ------------------------------
print("=== REIT Dividend & Valuation Screen ===")

results = []
for ticker in tickers:
    m = metrics[metrics["ticker"] == ticker].sort_values("period_end")
    if m.empty:
        continue

    latest = m.iloc[-1]
    div_yield = latest["dividend_yield"] * 100 if latest["dividend_yield"] else 0

    results.append({
        "ticker": ticker,
        "entity_name": latest.get("entity_name", ticker),
        "dividend_yield": div_yield,
        "pe_ratio": latest["pe_ratio"],
        "pb_ratio": latest["pb_ratio"],
        "debt_to_equity": latest["debt_to_equity"],
    })

# Sort by dividend yield descending
results.sort(key=lambda x: x["dividend_yield"], reverse=True)

for r in results:
    name = r["entity_name"][:24]
    print(
        f"  {r['ticker']:<6} {name:<24}"
        f"  yield={r['dividend_yield']:4.1f}%"
        f"  PE={r['pe_ratio']:6.1f}"
        f"  P/B={r['pb_ratio']:5.1f}"
        f"  D/E={r['debt_to_equity']:5.2f}"
    )
