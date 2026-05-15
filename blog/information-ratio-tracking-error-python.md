# How Good Is a Stock Pick? Information Ratio and Tracking Error in Python

## What's the question?

Beating the benchmark is only meaningful if the outperformance is consistent. A stock that beats SPY by 20% one year but trails by 25% the next has high active return but also high tracking error -- the volatility of the difference between the stock's return and the benchmark's return. The information ratio (IR) divides active return by tracking error to measure the risk-adjusted quality of the outperformance. An IR above 0.5 indicates persistent alpha generation; below -0.5 indicates consistent underperformance.

## The approach

Treat 8 individual stocks as single-stock "portfolios" measured against SPY over 1 year. For each stock, compute the total return, the active return (total return minus SPY's return), the tracking error (annualized standard deviation of daily active returns), and the information ratio (active return divided by tracking error). Also compute the hit rate -- the percentage of trading days on which the stock outperformed SPY.

## Code

See [`information-ratio-tracking-error-python.py`](information-ratio-tracking-error-python.py)

## Output

```
=== Information Ratio vs SPY (1Y) ===
Benchmark (SPY) annualized return: 28.4%

Ticker   Return   Active      TE      IR   Hit%
--------------------------------------------
NVDA    +84.6%  +36.4%  27.5%  +1.32    54%
JNJ     +60.1%  +22.1%  20.0%  +1.11    48%
AAPL    +44.2%  +11.6%  19.2%  +0.61    48%
XOM     +45.0%  +12.2%  27.8%  +0.44    53%
AMZN    +32.9%   +3.5%  24.7%  +0.14    51%
JPM     +15.5%  -10.6%  17.5%  -0.61    53%
META     -0.4%  -25.4%  30.5%  -0.83    46%
MSFT     -7.1%  -32.3%  21.2%  -1.53    46%

IR interpretation:
  > +0.5: strong outperformance | -0.5 to +0.5: noise | < -0.5: consistent underperformance
```

## What this tells us

NVDA and JNJ have the strongest IRs (+1.32 and +1.11) -- both delivered substantial active returns relative to their tracking error. JNJ is the more remarkable case: it achieved an IR of 1.11 with only 20% tracking error, meaning it consistently outperformed with moderate deviation from SPY. NVDA's higher active return (+36.4%) came with proportionally higher tracking error (27.5%). The hit rate column adds nuance: JNJ beat SPY on only 48% of trading days despite having the second-highest IR. This shows that information ratio is about the size of wins relative to losses, not the frequency.

## So what?

When evaluating whether a stock pick or fund is genuinely skilled vs lucky, the information ratio is more informative than raw return. An IR above 0.5 sustained over 2-3 years is the threshold most institutional allocators consider evidence of skill. For portfolio construction, prefer holdings with high IR and moderate tracking error over those with extreme returns but proportionally extreme deviation from the benchmark.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
