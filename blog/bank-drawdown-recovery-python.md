# How to Analyze Drawdown and Recovery for Bank Stocks in Python

## What's the question?

Bank stocks are among the most cyclical in the equity market, driven by interest rate expectations, credit conditions, and macroeconomic sentiment. When the sector sells off, the critical question for portfolio managers is not just how far each stock falls, but how quickly it recovers. A stock that draws down 20% and recovers in 30 days presents a fundamentally different risk profile than one that draws down 20% and remains underwater for months. Which major U.S. banks recover fastest from peak-to-trough declines, and which tend to stay impaired?

## The approach

Drawdown analysis measures the percentage decline from a stock's running peak to its subsequent trough. For each of five major bank stocks -- Bank of America (BAC), Goldman Sachs (GS), Morgan Stanley (MS), Wells Fargo (WFC), and Citigroup (C) -- one year of daily price data is used to compute the cumulative return series, the running maximum (high-water mark), and the drawdown at each point in time. The maximum drawdown identifies the worst peak-to-trough decline over the period. Recovery time is measured as the number of trading days from the maximum drawdown date until the cumulative return series first returns to or exceeds the prior peak. If the stock has not yet recovered, it is flagged as still underwater.

## Code

```python
import numpy as np
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["BAC", "GS", "MS", "WFC", "C"]

prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print("=== Bank Stock Drawdown Analysis (1Y) ===")

results = []
for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").reset_index(drop=True)
    if df.empty:
        continue

    entity_name = df["entity_name"].iloc[0]
    returns = df["return_daily"].dropna()
    closes = df["close"]

    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak

    max_dd = drawdown.min()
    max_dd_idx = drawdown.idxmin()
    max_dd_date = df.loc[max_dd_idx, "date"]

    post_dd = drawdown.iloc[max_dd_idx:]
    recovered = post_dd[post_dd >= 0]
    if len(recovered) > 0:
        recovery_idx = recovered.index[0]
        recovery_days = recovery_idx - max_dd_idx
        recovery_str = f"{recovery_days:5d}d"
    else:
        recovery_str = "not yet"

    current_dd = drawdown.iloc[-1]
    ret_1y = (1 + returns).prod() - 1

    results.append({
        "ticker": ticker,
        "entity_name": entity_name,
        "max_dd": max_dd,
        "max_dd_date": max_dd_date,
        "recovery": recovery_str,
        "current_dd": current_dd,
        "return_1y": ret_1y,
    })

results.sort(key=lambda x: x["max_dd"])

for r in results:
    name = r["entity_name"][:22]
    print(
        f"  {r['ticker']:<6} {name:<22}"
        f"  max_dd={r['max_dd']:+.1%}"
        f"  on {r['max_dd_date']}"
        f"  recovery={r['recovery']}"
        f"  now={r['current_dd']:+.1%}"
        f"  1y={r['return_1y']:+.1%}"
    )

avg_dd = np.mean([r["max_dd"] for r in results])
print(f"\nAvg max drawdown: {avg_dd:.1%}")
```

## Output

```
=== Bank Stock Drawdown Analysis (1Y) ===
  WFC   WELLS FARGO & CO        max_dd=-23.7%  on 2026-05-11  recovery=not yet  now=-22.0%  1y= -1.1%
  GS    GOLDMAN SACHS GROUP IN  max_dd=-19.8%  on 2026-03-13  recovery=not yet  now=-3.1%  1y=+56.7%
  MS    MORGAN STANLEY          max_dd=-19.3%  on 2026-03-12  recovery=   34d  now=-0.8%  1y=+48.3%
  BAC   BANK OF AMERICA CORP    max_dd=-18.4%  on 2026-03-13  recovery=not yet  now=-11.3%  1y=+14.7%
  C     CITIGROUP INC           max_dd=-14.8%  on 2026-03-12  recovery=   28d  now=-5.0%  1y=+67.3%

Avg max drawdown: -19.2%
```

## What this tells us

The March 2026 drawdown cluster is the dominant feature of this analysis. Four of the five banks -- Goldman Sachs, Morgan Stanley, Bank of America, and Citigroup -- all hit their maximum drawdowns within a two-day window (March 12-13), indicating a sector-wide shock rather than idiosyncratic company events. This type of synchronous drawdown is characteristic of interest rate or credit contagion, where the entire banking sector reprices simultaneously.

Recovery divergence reveals meaningful differences in perceived quality. Citigroup had the shallowest maximum drawdown (-14.8%) and the fastest recovery (28 trading days), while also delivering the strongest one-year return (+67.3%). Morgan Stanley recovered in 34 days. Goldman Sachs, despite strong one-year performance (+56.7%), has not fully recovered from its March trough. Wells Fargo is the clear outlier: the deepest drawdown (-23.7%), the only negative one-year return (-1.1%), and no recovery in sight.

The average maximum drawdown across the five banks of -19.2% is broadly consistent with the broader market, suggesting bank stocks did not materially underperform during this period on a drawdown basis, though recovery times varied widely.

## So what?

Drawdown and recovery metrics are more informative than raw returns for risk management. A stock with a strong one-year return but a deep, unrecovered drawdown (like GS or BAC) signals that much of the gain occurred before the drawdown event -- an investor who entered at the wrong time experienced a very different outcome than the annualized return implies. When evaluating bank stocks after a sector sell-off, recovery speed is a useful signal: the stocks that recover fastest tend to be those the market views as best-positioned for the prevailing rate environment.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
