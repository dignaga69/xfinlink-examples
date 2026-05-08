# How to Screen Stocks by Momentum in Python

Momentum investing is one of the most well-documented anomalies in finance — stocks that have gone up recently tend to keep going up in the short term. Whether you're building a factor portfolio or just want to see which large caps are running hot, ranking stocks by their trailing return is the starting point. Here's how to screen 20 S&P 500 stocks by 3-month momentum.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== Momentum Ranking (Top 10 by 3-Month Return) ===
        last_close  total_return_6mo  total_return_3mo  total_return_1mo
ticker                                                                  
UNH         369.74            0.1498            0.3768            0.2084
AVGO        412.56            0.1602            0.3287            0.1766
ORCL        194.59           -0.2018            0.3267            0.3592
NVDA        211.50            0.1245            0.2305            0.1616
AMZN        271.17            0.1157            0.2177            0.2256
NFLX         88.25           -0.9196            0.0913           -0.1121
MSFT        420.77           -0.1536            0.0688            0.1241
AAPL        287.44            0.0655            0.0418            0.1102
COST       1012.06            0.0958            0.0230           -0.0177
XOM         146.58            0.2802            0.0034           -0.0617

=== Bottom 5 (Weakest Momentum) ===
        last_close  total_return_6mo  total_return_3mo  total_return_1mo
ticker                                                                  
PEP         156.29            0.1039           -0.0671            0.0096
ABBV        202.71           -0.0746           -0.0745           -0.0420
PG          146.06           -0.0005           -0.0791            0.0080
META        616.81           -0.0034           -0.0797            0.0072
HD          322.64           -0.1258           -0.1562           -0.0402
```

UNH leads with +37.7% over 3 months, followed by AVGO and ORCL both above +32%. The gap between the leaders and the laggards is stark — HD is down -15.6% over the same period. Notice how 6-month and 3-month momentum can diverge: ORCL is -20% over 6 months but +33% over 3 months, meaning most of its loss came early and it's been surging recently. This "acceleration" signal — when short-term momentum is much stronger than long-term — is often used by quant funds to spot regime changes.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
