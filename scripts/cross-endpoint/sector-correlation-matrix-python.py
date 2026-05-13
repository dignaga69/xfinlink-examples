# Full write-up: https://xfinlink.com/blog/sector-correlation-matrix-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# ── 8 sector ETFs ────────────────────────────────────────────────────
tickers = ["XLK", "XLF", "XLV", "XLE", "XLY", "XLP", "XLI", "XLU"]

sector_labels = {
    "XLK": "Tech",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLY": "ConsDisc",
    "XLP": "ConsStaples",
    "XLI": "Industrials",
    "XLU": "Utilities",
}

# ── Fetch 1Y of daily returns ────────────────────────────────────────
prices = xfl.prices(tickers, period="1y", fields=["return_daily"])

# ── Pivot to wide format: date x sector ──────────────────────────────
pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot.rename(columns=sector_labels)

# Reorder columns for readability
col_order = ["Energy", "Financials", "Industrials", "Tech",
             "ConsStaples", "Utilities", "Healthcare", "ConsDisc"]
pivot = pivot[col_order]

# ── Compute correlation matrix ───────────────────────────────────────
corr = pivot.corr()

print("=== Sector Correlation Matrix (1Y Daily Returns) ===")
header = "             " + "  ".join(f"{c:>11}" for c in col_order)
print(header)

for row_label in col_order:
    values = "  ".join(f"{corr.loc[row_label, c]:11.3f}" for c in col_order)
    print(f"{row_label:<13}{values}")

# ── Find most / least correlated pairs ────────────────────────────────
import itertools

pairs = []
for a, b in itertools.combinations(col_order, 2):
    pairs.append((a, b, corr.loc[a, b]))

pairs.sort(key=lambda x: x[2])

print("\nMost correlated pairs:")
for a, b, c in pairs[-3:]:
    print(f"  {a} \u2194 {b}: {c:.3f}")

print("\nLeast correlated pairs (best diversifiers):")
for a, b, c in pairs[:3]:
    print(f"  {a} \u2194 {b}: {c:.3f}")
