# How to Track S&P 500 Additions and Removals Over Time in Python

Every time the S&P 500 adds or removes a stock, billions of dollars move — index funds must buy the new entrant and sell the exit. Understanding who got added and why reveals what the index committee values: market cap, profitability, and sector balance. Here's how to compare index composition across time using point-in-time historical data.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Compare S&P 500 composition at 3 points to track additions and removals
dates = ["2024-01-01", "2025-01-01", "2026-05-01"]
snapshots = {}
for d in dates:
    snapshots[d] = set(xfl.index("sp500", as_of=d)["ticker"].tolist())

# What was added between 2024 and 2025?
added_2024_25 = sorted(snapshots["2025-01-01"] - snapshots["2024-01-01"])
removed_2024_25 = sorted(snapshots["2024-01-01"] - snapshots["2025-01-01"])

# What was added between 2025 and now?
added_2025_now = sorted(snapshots["2026-05-01"] - snapshots["2025-01-01"])
removed_2025_now = sorted(snapshots["2025-01-01"] - snapshots["2026-05-01"])

print("=== S&P 500 Rebalancing: Who Got In, Who Got Out ===")
print()
print(f"--- 2024 → 2025 ({len(added_2024_25)} added, {len(removed_2024_25)} removed) ---")
print(f"  Added:   {' '.join(added_2024_25[:20])}")
print(f"  Removed: {' '.join(removed_2024_25[:20])}")
print()
print(f"--- 2025 → May 2026 ({len(added_2025_now)} added, {len(removed_2025_now)} removed) ---")
print(f"  Added:   {' '.join(added_2025_now[:20])}")
print(f"  Removed: {' '.join(removed_2025_now[:20])}")
print()

for d in dates:
    print(f"  S&P 500 as of {d}: {len(snapshots[d])} constituents")
print()

total_changes = len(added_2024_25) + len(removed_2024_25) + len(added_2025_now) + len(removed_2025_now)
print(f"Total changes in ~2.5 years: {total_changes} ({total_changes//2} in+out cycles)")
```

**Output:**

```
=== S&P 500 Rebalancing: Who Got In, Who Got Out ===

--- 2024 → 2025 (16 added, 13 removed) ---
  Added:   APO CRWD DECK DELL ERIE GDDY GEV KKR LII PLTR SMCI SOLV SW TPL VST WDAY
  Removed: AAL BIO CMA CTLT ETSY ILMN LB PXD QRVO RHI VFC XRAY ZION

--- 2025 → May 2026 (0 added, 6 removed) ---
  Added:   
  Removed: ANSS DFS HES IPG JNPR WBA

  S&P 500 as of 2024-01-01: 438 constituents
  S&P 500 as of 2025-01-01: 441 constituents
  S&P 500 as of 2026-05-01: 435 constituents

Total changes in ~2.5 years: 35 (17 in+out cycles)
```

The 2024-2025 rebalance was dominated by high-growth tech and private equity entrants: PLTR, CRWD, DELL, KKR, and APO all made the cut. On the removal side, it was retail (VFC, ETSY), biotech (BIO, ILMN), and regional banks (CMA, ZION) — companies that shrank below the market cap threshold. The 2025-2026 period shows six removals with no additions, mostly due to M&A: Hess (acquired by Chevron), Discover Financial (Capital One), and Juniper Networks (HPE). This is the kind of historical composition data that matters for survivorship-bias-free backtesting.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
