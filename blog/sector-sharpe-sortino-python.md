# How to Compare Sector Sharpe Ratios and Sortino Ratios in Python

Raw returns lie about risk. A sector returning 30% with 30% vol is worse risk-adjusted than one returning 15% with 10% vol. The Sharpe ratio normalizes return by total volatility; the Sortino ratio only penalizes downside volatility — useful when you care more about losses than fluctuations.

## Code

See [`sector-sharpe-sortino-python.py`](sector-sharpe-sortino-python.py)

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

## Discussion

Tech dominates risk-adjusted returns with a Sharpe of 2.48 — exceptional by any standard (above 2.0 is rare over a full year). Energy is second at 1.60, delivering strong absolute returns with comparable vol to tech. Financials is the only sector with negative Sharpe (-0.29), meaning the risk-free T-bill at 5% beat XLF. The Sortino ratio tells a more nuanced story: Tech's Sortino (3.62) is much higher than its Sharpe (2.48), meaning most of its volatility was upside — exactly what you want. Financials' Sortino (-0.39) is worse than its Sharpe (-0.29), indicating more downside than upside vol.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
