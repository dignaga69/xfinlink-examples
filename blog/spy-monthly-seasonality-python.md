# Is "Sell in May" Real? SPY Monthly Seasonality Over 10 Years

"Sell in May and go away" is one of the oldest market adages. But does it hold up in recent data? By calculating the average monthly return for SPY over the last 10 years, we can see which months actually deliver and which ones are statistical dead zones. The answer might surprise you.

```python
import xfinlink as xfl
import pandas as pd
import numpy as np

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== SPY Monthly Seasonality (10-Year Average) ===
       avg_return     std  count  win_rate
month                                     
Jan        0.0211  0.0387     10      0.70
Feb       -0.0040  0.0412     10      0.40
Mar       -0.0090  0.0556     10      0.60
Apr        0.0220  0.0637     10      0.70
May        0.0166  0.0338     11      0.91
Jun        0.0191  0.0430     10      0.90
Jul        0.0352  0.0241     10      1.00
Aug        0.0106  0.0313     10      0.70
Sep       -0.0124  0.0410     10      0.60
Oct        0.0079  0.0457     10      0.50
Nov        0.0431  0.0369     10      0.90
Dec        0.0019  0.0455     10      0.60

Best month:  Nov (avg +4.31%, wins 90% of the time)
Worst month: Sep (avg -1.24%, wins 60% of the time)
```

"Sell in May" is wrong — May has actually been positive 91% of the time over the last decade with an average return of +1.7%. The real seasonal pattern: November is the best month (+4.3%, 90% win rate) and September is the worst (-1.2%). July is remarkable: +3.5% average with a 100% win rate — it was positive every single year for 10 years. The months to actually worry about are February, March, and September — the only three with negative average returns.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
