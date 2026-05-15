# What Is Adjusted Beta? Merrill Lynch Beta Shrinkage in Python

## What's the question?

Raw beta from OLS regression measures a stock's historical market sensitivity. But raw betas are noisy -- they fluctuate substantially depending on the estimation period. The Merrill Lynch adjusted beta (also called Bloomberg beta) addresses this by shrinking the raw estimate toward 1.0 using the formula: Adjusted Beta = (2/3) x Raw Beta + (1/3) x 1.0. The rationale: betas tend to mean-revert toward 1.0 over time (high-beta stocks get less volatile, low-beta stocks become more correlated with the market). The 2/3 weight is empirically calibrated.

## The approach

Select 10 stocks across risk profiles -- from high-volatility names (TSLA, NVDA) to defensive consumer staples (PG, JNJ). Run OLS regression of each stock's daily returns against SPY over 1 year to obtain the raw beta, then apply the Merrill Lynch shrinkage formula. Compare both estimates side by side with the R-squared from each regression.

## Code

See [`merrill-lynch-adjusted-beta-python.py`](merrill-lynch-adjusted-beta-python.py)

## Output

```
=== Raw Beta vs Merrill Lynch Adjusted Beta (1Y vs SPY) ===
Ticker   Raw Beta   Adj Beta   Shrinkage      R²
----------------------------------------------
TSLA        2.041      1.694      +0.347   0.280
NVDA        1.803      1.535      +0.268   0.429
GS          1.471      1.314      +0.157   0.444
AAPL        0.984      0.989      -0.005   0.277
JPM         0.982      0.988      -0.006   0.315
MSFT        0.901      0.934      -0.033   0.218
UNH         0.706      0.804      -0.098   0.039
PG          0.097      0.398      -0.301   0.004
JNJ         0.054      0.369      -0.315   0.002
XOM        -0.246      0.169      -0.415   0.016

Adjustment formula: Adj Beta = (2/3) * Raw Beta + (1/3) * 1.0
Average raw beta:  0.879
Average adj beta:  0.919
```

## What this tells us

The adjustment has asymmetric effects depending on which side of 1.0 the raw beta sits. High-beta stocks get pulled down: TSLA shrinks from 2.04 to 1.69. Low-beta stocks get pulled up: XOM's negative beta (-0.25) becomes a modest positive (0.17). Near-1.0 betas barely change: AAPL moves from 0.984 to 0.989. The R-squared column reveals another dimension: JNJ and PG have near-zero R-squared values (0.002 and 0.004), meaning their raw betas are estimated from essentially no signal. The adjustment pushes these unreliable estimates toward 1.0, which is a safer prior than trusting a noisy regression. The Bayesian interpretation: the formula treats 1.0 as a prior and updates it with the data, with the 2/3 weight reflecting how much to trust the observed beta.

## So what?

When constructing portfolios or hedging, use adjusted beta instead of raw beta. Raw beta overestimates the market sensitivity of volatile stocks and underestimates it for defensive stocks. For risk models that compute expected returns via CAPM (Expected Return = Rf + Beta x Market Premium), using raw betas produces forecasts that are too extreme in both directions. The Merrill Lynch adjustment is a one-line correction that improves out-of-sample prediction.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
