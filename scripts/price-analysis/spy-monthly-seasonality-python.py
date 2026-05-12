# Full write-up: https://xfinlink.com/blog/spy-monthly-seasonality-python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

# Analyze monthly seasonality for SPY over 10 years
df = xfl.prices("SPY", period="10y", fields=["close", "return_daily"])

df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Monthly returns: compound daily returns per month
monthly = df.groupby(["year", "month"])["return_daily"].apply(lambda x: (1 + x).prod() - 1).reset_index()
monthly.columns = ["year", "month", "monthly_return"]

# Average return by month
avg = monthly.groupby("month")["monthly_return"].agg(["mean", "std", "count"]).round(4)
avg.columns = ["avg_return", "std", "count"]
avg["win_rate"] = monthly.groupby("month")["monthly_return"].apply(lambda x: (x > 0).mean()).round(2)

month_names = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
               7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
avg.index = avg.index.map(month_names)

print("=== SPY Monthly Seasonality (10-Year Average) ===")
print(avg.to_string())
print()

best = avg["avg_return"].idxmax()
worst = avg["avg_return"].idxmin()
print(f"Best month:  {best} (avg +{avg.loc[best, 'avg_return']:.2%}, wins {avg.loc[best, 'win_rate']:.0%} of the time)")
print(f"Worst month: {worst} (avg {avg.loc[worst, 'avg_return']:.2%}, wins {avg.loc[worst, 'win_rate']:.0%} of the time)")
