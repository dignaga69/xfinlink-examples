# Full write-up: https://xfinlink.com/blog/mag7-correlation-python

import itertools
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Magnificent 7 (minus GOOGL — uses 6 for clean matrix) ---------------
tickers = ["AAPL", "AMZN", "META", "MSFT", "NVDA", "TSLA"]

# -- Fetch 1Y of daily returns -------------------------------------------
prices = xfl.prices(tickers, period="1y", fields=["return_daily"])

# -- Pivot to wide format: date x ticker ---------------------------------
pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot[tickers]  # enforce column order

# -- Compute correlation matrix -------------------------------------------
corr = pivot.corr()

print("=== Magnificent 7 Intra-Group Correlation (1Y) ===")
print("(Which of these mega-caps move independently?)")
print()

header = f"{'ticker':<8}" + "  ".join(f"{t:>6}" for t in tickers)
print(header)

for row in tickers:
    values = "  ".join(f"{corr.loc[row, c]:6.3f}" for c in tickers)
    print(f"{row:<8}{values}")

# -- Find most / least correlated pairs ----------------------------------
pairs = []
for a, b in itertools.combinations(tickers, 2):
    pairs.append((a, b, corr.loc[a, b]))

pairs.sort(key=lambda x: x[2])

print("\nLowest correlation (most independent):")
for a, b, c in pairs[:3]:
    print(f"  {a} / {b}: {c:.3f}")

print("\nHighest correlation (most redundant):")
for a, b, c in pairs[-3:]:
    print(f"  {a} / {b}: {c:.3f}")
