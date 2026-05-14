# How to Forecast Stock Volatility with GARCH Models in Python

Historical volatility looks backward. GARCH models forecast forward — estimating tomorrow's volatility based on today's return and the persistence of past volatility shocks. A GARCH persistence near 1.0 means volatility clusters; a low persistence means shocks fade quickly.

## Code

See [`garch-volatility-forecast-python.py`](garch-volatility-forecast-python.py)

## Output

```
=== GARCH(1,1) Volatility Forecast ===
(Fits a GARCH model to daily returns, forecasts next-day volatility)

  AAPL:
    GARCH params: omega=1.3003  alpha=0.0909  beta=0.2600  persistence=0.3509
    Forecast next-day vol: 1.38% daily = 22.0% annualized
    Historical vol:        22.5% annualized
    Regime: NORMAL

  NVDA:
    GARCH params: omega=1.9419  alpha=0.0875  beta=0.4749  persistence=0.5624
    Forecast next-day vol: 2.05% daily = 32.6% annualized
    Historical vol:        33.5% annualized
    Regime: NORMAL

  XOM:
    GARCH params: omega=0.0120  alpha=0.0305  beta=0.9682  persistence=0.9987
    Forecast next-day vol: 1.91% daily = 30.3% annualized
    Historical vol:        23.6% annualized
    Regime: HIGH

  JPM:
    GARCH params: omega=0.0083  alpha=0.0000  beta=0.9992  persistence=0.9992
    Forecast next-day vol: 1.61% daily = 25.6% annualized
    Historical vol:        21.1% annualized
    Regime: HIGH
```

## Discussion

XOM and JPM both flash "HIGH" regime — their GARCH persistence is near 1.0 (0.999), meaning recent volatility shocks are persisting rather than fading. This is the volatility clustering effect: once XOM or JPM starts moving, the elevated vol tends to continue. AAPL and NVDA show lower persistence (0.35 and 0.56), meaning their volatility shocks fade faster — more "return to normal" behavior. The practical takeaway: if you're sizing positions using historical vol, you're underestimating current risk for XOM and JPM.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
