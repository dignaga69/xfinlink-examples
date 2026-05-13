# Full write-up: https://xfinlink.com/blog/multi-endpoint-dashboard-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# ── Target tickers ────────────────────────────────────────────────────
tickers = ["AAPL", "MSFT", "AMZN", "JPM", "JNJ", "XOM", "PG", "UNH", "HD", "CRM"]

# ── Step 1: Get S&P 500 members as of 2020 ───────────────────────────
index_data = xfl.index("SP500", as_of="2020-01-01")
members = index_data["ticker"].unique().tolist()
print(f"Step 1: {len(members)} unique S&P 500 members as of 2020-01-01")

# ── Step 2: Confirm our tickers were in the 2020 index ────────────────
confirmed = [t for t in tickers if t in members]
print(f"Step 2: {len(confirmed)}/{len(tickers)} confirmed in 2020 index")

# ── Step 3: Fetch 1Y price data ──────────────────────────────────────
prices = xfl.prices(confirmed, period="1y", fields=["close", "return_daily"])
print(f"Step 3: {len(prices)} price rows")

# ── Step 4: Fetch 3Y fundamentals ────────────────────────────────────
fundamentals = xfl.fundamentals(
    confirmed,
    period="3y",
    fields=["revenue", "net_income"],
)

# ── Step 5: Fetch 3Y metrics ─────────────────────────────────────────
metrics = xfl.metrics(
    confirmed,
    period="3y",
    fields=["pe_ratio", "roe"],
    period_type="annual",
)
print("Step 4-5: Combined")

# ── Build dashboard ──────────────────────────────────────────────────
print()
print("=== Multi-Endpoint Dashboard: 1Y Return + Fundamentals + Metrics ===")
print("(Survivorship-bias-free: tickers confirmed in 2020 S&P 500)")
print()

results = []
for ticker in confirmed:
    # 1Y compound return
    p = prices[prices["ticker"] == ticker].sort_values("date")
    ret_1y = (1 + p["return_daily"]).prod() - 1 if not p.empty else None

    # Latest annual revenue
    f = fundamentals[fundamentals["ticker"] == ticker].sort_values("period_end")
    rev = f["revenue"].iloc[-1] if not f.empty else None

    # Latest PE and ROE
    m = metrics[metrics["ticker"] == ticker].sort_values("period_end")
    pe = m["pe_ratio"].iloc[-1] if not m.empty else None
    roe = m["roe"].iloc[-1] if not m.empty else None

    results.append({
        "ticker": ticker,
        "return_1y": ret_1y,
        "revenue": rev,
        "pe_ratio": pe,
        "roe": roe,
    })

# Sort by 1Y return descending
results.sort(key=lambda x: x["return_1y"] or 0, reverse=True)

for r in results:
    rev_str = f"${r['revenue'] / 1e9:,.0f}B" if r["revenue"] else "N/A"
    print(
        f"  {r['ticker']:<6} 1y={r['return_1y']:+.1%}"
        f"  rev={rev_str:>6}"
        f"  PE={r['pe_ratio']:5.1f}"
        f"  ROE={r['roe']:+.1%}"
    )
