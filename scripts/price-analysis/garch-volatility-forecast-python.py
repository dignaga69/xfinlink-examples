# Full write-up: https://xfinlink.com/blog/garch-volatility-forecast-python

import numpy as np
from arch import arch_model
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Fetch 1Y daily returns for four stocks ---------------------------------
tickers = ["AAPL", "NVDA", "XOM", "JPM"]
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print("=== GARCH(1,1) Volatility Forecast ===")
print("(Fits a GARCH model to daily returns, forecasts next-day volatility)")
print()

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").copy()
    df = df.dropna(subset=["return_daily"])

    # Scale returns to percent (arch package convention)
    returns_pct = df["return_daily"].values * 100

    # Fit GARCH(1,1)
    model = arch_model(returns_pct, vol="Garch", p=1, q=1, mean="Constant")
    result = model.fit(disp="off")

    omega = result.params["omega"]
    alpha = result.params["alpha[1]"]
    beta = result.params["beta[1]"]
    persistence = alpha + beta

    # Forecast next-day variance
    forecast = result.forecast(horizon=1)
    next_day_var = forecast.variance.iloc[-1, 0]
    next_day_vol_daily = np.sqrt(next_day_var) / 100  # back to decimal
    next_day_vol_annual = next_day_vol_daily * np.sqrt(252)

    # Historical vol for comparison
    hist_vol = df["return_daily"].std() * np.sqrt(252)

    # Classify regime
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
