# Full write-up: https://xfinlink.com/blog/momentum-screening-sp500-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

# Pick 20 large-cap S&P 500 stocks across sectors
tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META",
    "JPM", "V", "UNH", "LLY", "XOM",
    "PG", "COST", "HD", "AVGO", "CRM",
    "NFLX", "ABBV", "MRK", "PEP", "ORCL",
]

# Pull 6 months of daily prices
df = xfl.prices(tickers, period="6mo", fields=["close", "return_daily"])

# Calculate 3-month (63 trading days) and 1-month (21 days) momentum
mom = df.sort_values("date").groupby("ticker").agg(
    last_close=("close", "last"),
    total_return_6mo=("return_daily", lambda x: (1 + x).prod() - 1),
    total_return_3mo=("return_daily", lambda x: (1 + x.tail(63)).prod() - 1),
    total_return_1mo=("return_daily", lambda x: (1 + x.tail(21)).prod() - 1),
).round(4)

# Rank by 3-month momentum
mom = mom.sort_values("total_return_3mo", ascending=False)

print("=== Momentum Ranking (Top 10 by 3-Month Return) ===")
print(mom.head(10).to_string())
print()

print("=== Bottom 5 (Weakest Momentum) ===")
print(mom.tail(5).to_string())
