# How to Screen Stocks by Balance Sheet Health in Python

A stock can have great earnings and still go bankrupt if it can't pay its bills. The balance sheet tells you whether a company can survive a downturn — current ratio measures short-term liquidity, debt-to-equity measures leverage, and interest coverage tells you how easily it can service its debt. Here's how to screen 10 major stocks for financial health.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "JNJ", "XOM", "T"]

metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["current_ratio", "quick_ratio", "debt_to_equity", "debt_to_assets", "interest_coverage", "cash_per_share"],
                      period="3y")

latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.sort_values("current_ratio", ascending=False)

print("=== Balance Sheet Health: Liquidity Ratios ===")
print(latest[["ticker", "entity_name", "current_ratio", "quick_ratio", "cash_per_share"]].to_string(index=False))
print()

print("=== Leverage Ratios ===")
lev = latest.sort_values("debt_to_equity", ascending=True)
print(lev[["ticker", "entity_name", "debt_to_equity", "debt_to_assets", "interest_coverage"]].to_string(index=False))
print()

risky = latest[(latest["current_ratio"] < 1) | (latest["debt_to_equity"] > 2)]
print("=== Watch List: Weak Balance Sheets ===")
if len(risky) > 0:
    for _, r in risky.iterrows():
        flags = []
        if r["current_ratio"] < 1:
            flags.append(f"current_ratio={r['current_ratio']:.2f}")
        if r["debt_to_equity"] is not None and r["debt_to_equity"] > 2:
            flags.append(f"debt/equity={r['debt_to_equity']:.2f}")
        print(f"  {r['ticker']}: {', '.join(flags)}")
else:
    print("  All clear")
```

**Output:**

```
=== Balance Sheet Health: Liquidity Ratios ===
ticker         entity_name  current_ratio  quick_ratio  cash_per_share
  META  Meta Platforms Inc       2.598767          NaN             NaN
  TSLA           TESLA INC       2.164407     1.773665          4.4023
  GOOG        ALPHABET INC       2.005334          NaN          2.5404
  MSFT      MICROSOFT CORP       1.353446     1.346804          4.0711
   XOM    EXXON MOBIL CORP       1.152800     0.835103          2.5769
  AMZN      AMAZON COM INC       1.050815     0.875017          8.0700
   JNJ   JOHNSON & JOHNSON       1.027676     0.765492          8.1784
     T         A T & T INC       0.906136          NaN          2.6046
  AAPL           Apple Inc       0.893293     0.858770          2.4466
   JPM JPMORGAN CHASE & CO            NaN          NaN          8.0639

=== Leverage Ratios ===
ticker         entity_name  debt_to_equity  debt_to_assets  interest_coverage
  TSLA           TESLA INC        0.099261        0.059163          12.884615
  GOOG        ALPHABET INC        0.112090        0.078193         175.324728
  MSFT      MICROSOFT CORP        0.116898        0.064866          53.890147
   XOM    EXXON MOBIL CORP        0.143801        0.083077          69.437811
  AMZN      AMAZON COM INC        0.160809        0.080806          35.169305
   JPM JPMORGAN CHASE & CO        0.178723        0.014639          32.590513
  META  Meta Platforms Inc        0.271585        0.161193          76.400000
   JNJ   JOHNSON & JOHNSON        0.587818        0.240615          34.554068
     T         A T & T INC        1.065040        0.320606           3.551146
  AAPL           Apple Inc        1.170534        0.240248                NaN

=== Watch List: Weak Balance Sheets ===
  T: current_ratio=0.91
  AAPL: current_ratio=0.89
```

The surprise is Apple: it has the second-worst balance sheet in this group with a current ratio below 1 (0.89) and the highest debt-to-equity (1.17). This is by design — Apple deliberately runs a leveraged balance sheet because its cash flow is so predictable that it doesn't need liquidity buffers. AT&T is the other flag with a current ratio of 0.91 and interest coverage of only 3.5x — much less margin for error. On the other end, TSLA has the cleanest balance sheet: lowest debt-to-equity at 0.10 and a 2.16 current ratio, reflecting its decision to fund growth from operations rather than debt.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
