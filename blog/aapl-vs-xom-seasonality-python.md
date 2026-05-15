# AAPL vs XOM: Do Individual Stocks Have Seasonal Patterns?

## What's the question?

Broad market seasonality -- the "sell in May" effect, the January effect, the Santa Claus rally -- is well documented in academic literature and widely discussed among practitioners. But individual stocks have their own business cycles that differ from the market as a whole. Apple has a product launch calendar (September iPhone events, June WWDC), while ExxonMobil's revenue is tied to seasonal energy demand (winter heating, summer driving). Do these company-specific cycles produce measurable monthly return patterns, and if so, do the patterns differ enough between stocks to create calendar-based diversification opportunities?

## The approach

Five complete calendar years of daily price data (2021-2025) are fetched for both Apple (AAPL) and ExxonMobil (XOM). Daily returns are compounded within each calendar month to produce monthly returns, then averaged across all five instances of each month to compute the mean monthly return, win rate (percentage of years with a positive return for that month), and sample size. The five-year window provides enough data to identify persistent patterns while remaining recent enough to reflect current business dynamics. A visual bar chart scales with the magnitude of the average return, using "+" for positive months and "-" for negative months.

## Code

```python
import pandas as pd
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["AAPL", "XOM"]

prices = xfl.prices(
    tickers,
    start="2021-01-01",
    end="2025-12-31",
    fields=["close", "return_daily"],
)

for ticker in tickers:
    df = prices[prices["ticker"] == ticker].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    monthly = (
        df.groupby(["year", "month"])["return_daily"]
        .apply(lambda x: (1 + x).prod() - 1)
        .reset_index()
    )
    monthly.columns = ["year", "month", "monthly_return"]

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

        bar_len = int(abs(avg_ret) * 200)
        bar = ("+" if avg_ret >= 0 else "-") * bar_len

        print(
            f"  {month_names[m-1]}  avg={avg_ret:+5.1%}"
            f"  wins={win_rate:.0%}"
            f"  n={n}"
            f"  {bar}"
        )

    print()
```

## Output

```
=== AAPL Monthly Seasonality (2021-2025, 5 complete years) ===
  Jan  avg= -0.2%  wins=20%  n=5  
  Feb  avg= -2.1%  wins=40%  n=5  ----
  Mar  avg= +1.0%  wins=60%  n=5  ++
  Apr  avg= -0.8%  wins=40%  n=5  -
  May  avg= +0.3%  wins=40%  n=5  
  Jun  avg= +4.6%  wins=80%  n=5  +++++++++
  Jul  avg= +6.7%  wins=100%  n=5  +++++++++++++
  Aug  avg= +2.4%  wins=60%  n=5  ++++
  Sep  avg= -3.3%  wins=40%  n=5  ------
  Oct  avg= +3.9%  wins=60%  n=5  +++++++
  Nov  avg= +5.4%  wins=80%  n=5  ++++++++++
  Dec  avg= -0.1%  wins=60%  n=5  

=== XOM Monthly Seasonality (2021-2025, 5 complete years) ===
  Jan  avg= +8.1%  wins=80%  n=5  ++++++++++++++++
  Feb  avg= +6.0%  wins=80%  n=5  ++++++++++++
  Mar  avg= +5.2%  wins=80%  n=5  ++++++++++
  Apr  avg= +0.9%  wins=80%  n=5  +
  May  avg= +0.2%  wins=40%  n=5  
  Jun  avg= +1.2%  wins=60%  n=5  ++
  Jul  avg= +2.2%  wins=60%  n=5  ++++
  Aug  avg= +0.6%  wins=60%  n=5  +
  Sep  avg= +0.6%  wins=40%  n=5  +
  Oct  avg= +5.5%  wins=60%  n=5  +++++++++++
  Nov  avg= -0.7%  wins=60%  n=5  -
  Dec  avg= -1.3%  wins=40%  n=5  --
```

## What this tells us

The two stocks exhibit nearly opposite seasonal profiles. Apple's strongest months are July (+6.7%, 100% win rate across all five years) and November (+5.4%, 80% win rate). July aligns with the pre-earnings anticipation period -- Apple typically reports fiscal Q3 results in late July or early August, and the run-up reflects positioning ahead of the announcement. November's strength corresponds to holiday season optimism and early Black Friday demand signals. Apple's worst month is September (-3.3%), which is counterintuitive given that Apple's annual iPhone launch event occurs in September. This is a textbook example of the "buy the rumor, sell the news" dynamic: the market prices in the product launch during the summer months, and September marks the point where expectations meet (or fail to meet) reality.

ExxonMobil's seasonal pattern is driven by energy commodity cycles. The first quarter dominates: January (+8.1%), February (+6.0%), and March (+5.2%) all show strong average returns with 80% win rates. This Q1 strength aligns with winter heating demand in the Northern Hemisphere, which supports crude oil and natural gas prices. The fourth quarter is ExxonMobil's weakest period (November -0.7%, December -1.3%), reflecting the seasonal trough between summer driving season and winter heating demand.

The two stocks have essentially zero overlap in their strong months. Apple peaks in summer and fall; ExxonMobil peaks in winter and early spring. This complementary seasonal structure means that a portfolio holding both stocks benefits from calendar-based diversification -- when one stock is in its historically weak season, the other is typically in its strong season.

## So what?

Seasonal patterns in individual stocks are suggestive but not predictive with high confidence, given the small sample size (five observations per month). They are best used as a secondary input: if fundamental analysis already favors a position, seasonal tendencies can inform the timing of entry and exit. The AAPL-XOM comparison also illustrates that sector diversification provides calendar diversification as a byproduct -- holding stocks with different business cycle exposures naturally smooths returns across the year.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
