# How to Compare Sector Sharpe Ratios and Sortino Ratios in Python

## What's the question?

Raw returns are misleading as a measure of investment quality because they ignore the risk required to achieve them. A sector returning 30% with 30% volatility is worse on a risk-adjusted basis than one returning 15% with 10% volatility. The Sharpe ratio normalizes return by total volatility, answering the question: how much excess return did this sector generate per unit of total risk? The Sortino ratio refines this further by penalizing only downside volatility -- deviation below the risk-free rate -- on the premise that upside volatility is desirable rather than penalizable. Which U.S. equity sectors delivered the best risk-adjusted returns, and does the distinction between total volatility and downside volatility change the ranking?

## The approach

Eight SPDR sector ETFs are evaluated over one year of daily price data: Technology (XLK), Energy (XLE), Industrials (XLI), Utilities (XLU), Healthcare (XLV), Consumer Discretionary (XLY), Consumer Staples (XLP), and Financials (XLF). For each sector, four metrics are computed. The Sharpe ratio is calculated as (annualized return minus risk-free rate) divided by annualized volatility, where the risk-free rate is set at 5% to reflect prevailing Treasury yields. The Sortino ratio replaces total volatility in the denominator with downside deviation -- the root mean square of negative excess daily returns, annualized by multiplying by the square root of 252. Maximum drawdown (the largest peak-to-trough decline) provides additional context on tail risk. Sectors are ranked by Sharpe ratio.

## Code

```python
import numpy as np
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

sectors = {
    "XLK": "Technology",
    "XLE": "Energy",
    "XLI": "Industrials",
    "XLU": "Utilities",
    "XLV": "Healthcare",
    "XLY": "ConsDisc",
    "XLP": "ConsStaples",
    "XLF": "Financials",
}
tickers = list(sectors.keys())
rf_annual = 0.05
rf_daily = rf_annual / 252

prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print(f"=== Sector Risk-Adjusted Returns: Sharpe & Sortino (1Y, Rf={int(rf_annual*100)}%) ===")
print()

results = []

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").copy()
    df = df.dropna(subset=["close", "return_daily"])

    returns = df["return_daily"].values
    close = df["close"].values

    total_return = close[-1] / close[0] - 1

    vol = np.std(returns, ddof=1) * np.sqrt(252)

    sharpe = (total_return - rf_annual) / vol

    excess_returns = returns - rf_daily
    downside = excess_returns[excess_returns < 0]
    downside_dev = np.sqrt(np.mean(downside ** 2)) * np.sqrt(252)
    sortino = (total_return - rf_annual) / downside_dev

    cummax = np.maximum.accumulate(close)
    drawdowns = close / cummax - 1
    max_dd = drawdowns.min()

    results.append((sectors[ticker], ticker, total_return, vol, sharpe, sortino, max_dd))

results.sort(key=lambda x: x[4], reverse=True)

for name, ticker, ret, vol, sharpe, sortino, max_dd in results:
    print(
        f"  {name:<15}({ticker})  "
        f"return={ret:+5.1%}  "
        f"vol={vol:4.1%}  "
        f"sharpe={sharpe:+5.2f}  "
        f"sortino={sortino:+5.2f}  "
        f"maxDD={max_dd:5.1%}"
    )
```

## Output

```
=== Sector Risk-Adjusted Returns: Sharpe & Sortino (1Y, Rf=5%) ===

  Technology     (XLK)  return=+55.5%  vol=20.3%  sharpe=+2.48  sortino=+3.62  maxDD=-16.2%
  Energy         (XLE)  return=+37.3%  vol=20.1%  sharpe=+1.60  sortino=+2.44  maxDD=-12.1%
  Industrials    (XLI)  return=+24.4%  vol=15.3%  sharpe=+1.27  sortino=+2.14  maxDD=-12.5%
  Utilities      (XLU)  return=+13.4%  vol=14.3%  sharpe=+0.58  sortino=+0.88  maxDD= -9.9%
  Healthcare     (XLV)  return=+12.6%  vol=15.0%  sharpe=+0.50  sortino=+0.87  maxDD=-10.8%
  ConsDisc       (XLY)  return=+12.1%  vol=18.0%  sharpe=+0.40  sortino=+0.63  maxDD=-15.1%
  ConsStaples    (XLP)  return= +6.9%  vol=12.7%  sharpe=+0.15  sortino=+0.24  maxDD= -9.9%
  Financials     (XLF)  return= +0.9%  vol=14.4%  sharpe=-0.29  sortino=-0.39  maxDD=-15.2%
```

## What this tells us

Technology dominates risk-adjusted returns with a Sharpe ratio of 2.48 -- a level that is exceptional by historical standards, as sustained Sharpe ratios above 2.0 over a full year are rare for any asset class. Despite a maximum drawdown of -16.2% (the second deepest in the group), the 55.5% return more than compensated for the volatility incurred.

The gap between Technology's Sharpe (2.48) and Sortino (3.62) reveals an important characteristic of the return distribution. The Sortino ratio is higher than the Sharpe ratio when a disproportionate share of the total volatility comes from upside moves. In Technology's case, the large gap (3.62 vs. 2.48) indicates that most of the sector's daily return variance was on the positive side -- exactly the type of volatility investors welcome.

Energy ranks second on both measures (Sharpe 1.60, Sortino 2.44), delivering comparable volatility to Technology (20.1% vs. 20.3%) but lower absolute returns. The similar Sharpe-to-Sortino ratio gap suggests Energy also exhibited more upside than downside volatility during this period.

Financials is the only sector with a negative Sharpe ratio (-0.29), meaning the 5% risk-free Treasury rate outperformed XLF on a risk-adjusted basis. The Sortino ratio (-0.39) is more negative than the Sharpe ratio, which is the inverse of the Technology pattern: Financials experienced more downside volatility than upside, and its 15.2% maximum drawdown was the deepest in the group despite generating only 0.9% in returns.

Consumer Staples and Utilities, while posting positive Sharpe ratios, barely exceeded the risk-free rate. Their low volatility (12.7% and 14.3%) keeps the ratios positive, but the near-zero excess returns raise the question of whether the equity risk premium justified the allocation relative to Treasury bills.

## So what?

Risk-adjusted metrics should be the primary basis for sector comparison and allocation decisions, not raw returns. A sector with moderate returns and low downside volatility (high Sortino) may be a better allocation choice than one with higher returns but symmetric or negatively skewed volatility. The Sharpe-to-Sortino ratio gap is itself informative: sectors where Sortino significantly exceeds Sharpe have favorable return distributions (more upside than downside), while sectors where Sortino is worse than Sharpe have unfavorable distributions. Use both ratios together to distinguish between total risk and the risk that actually matters -- losses.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
