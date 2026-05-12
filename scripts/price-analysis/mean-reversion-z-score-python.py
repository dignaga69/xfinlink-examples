# Full write-up: https://xfinlink.com/blog/mean-reversion-z-score-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
