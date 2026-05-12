# Full write-up: https://xfinlink.com/blog/sp500-rebalancing-additions-removals-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
