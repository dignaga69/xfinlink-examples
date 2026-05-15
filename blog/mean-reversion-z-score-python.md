# How to Find Oversold and Overbought Stocks Using Z-Scores in Python

## What's the question?

When a stock deviates significantly from its recent average price, is it extended enough to warrant attention as a potential reversal candidate? Mean reversion — the tendency of prices to gravitate back toward a moving average over time — is one of the most widely traded concepts in quantitative finance. The challenge is defining "significantly deviated" in a way that is consistent across stocks with different price levels and volatility profiles.

## The approach

A z-score measures how many standard deviations a value is from its mean. Applied to stock prices, we compute each stock's 50-day simple moving average (SMA) and the rolling 50-day standard deviation of closing prices. The z-score is then `(current price - SMA) / standard deviation`. A z-score below -1.5 indicates the stock is trading more than 1.5 standard deviations below its 50-day average — statistically oversold. Above +1.5, the stock is statistically overbought.

The advantage of z-scores over raw price gaps is standardization: a 5% deviation from the SMA means something very different for a low-volatility stock like PG than for a high-volatility stock like NVDA. Z-scores normalize for this difference, making signals comparable across names.

We screen 10 large-cap stocks spanning technology, energy, healthcare, and consumer staples.

## Code

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

## Output

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

## What this tells us

JNJ is the only stock triggering the oversold threshold at z = -1.93, trading 6.1% below its 50-day moving average. On the opposite end, GOOGL is the most statistically extended at z = +3.28, sitting 22.6% above its 50-day average — an extreme reading by any historical standard.

Three stocks trigger the overbought signal: NVDA (+2.14), AAPL (+2.46), and GOOGL (+3.28). All three are technology-related names, suggesting the recent rally in that sector may be stretched relative to its own recent trend. JPM sits almost exactly on its 50-day average (z = -0.00), reflecting a stock in equilibrium with its recent trading range.

The spread between the most oversold stock (JNJ at -1.93) and the most overbought (GOOGL at +3.28) is 5.21 standard deviations — substantial cross-sectional dispersion that indicates the market is not moving uniformly.

## So what?

Z-score screens identify statistical extension, not directional prediction. A stock can remain overbought for weeks during a strong trend, and an oversold reading does not guarantee a bounce. The value of this screen is in identifying which names are stretched and which have room to move, providing a starting point for further analysis rather than a standalone trade signal. For portfolio managers, z-scores also serve as a risk tool: concentrated positions in stocks with extreme z-scores carry elevated reversion risk regardless of the fundamental thesis.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
