# Is "Sell in May" Real? SPY Monthly Seasonality Over 10 Years

## What's the question?

"Sell in May and go away" is one of the oldest adages in equity markets. The claim is simple: returns during the May-through-October period are systematically weaker than during November-through-April, making it rational to exit equities for the summer months. The saying dates back to at least the 1930s and has been cited in academic literature, financial media, and trading desks ever since.

But adages are not evidence. The question is whether recent data supports the pattern, and if so, whether the effect is concentrated in specific months or spread evenly across the "weak" half of the year. By calculating the average monthly return, standard deviation, and win rate (the percentage of years a given month was positive) for SPY over the past 10 years, we can identify which months actually delivered and which were statistical dead zones.

## The approach

We retrieve 10 years of daily SPY price data and compute compound monthly returns by grouping daily returns within each calendar month. For each of the 12 months, we calculate three statistics: the average monthly return, the standard deviation of monthly returns (a measure of consistency), and the win rate. A high win rate with a positive average return indicates a reliably strong month. A negative average return, regardless of win rate, marks a month where the expected outcome is a loss.

## Code

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

## Output

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

## What this tells us

The "Sell in May" thesis does not hold in the most recent decade of data. May itself has been positive 91% of the time with an average return of +1.7%, making it one of the most reliable months of the year. The summer months (June and July) are also strong: June averages +1.9% with a 90% win rate, and July is the most remarkable month in the dataset at +3.5% with a 100% win rate — positive every single year for 10 consecutive years.

The actual seasonal weakness is concentrated in three months: February (-0.4%), March (-0.9%), and September (-1.2%). These are the only months with negative average returns. September is the worst, consistent with the well-documented "September effect" observed across decades of market data.

November is the single best month at +4.3% with a 90% win rate, and its low standard deviation (0.0369) relative to its mean indicates that the result is consistent rather than driven by a few outlier years.

## So what?

Seasonal patterns are descriptive, not predictive. A 10-year sample is too small for statistical significance on any individual month, and the composition of the S&P 500 changes materially over a decade. That said, the data directly contradicts the "Sell in May" narrative for this period. If anything, the weakest seasonal window is late winter (February-March) and early fall (September), not the summer months. Investors relying on calendar-based timing rules should test them against actual data before acting — and this analysis demonstrates how to do that in a few lines of code.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
