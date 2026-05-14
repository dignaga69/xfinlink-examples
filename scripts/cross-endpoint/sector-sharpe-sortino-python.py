# Full write-up: https://xfinlink.com/blog/sector-sharpe-sortino-python

import numpy as np
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Sector ETFs (SPDR) -----------------------------------------------------
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

# -- Fetch 1Y daily data ----------------------------------------------------
prices = xfl.prices(tickers, period="1y", fields=["close", "return_daily"])

print(f"=== Sector Risk-Adjusted Returns: Sharpe & Sortino (1Y, Rf={int(rf_annual*100)}%) ===")
print()

results = []

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].sort_values("date").copy()
    df = df.dropna(subset=["close", "return_daily"])

    returns = df["return_daily"].values
    close = df["close"].values

    # Annualized return
    total_return = close[-1] / close[0] - 1

    # Annualized volatility
    vol = np.std(returns, ddof=1) * np.sqrt(252)

    # Sharpe ratio
    sharpe = (total_return - rf_annual) / vol

    # Sortino ratio (downside deviation only)
    excess_returns = returns - rf_daily
    downside = excess_returns[excess_returns < 0]
    downside_dev = np.sqrt(np.mean(downside ** 2)) * np.sqrt(252)
    sortino = (total_return - rf_annual) / downside_dev

    # Max drawdown
    cummax = np.maximum.accumulate(close)
    drawdowns = close / cummax - 1
    max_dd = drawdowns.min()

    results.append((sectors[ticker], ticker, total_return, vol, sharpe, sortino, max_dd))

# Sort by Sharpe descending
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
