# How to Calculate CAPM Alpha and Beta with Regression in Python

The Capital Asset Pricing Model predicts a stock's return based on its market sensitivity (beta). Alpha is the excess return unexplained by market exposure — positive alpha means the stock outperformed what CAPM predicted, negative means it lagged. Here's how to run the regression and interpret the results.

## Code

See [`capm-alpha-beta-regression-python.py`](capm-alpha-beta-regression-python.py)

## Output

```
=== CAPM Regression: Alpha, Beta, R² (1Y vs SPY, Rf=5%) ===

Ticker    Beta   Alpha (ann)      R²   Ann Return        Interpretation
----------------------------------------------------------------------
JNJ       0.06       +39.4%   0.002      +55.5%            OUTPERFORM
XOM      -0.25       +35.3%   0.017      +38.7%            OUTPERFORM
NVDA      1.75       +22.3%   0.397      +74.2%            OUTPERFORM
AAPL      0.98       +12.5%   0.278      +40.6%            OUTPERFORM
AMZN      1.43        -3.7%   0.341      +27.9%                  FAIR
JPM       0.99        -8.6%   0.318      +14.2%          UNDERPERFORM
MSFT      0.87       -29.3%   0.198       -9.8%          UNDERPERFORM
META      1.47       -33.7%   0.261       -6.0%          UNDERPERFORM
```

## Discussion

JNJ is the alpha king at +39.4% — it returned +55.5% with virtually zero market exposure (beta=0.06, R²=0.002). Its returns are almost entirely idiosyncratic, meaning JNJ moved for company-specific reasons independent of the market. XOM's negative beta (-0.25) is notable: energy moved inversely to the broader market this year, yet still delivered +38.7%. NVDA's alpha (+22.3%) is genuine outperformance above what its high beta (1.75) would predict. META and MSFT show large negative alpha — they lagged significantly even after accounting for their market sensitivity.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
