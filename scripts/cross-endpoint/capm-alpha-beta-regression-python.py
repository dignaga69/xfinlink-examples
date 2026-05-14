# Full write-up: https://xfinlink.com/blog/capm-alpha-beta-regression-python

import numpy as np
from scipy import stats
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "XOM", "JNJ", "JPM"]
benchmark = "SPY"
rf_annual = 0.05  # 5% risk-free rate
rf_daily = rf_annual / 252

# -- Fetch 1Y daily returns -------------------------------------------------
all_tickers = tickers + [benchmark]
prices = xfl.prices(all_tickers, period="1y", fields=["return_daily"])

# -- Pivot to wide format ----------------------------------------------------
pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot.dropna()

# -- Compute excess returns --------------------------------------------------
spy_excess = pivot[benchmark] - rf_daily

print(f"=== CAPM Regression: Alpha, Beta, R² (1Y vs SPY, Rf={int(rf_annual*100)}%) ===")
print()
header = f"{'Ticker':<10}{'Beta':>6}   {'Alpha (ann)':>11}   {'R²':>5}   {'Ann Return':>10}        {'Interpretation'}"
print(header)
print("-" * len(header))

results = []

for ticker in tickers:
    stock_excess = pivot[ticker] - rf_daily

    # OLS regression: stock_excess = alpha + beta * spy_excess + epsilon
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        spy_excess.values, stock_excess.values
    )

    beta = slope
    alpha_daily = intercept
    alpha_annual = alpha_daily * 252
    r_squared = r_value ** 2

    # Annualized total return
    total_return = (1 + pivot[ticker]).prod() - 1
    ann_return = total_return  # already 1Y

    # Interpretation
    if alpha_annual > 0.05:
        interp = "OUTPERFORM"
    elif alpha_annual < -0.05:
        interp = "UNDERPERFORM"
    else:
        interp = "FAIR"

    results.append((ticker, beta, alpha_annual, r_squared, ann_return, interp))

# Sort by alpha descending
results.sort(key=lambda x: x[2], reverse=True)

for ticker, beta, alpha_annual, r_squared, ann_return, interp in results:
    print(
        f"{ticker:<10}"
        f"{beta:6.2f}   "
        f"{alpha_annual:+10.1%}   "
        f"{r_squared:5.3f}   "
        f"{ann_return:+10.1%}   "
        f"{'':>8}{interp}"
    )
