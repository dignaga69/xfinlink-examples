# How to Compare Volatility Across Energy Stocks in Python

## What's the question?

How does risk differ among major energy companies, and is recent volatility consistent with the longer-term pattern? Energy stocks are among the most volatile in the equity market, driven by commodity price fluctuations, geopolitical events, and capital expenditure cycles. But "energy" is not monolithic — an integrated major like Exxon Mobil behaves differently from an oilfield services company like Schlumberger or a refiner like Marathon Petroleum. Quantifying each company's volatility profile identifies the defensive and aggressive options within the sector.

## The approach

We calculate three risk metrics for six major energy companies over a one-year window. Annualized volatility is the standard deviation of daily returns multiplied by the square root of 252 (the typical number of trading days per year), representing the expected range of annual returns under normal conditions. The 30-day rolling volatility provides a snapshot of recent risk levels, which may diverge from the annual figure during periods of elevated uncertainty. Maximum drawdown — the largest peak-to-trough decline during the period — measures the worst-case experienced loss. Together, these three metrics characterize each stock's risk profile from different angles.

## Code

See [`energy-sector-volatility-python.py`](energy-sector-volatility-python.py)

## Output

```
=== Energy Sector Volatility Profile (1Y) ===
  SLB    SCHLUMBERGER LTD           vol=33.4%  30d_vol=30.0%  drawdown=-15.0%  return=+59.0%
  MPC    MARATHON PETROLEUM CORP    vol=31.4%  30d_vol=41.7%  drawdown=-18.7%  return=+67.3%
  COP    CONOCOPHILLIPS             vol=29.4%  30d_vol=36.0%  drawdown=-14.9%  return=+30.4%
  EOG    EOG RESOURCES INC          vol=25.9%  30d_vol=32.3%  drawdown=-19.3%  return=+20.0%
  XOM    EXXON MOBIL CORP           vol=23.6%  30d_vol=32.5%  drawdown=-15.7%  return=+39.5%
  CVX    CHEVRON CORP               vol=21.8%  30d_vol=29.0%  drawdown=-14.0%  return=+33.4%

Sector avg volatility: 27.6%
```

## What this tells us

All six energy stocks posted positive one-year returns, reflecting a broad sector tailwind. However, the risk profiles differ substantially. MPC delivered the highest return (+67.3%) but also suffered the deepest drawdown (-18.7%), and its 30-day rolling volatility of 41.7% is significantly elevated relative to its annual average of 31.4%. This divergence indicates heightened near-term uncertainty — the recent trading environment for MPC has been materially more volatile than the past year on average.

CVX sits at the opposite end of the spectrum with the lowest annualized volatility (21.8%) and the shallowest drawdown (-14.0%), making it the defensive option within the energy sector. SLB, as an oilfield services company with more cyclical revenue tied to upstream drilling activity, has the highest annualized volatility at 33.4%.

The sector average volatility of 27.6% is notably higher than the S&P 500's typical range of 15-18%, confirming energy's higher-beta characteristics relative to the broad market.

## So what?

Volatility profiling within a sector enables informed position sizing. An investor with a fixed risk budget can hold a larger position in CVX than in SLB while maintaining the same portfolio-level risk contribution. The divergence between annualized and 30-day rolling volatility is also actionable: when recent volatility exceeds the annual average (as with MPC), it signals a regime shift that may warrant hedging or position reduction regardless of the fundamental outlook.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
