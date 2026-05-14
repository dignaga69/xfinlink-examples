# Are Stock Prices Mean-Reverting? Augmented Dickey-Fuller Test in Python

Mean reversion strategies assume prices return to a moving average. But do stock prices actually mean-revert? The Augmented Dickey-Fuller test answers this statistically — testing whether a time series has a unit root (random walk) or is stationary (mean-reverting). Spoiler: raw prices almost never pass.

## Code

See [`adf-mean-reversion-test-python.py`](adf-mean-reversion-test-python.py)

## Output

```
=== Augmented Dickey-Fuller Test: Are Stock Prices Mean-Reverting? ===
(H0: unit root exists = non-stationary = trending/random walk)
(If p < 0.05: reject H0 → stationary → mean-reverting)

Ticker   Price ADF   Price p        Result  |  Return ADF  Return p        Result
-------------------------------------------------------------------------------------
AAPL        -0.557    0.8803     UNIT ROOT  |     -14.469    0.0000    STATIONARY
MSFT        -0.753    0.8325     UNIT ROOT  |     -15.126    0.0000    STATIONARY
XOM         -0.491    0.8937     UNIT ROOT  |     -12.008    0.0000    STATIONARY
JNJ         -1.327    0.6168     UNIT ROOT  |     -15.172    0.0000    STATIONARY
NVDA        -1.424    0.5708     UNIT ROOT  |      -9.588    0.0000    STATIONARY
PG          -1.694    0.4340     UNIT ROOT  |     -15.093    0.0000    STATIONARY

Prices stationary:  0/6 (expect 0 — prices follow random walks)
Returns stationary: 6/6 (expect all — returns are i.i.d.)
```

## Discussion

Every stock's price series has a unit root (p > 0.43 for all), meaning prices follow random walks — they don't mean-revert. But daily returns are all strongly stationary (p = 0.0000), which is the mathematical prerequisite for most factor models and portfolio optimization. This is why mean reversion strategies don't work on raw prices but can work on spreads, ratios, or z-scores relative to a moving average — those derived series can be stationary even when the underlying prices aren't.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
