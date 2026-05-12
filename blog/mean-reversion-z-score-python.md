# How to Find Oversold and Overbought Stocks Using Z-Scores in Python

Mean reversion is the idea that prices tend to return to their average over time. When a stock's Z-score from its 50-day moving average drops below -1.5, it's statistically extended to the downside — a potential bounce candidate. Above +1.5, it's overextended and due for a pullback. Here's how to screen 10 large caps for mean reversion signals.

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "JPM", "XOM", "JNJ", "PG"]
df = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

results = []
for ticker in tickers:
    t = df[df["ticker"] == ticker].sort_values("date").copy()
    t["sma_50"] = t["close"].rolling(50).mean()
    t["z_score"] = (t["close"] - t["sma_50"]) / t["close"].rolling(50).std()
    last = t.dropna().iloc[-1]
    results.append({
        "ticker": ticker,
        "close": last["close"],
        "sma_50": last["sma_50"],
        "pct_from_sma50": (last["close"] / last["sma_50"] - 1),
        "z_score": last["z_score"],
    })

rdf = pd.DataFrame(results).sort_values("z_score")
print("=== Mean Reversion Signals: Z-Score from 50-Day SMA ===")
print("(Negative = below average = potential bounce, Positive = extended = potential pullback)")
print()
for _, r in rdf.iterrows():
    signal = "OVERSOLD" if r["z_score"] < -1.5 else ("OVERBOUGHT" if r["z_score"] > 1.5 else "")
    print(f"  {r['ticker']:5s}  close=${r['close']:>8.2f}  sma50=${r['sma_50']:>8.2f}  gap={r['pct_from_sma50']:>+6.1%}  z={r['z_score']:>+5.2f}  {signal}")
```

**Output:**

```
=== Mean Reversion Signals: Z-Score from 50-Day SMA ===
(Negative = below average = potential bounce, Positive = extended = potential pullback)

  JNJ    close=$  221.43  sma50=$  235.87  gap= -6.1%  z=-1.93  OVERSOLD
  PG     close=$  143.36  sma50=$  147.26  gap= -2.6%  z=-0.78  
  XOM    close=$  149.68  sma50=$  154.84  gap= -3.3%  z=-0.78  
  META   close=$  598.86  sma50=$  625.56  gap= -4.3%  z=-0.67  
  JPM    close=$  300.00  sma50=$  300.03  gap= -0.0%  z=-0.00  
  MSFT   close=$  412.66  sma50=$  398.55  gap= +3.5%  z=+0.67  
  AMZN   close=$  268.99  sma50=$  232.42  gap=+15.7%  z=+1.44  
  NVDA   close=$  219.44  sma50=$  189.50  gap=+15.8%  z=+2.14  OVERBOUGHT
  AAPL   close=$  292.68  sma50=$  263.37  gap=+11.1%  z=+2.46  OVERBOUGHT
  GOOGL  close=$  384.80  sma50=$  313.86  gap=+22.6%  z=+3.28  OVERBOUGHT
```

JNJ is the only stock flashing OVERSOLD at z=-1.93, trading 6% below its 50-day SMA. On the opposite end, GOOGL is the most extended at z=+3.28 — 23% above its 50-day average, which is extreme by any standard. Three stocks trigger the OVERBOUGHT signal (NVDA, AAPL, GOOGL), suggesting the recent tech rally may be due for a pause. Mean reversion doesn't predict timing, but it tells you which names are stretched and which have room to bounce.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
