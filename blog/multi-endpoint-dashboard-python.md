# How to Build a Multi-Endpoint Financial Dashboard in Python

## What's the question?

Can we combine index composition, price history, fundamental data, and valuation metrics into a single unified view of a stock — and do so without introducing survivorship bias? Real financial analysis rarely depends on a single data type. Understanding a company requires prices (what the market thinks), fundamentals (what the company earns and owns), and metrics (how the market values those earnings). Building a pipeline that joins all three against a point-in-time index membership list ensures that the analysis reflects what was actually investable on a given date, not a retroactively curated universe.

## The approach

The pipeline operates in four steps. First, we retrieve the S&P 500 constituent list as of January 1, 2020, using the `as_of` parameter to get point-in-time composition. This prevents survivorship bias — the systematic error of testing only on companies that survived to the present. Second, we confirm that our 10 target stocks were members of the 2020 index. Third, we pull one year of daily price data and compute 1-year total returns by compounding daily returns. Fourth, we join the price-derived returns with annual fundamentals (revenue) and metrics (PE ratio, ROE) from the most recent filing period.

The result is a single table combining market-based return data with accounting-based fundamental data, anchored to historically accurate index membership.

## Code

See [`multi-endpoint-dashboard-python.py`](multi-endpoint-dashboard-python.py)

## Output

```
Step 1: 493 unique S&P 500 members as of 2020-01-01
Step 2: 10/10 confirmed in 2020 index
Step 3: 2510 price rows
Step 4-5: Combined

=== Multi-Endpoint Dashboard: 1Y Return + Fundamentals + Metrics ===
(Survivorship-bias-free: tickers confirmed in 2020 S&P 500)

  AAPL   1y=+47.4%  rev= $416B  PE= 39.2  ROE=151.9%
  JNJ    1y=+43.6%  rev=  $94B  PE= 20.1  ROE= 32.9%
  XOM    1y=+39.5%  rev= $332B  PE= 22.3  ROE= 11.1%
  AMZN   1y=+39.3%  rev= $717B  PE= 37.5  ROE= 18.9%
  JPM    1y=+18.5%  rev= $182B  PE= 15.0  ROE= 15.7%
  UNH    1y= +1.0%  rev= $448B  PE= 29.1  ROE= 12.0%
  MSFT   1y= -5.9%  rev= $282B  PE= 30.2  ROE= 29.6%
  PG     1y= -9.1%  rev=  $84B  PE= 22.0  ROE= 30.6%
  HD     1y=-14.1%  rev= $165B  PE= 21.9  ROE=110.5%
  CRM    1y=-35.6%  rev=  $38B  PE= 27.9  ROE= 10.1%
```

## What this tells us

AAPL leads the group with a +47.4% one-year return. Its ROE of 151.9% is mathematically correct but requires context: Apple has reduced its book equity to approximately $62B through sustained share buybacks, so net income of $112B divided by that small equity base produces an extreme ratio. HD exhibits the same phenomenon at 110.5% ROE. In both cases, the elevated ROE reflects capital structure decisions (returning capital to shareholders) rather than superior operating efficiency. For cross-company comparisons, return on invested capital (ROIC) would provide a more meaningful profitability measure.

JPM at 15x PE and 15.7% ROE represents a conventional value profile — moderate valuation with solid but not extreme profitability. CRM is the worst performer at -35.6% despite a reasonable PE of 27.9, suggesting the market is pricing in deceleration in Salesforce's revenue growth rather than responding to current-period fundamentals.

The pipeline confirms that all 10 stocks were S&P 500 members as of January 2020, validating the analysis against historically accurate composition data.

## So what?

Multi-endpoint pipelines are the foundation of systematic investment research. Combining price, fundamental, and metric data into a single view enables comparisons that no single data type can support — for example, identifying stocks with strong returns but deteriorating fundamentals, or stocks with low valuations and improving profitability. The point-in-time index membership check is the critical first step: without it, any historical analysis is contaminated by survivorship bias, producing performance estimates that overstate what a real investor would have experienced.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
