# Do Stock Returns Follow a Normal Distribution? Testing for Fat Tails in Python

## What's the question?

The normal (Gaussian) distribution is the default assumption in most financial models -- portfolio theory, Value at Risk (VaR), options pricing, and risk management all rely on it. Under the normal distribution, a daily return more than 3 standard deviations from the mean (a "3-sigma event") should occur approximately 0.27% of the time, or about once every 371 trading days. But financial returns are known to exhibit leptokurtosis -- "fat tails" -- meaning extreme events occur far more frequently than the bell curve predicts. If returns are not normal, models that assume normality systematically underestimate the probability of extreme losses.

Kurtosis measures the weight in the tails of a distribution. A normal distribution has a kurtosis of 3.0 (or excess kurtosis of 0). Values above 3.0 indicate fat tails -- the higher the number, the more likely extreme moves are. The Jarque-Bera test formalizes this: it tests whether the skewness and kurtosis of a sample are consistent with normality.

## The approach

Analyze 7 tickers including SPY (the market itself) over 3 years of daily returns. For each, compute kurtosis (Pearson form), excess kurtosis (kurtosis minus 3.0), skewness, and the Jarque-Bera test statistic with its p-value. Then count the actual number of 3-sigma events for selected tickers and compare to the expected count under normality.

## Code

See [`fat-tails-kurtosis-python.py`](fat-tails-kurtosis-python.py)

## Output

```
=== Fat Tails in Financial Returns: Kurtosis Analysis (3Y) ===
Ticker   Kurtosis   Excess   Skewness   JB Stat     JB p   Normal?
--------------------------------------------------------------
AAPL        15.87   +12.87     +0.764    5264.5   0.0000        NO
MSFT         9.77    +6.77     -0.146    1439.2   0.0000        NO
NVDA        11.62    +8.62     +0.777    2403.7   0.0000        NO
TSLA         7.71    +4.71     +0.579     735.7   0.0000        NO
XOM          4.49    +1.49     -0.425      92.0   0.0000        NO
JNJ          9.42    +6.42     +0.023    1292.8   0.0000        NO
SPY         24.77   +21.77     +0.940   14960.4   0.0000        NO

Average excess kurtosis: +8.95 (normal = 0)
Stocks rejecting normality (JB test, p<0.05): 100%
Observations per stock: 752

=== 3-Sigma Events: Expected vs Actual (3Y) ===
  NVDA: 8 events (expected 2.0 under normality) = 3.9x more
  TSLA: 10 events (expected 2.0 under normality) = 4.9x more
  SPY: 8 events (expected 2.0 under normality) = 3.9x more
```

## What this tells us

Every stock and the broad market index reject normality decisively. Not a single p-value exceeds the 0.05 threshold. The Jarque-Bera statistics are enormous, with SPY producing the highest (14,960.4) -- driven by its excess kurtosis of +21.77, likely reflecting concentrated extreme-move days (such as tariff-related selloffs in early 2025). Excess kurtosis ranges from +1.49 (XOM) to +21.77 (SPY). Even XOM, the closest to normal, still has meaningfully fat tails. The 3-sigma event count makes this concrete: under a normal distribution, approximately 2 such events are expected in 752 trading days. TSLA experienced 10 -- nearly 5 times the expected frequency. SPY and NVDA both recorded 8 such events, approximately 4 times the normal expectation.

## So what?

Any risk model that assumes normality underestimates tail risk. Value at Risk (VaR) computed at the 99th percentile using a normal distribution will be breached more often than the stated 1% probability. Position sizing based on normal-distribution assumptions will result in larger losses during tail events than anticipated. Practitioners should consider using the Student-t distribution (which has a kurtosis parameter), historical simulation, or Cornish-Fisher expansion to account for fat tails when computing VaR or CVaR. At minimum, stress testing should include historical tail events -- not just normally-distributed scenarios.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
