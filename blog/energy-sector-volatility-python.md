# How to Compare Volatility Across Energy Stocks in Python

Energy stocks are among the most volatile sectors. Understanding each company's risk profile -- annualized vol, rolling vol, and max drawdown -- helps build better energy portfolios.

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

## Discussion

All 6 energy stocks are positive over 1 year -- a strong sector tailwind. MPC delivered the best return (+67.3%) but also had the deepest drawdown (-18.7%).

The interesting signal is the 30-day rolling vol: MPC's recent vol (41.7%) is significantly higher than its annual average (31.4%), suggesting elevated near-term uncertainty. CVX has the lowest vol at 21.8% -- the defensive play within energy.

The sector average of 27.6% is notably higher than the S&P 500's typical 15-18%, confirming energy's reputation as a high-beta sector.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
