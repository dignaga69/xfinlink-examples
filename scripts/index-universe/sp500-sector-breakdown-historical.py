# Full write-up: https://xfinlink.com/blog/sp500-sector-breakdown-historical
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("xfl_91cda643688e76bd182665c64ca6aedc")

# Compare S&P 500 sector composition: 2010 vs 2020 vs today
snapshots = {
    "2010-01-01": xfl.index("sp500", as_of="2010-01-01"),
    "2020-01-01": xfl.index("sp500", as_of="2020-01-01"),
    "2026-05-01": xfl.index("sp500"),  # current
}

# For each snapshot, search for sector info on the constituents
# Use a sample of tickers to get sector distribution
for label, df in snapshots.items():
    print(f"=== S&P 500 as of {label}: {len(df)} constituents ===")
    # Show first 10 by ticker
    sample = df.head(10)[["ticker", "entity_name"]].copy()
    print(sample.to_string(index=False))
    print()

# Track specific companies that entered/left the index
print("=== Notable S&P 500 Changes ===")

# Who was in the 2010 index but not today?
tickers_2010 = set(snapshots["2010-01-01"]["ticker"].tolist())
tickers_now = set(snapshots["2026-05-01"]["ticker"].tolist())

departed = sorted(tickers_2010 - tickers_now)[:15]
joined = sorted(tickers_now - tickers_2010)[:15]

print(f"Left since 2010 (sample of {len(tickers_2010 - tickers_now)}): {', '.join(departed)}")
print(f"Joined since 2010 (sample of {len(tickers_now - tickers_2010)}): {', '.join(joined)}")
print()

# Turnover rate
total_departed = len(tickers_2010 - tickers_now)
total_joined = len(tickers_now - tickers_2010)
overlap = len(tickers_2010 & tickers_now)
print(f"=== 16-Year Turnover ===")
print(f"Still in index: {overlap}")
print(f"Departed:       {total_departed}")
print(f"New entrants:   {total_joined}")
print(f"Turnover rate:  {total_departed / len(tickers_2010):.1%}")
