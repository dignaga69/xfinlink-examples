# Full write-up: https://xfinlink.com/blog/sp500-pe-ratio-screening-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("xfl_91cda643688e76bd182665c64ca6aedc")

# 30 blue-chip S&P 500 stocks across all 11 GICS sectors
tickers = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",  # Tech / Comm / Consumer
    "JPM", "BAC", "GS", "BRK.B", "V",          # Financials
    "UNH", "JNJ", "PFE", "LLY", "ABBV",        # Healthcare
    "XOM", "CVX", "COP",                        # Energy
    "PG", "KO", "PEP", "WMT", "COST",          # Consumer Staples / Disc
    "CAT", "HON", "UPS",                        # Industrials
    "NEE", "DUK",                               # Utilities
    "AMT", "PLD",                               # Real Estate
]

# Fetch valuation metrics — latest annual period for each
metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["pe_ratio", "pb_ratio", "earnings_yield", "dividend_yield"],
                      period="3y")

# Keep only the most recent period per ticker
metrics = metrics.sort_values("period_end").groupby("ticker").tail(1)

# Drop rows where PE is missing or negative (unprofitable)
valid = metrics.dropna(subset=["pe_ratio"])
valid = valid[valid["pe_ratio"] > 0].copy()

# Top 10 cheapest by P/E
cheapest = valid.nsmallest(10, "pe_ratio")[["ticker", "entity_name", "period_end", "pe_ratio", "pb_ratio", "earnings_yield"]]
print("=== 10 Cheapest Blue Chips by P/E Ratio ===")
print(cheapest.to_string(index=False))
print()

# Top 10 most expensive by P/E
expensive = valid.nlargest(10, "pe_ratio")[["ticker", "entity_name", "period_end", "pe_ratio", "pb_ratio", "earnings_yield"]]
print("=== 10 Most Expensive Blue Chips by P/E Ratio ===")
print(expensive.to_string(index=False))
print()

# Summary stats
print("=== P/E Summary (30 Blue Chips) ===")
print(f"Median P/E: {valid['pe_ratio'].median():.1f}")
print(f"Mean P/E:   {valid['pe_ratio'].mean():.1f}")
print(f"Min P/E:    {valid['pe_ratio'].min():.1f} ({valid.loc[valid['pe_ratio'].idxmin(), 'ticker']})")
print(f"Max P/E:    {valid['pe_ratio'].max():.1f} ({valid.loc[valid['pe_ratio'].idxmax(), 'ticker']})")
