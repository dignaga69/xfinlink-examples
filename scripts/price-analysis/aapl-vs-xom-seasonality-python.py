# Full write-up: https://xfinlink.com/blog/aapl-vs-xom-seasonality-python

import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"

# -- Two stocks with different seasonal drivers ---------------------------
tickers = ["AAPL", "XOM"]

# -- Fetch 5 complete years (2021-2025) using start/end -------------------
prices = xfl.prices(
    tickers,
    start="2021-01-01",
    end="2025-12-31",
    fields=["close", "return_daily"],
)

# -- Compute monthly returns per ticker -----------------------------------
import pandas as pd

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Assign year and month
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Compound daily returns into monthly returns
    monthly = (
        df.groupby(["year", "month"])["return_daily"]
        .apply(lambda x: (1 + x).prod() - 1)
        .reset_index()
    )
    monthly.columns = ["year", "month", "monthly_return"]

    # Filter to complete years only (2021-2025)
    monthly = monthly[monthly["year"].between(2021, 2025)]

    print(f"=== {ticker} Monthly Seasonality (2021-2025, 5 complete years) ===")

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]

    for m in range(1, 13):
        subset = monthly[monthly["month"] == m]
        avg_ret = subset["monthly_return"].mean()
        win_rate = (subset["monthly_return"] > 0).mean()
        n = len(subset)

        # Visual bar
        bar_len = int(abs(avg_ret) * 200)
        bar = ("+" if avg_ret >= 0 else "-") * bar_len

        print(
            f"  {month_names[m-1]}  avg={avg_ret:+5.1%}"
            f"  wins={win_rate:.0%}"
            f"  n={n}"
            f"  {bar}"
        )

    print()
