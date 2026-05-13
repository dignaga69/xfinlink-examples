# Full write-up: https://xfinlink.com/blog/momentum-large-cap-screen-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# ── 15 large-cap tickers ──────────────────────────────────────────────
tickers = [
    "AAPL", "MSFT", "AMZN", "META", "NVDA",
    "JPM",  "V",    "UNH",  "LLY",  "XOM",
    "PG",   "COST", "HD",   "AVGO", "CRM",
]

# ── Fetch 6 months of daily data ──────────────────────────────────────
prices = xfl.prices(tickers, period="6mo", fields=["close", "return_daily"])

# ── Compute compound returns for each window ──────────────────────────
print("=== 3-Month Momentum Ranking (15 Large Caps) ===")

results = []
for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").reset_index(drop=True)
    if df.empty:
        continue

    last_close = df["close"].iloc[-1]

    # Compound return: product of (1 + daily_return) - 1
    ret_6mo = (1 + df["return_daily"]).prod() - 1
    ret_3mo = (1 + df["return_daily"].tail(63)).prod() - 1
    ret_1mo = (1 + df["return_daily"].tail(21)).prod() - 1

    results.append({
        "ticker": ticker,
        "close": last_close,
        "return_6mo": ret_6mo,
        "return_3mo": ret_3mo,
        "return_1mo": ret_1mo,
    })

# ── Sort by 3-month return descending ─────────────────────────────────
results.sort(key=lambda x: x["return_3mo"], reverse=True)

for r in results:
    print(
        f"  {r['ticker']:<6} ${r['close']:>9,.2f}"
        f"  6mo={r['return_6mo']:+.1%}"
        f"  3mo={r['return_3mo']:+.1%}"
        f"  1mo={r['return_1mo']:+.1%}"
    )
