# How to Forecast Stock Volatility with GARCH Models in Python

## What's the question?

Historical volatility -- the standard deviation of past returns -- is backward-looking by definition. It tells you how much a stock moved, not how much it is likely to move tomorrow. For risk management, options pricing, and position sizing, the relevant quantity is forward-looking volatility. The question is whether past return behavior contains enough structure to forecast future volatility, and specifically whether volatility shocks persist (cluster) or dissipate quickly. A stock where a single large move predicts continued elevated volatility requires different risk management than one where shocks fade rapidly back to baseline.

## The approach

The GARCH(1,1) model -- Generalized Autoregressive Conditional Heteroskedasticity -- is the standard parametric model for volatility forecasting. It decomposes the conditional variance (the variance of tomorrow's return, given today's information) into three components: a long-run baseline variance (omega), the impact of yesterday's squared return shock (alpha), and the persistence of yesterday's conditional variance (beta). The sum alpha + beta is called persistence: values near 1.0 mean volatility shocks decay slowly (strong clustering), while values well below 1.0 mean shocks dissipate quickly.

Four stocks with different volatility profiles are tested: Apple (AAPL), Nvidia (NVDA), ExxonMobil (XOM), and JPMorgan (JPM). One year of daily returns is fitted to a GARCH(1,1) specification using maximum likelihood estimation. The model then forecasts next-day volatility, which is compared against historical annualized volatility to classify the current regime as HIGH (forecast exceeds historical by 20%+), LOW (forecast is 20%+ below historical), or NORMAL.

## Code

```python
import numpy as np
from arch import arch_model
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["AAPL", "NVDA", "XOM", "JPM"]
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print("=== GARCH(1,1) Volatility Forecast ===")
print("(Fits a GARCH model to daily returns, forecasts next-day volatility)")
print()

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").copy()
    df = df.dropna(subset=["return_daily"])

    returns_pct = df["return_daily"].values * 100

    model = arch_model(returns_pct, vol="Garch", p=1, q=1, mean="Constant")
    result = model.fit(disp="off")

    omega = result.params["omega"]
    alpha = result.params["alpha[1]"]
    beta = result.params["beta[1]"]
    persistence = alpha + beta

    forecast = result.forecast(horizon=1)
    next_day_var = forecast.variance.iloc[-1, 0]
    next_day_vol_daily = np.sqrt(next_day_var) / 100
    next_day_vol_annual = next_day_vol_daily * np.sqrt(252)

    hist_vol = df["return_daily"].std() * np.sqrt(252)

    if next_day_vol_annual > hist_vol * 1.2:
        regime = "HIGH"
    elif next_day_vol_annual < hist_vol * 0.8:
        regime = "LOW"
    else:
        regime = "NORMAL"

    print(f"  {ticker}:")
    print(f"    GARCH params: omega={omega:.4f}  alpha={alpha:.4f}  beta={beta:.4f}  persistence={persistence:.4f}")
    print(f"    Forecast next-day vol: {next_day_vol_daily*100:.2f}% daily = {next_day_vol_annual*100:.1f}% annualized")
    print(f"    Historical vol:        {hist_vol*100:.1f}% annualized")
    print(f"    Regime: {regime}")
    print()
```

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

## What this tells us

The persistence parameter divides these four stocks into two distinct volatility regimes. AAPL (persistence = 0.35) and NVDA (persistence = 0.56) exhibit low to moderate persistence, meaning that after a volatility shock -- a large daily move in either direction -- the elevated volatility fades relatively quickly back toward its long-run level. Their forecast volatilities (22.0% and 32.6%) are close to their historical volatilities (22.5% and 33.5%), confirming that both stocks are currently in a normal volatility state.

XOM and JPM tell a fundamentally different story. Both have persistence values near 1.0 (0.999 for each), indicating extreme volatility clustering -- once these stocks begin moving, the elevated volatility tends to self-perpetuate. The GARCH model reflects this by forecasting volatility substantially above the historical average: XOM's forecast of 30.3% annualized exceeds its 23.6% historical vol by 28%, and JPM's 25.6% forecast exceeds its 21.1% historical vol by 21%. Both are classified as HIGH regime.

The near-zero omega values for XOM (0.012) and JPM (0.008), combined with beta values near 1.0, mean that the long-run variance contributes almost nothing to the forecast. Tomorrow's volatility is almost entirely determined by today's volatility -- a purely autoregressive process. In contrast, AAPL's large omega (1.30) relative to its beta (0.26) means the long-run baseline dominates, producing mean-reverting volatility behavior.

## So what?

For position sizing and risk management, the practical implication is direct. If you are using historical volatility to set position sizes or stop-loss levels, you are underestimating current risk for XOM and JPM by approximately 25-30%. The GARCH forecast provides a more accurate estimate of near-term risk because it incorporates the clustering effect. For AAPL and NVDA, historical volatility is an adequate proxy because their volatility mean-reverts quickly. The regime classification (NORMAL vs. HIGH) can serve as a simple signal: when a stock enters a HIGH volatility regime, reduce position size or widen stops to account for the persistence of elevated moves.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
