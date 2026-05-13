# How to Build a Multi-Endpoint Financial Dashboard in Python

Real analysis needs multiple data sources. Here's a pipeline combining index composition, prices, fundamentals, and metrics into one dashboard.

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

## Discussion

AAPL leads with +47.4% one-year return. Note AAPL ROE of 152% and HD ROE of 111% -- both are real but inflated by negative/tiny book equity from aggressive buybacks, not operating performance.

JPM at 15x PE and 15.7% ROE is the classic value play. CRM is the worst performer at -35.6% despite reasonable PE (27.9), suggesting the market is pricing in growth deceleration.

The pipeline demonstrates how point-in-time index data prevents survivorship bias.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
