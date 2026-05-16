# How to Estimate Cost of Equity Using CAPM in Python

## What's the question?

The cost of equity is the return that shareholders require as compensation for bearing the risk of owning a stock. It is a critical input to discounted cash flow (DCF) models, capital budgeting decisions, and weighted average cost of capital (WACC) calculations. The Capital Asset Pricing Model (CAPM) provides a formula: Cost of Equity = Risk-Free Rate + Beta x Equity Risk Premium. The risk-free rate (Rf) represents the return on a riskless asset -- typically the 10-year Treasury yield. Beta measures the stock's sensitivity to market movements. The equity risk premium (ERP) is the additional return investors demand for holding equities instead of risk-free bonds. The current 10-year Treasury yield is approximately 4.3%, and the long-run ERP is conventionally estimated at 5.0-6.0%.

## The approach

Select 10 stocks across risk profiles -- from high-beta technology names to low-beta consumer staples. Estimate beta via ordinary least squares (OLS) regression of each stock's daily returns against SPY over 3 years. Report the standard error of the beta estimate and R-squared to quantify estimation precision. Apply the CAPM formula with Rf = 4.3% and ERP = 5.5% to compute the implied cost of equity for each stock.

## Code

See [`capm-cost-of-equity-python.py`](capm-cost-of-equity-python.py)

## Output

```
=== CAPM Cost of Equity Estimation ===
Risk-free rate (Rf): 4.3%  |  Equity risk premium (ERP): 5.5%
Formula: Ke = Rf + Beta x ERP = 4.3% + Beta x 5.5%

Ticker    Beta   Beta SE      R²   Cost of Equity
----------------------------------------------
TSLA      2.22     0.113   0.339           16.5%
NVDA      2.08     0.090   0.416           15.8%
AMZN      1.40     0.054   0.468           12.0%
AAPL      1.13     0.046   0.439           10.5%
MSFT      0.98     0.044   0.399            9.7%
JPM       0.90     0.044   0.363            9.3%
XOM       0.29     0.054   0.037            5.9%
UNH       0.28     0.088   0.013            5.8%
PG        0.15     0.041   0.018            5.1%
JNJ       0.05     0.041   0.002            4.6%

Median cost of equity: 9.5%
Range: 4.6% to 16.5%
```

## What this tells us

The CAPM produces a 12-percentage-point spread in cost of equity, from 4.6% (JNJ) to 16.5% (TSLA). This spread directly impacts valuation: a DCF model using 16.5% discounts TSLA's future cash flows far more aggressively than one using 4.6% for JNJ. The standard errors are informative -- JNJ's beta standard error (0.041) is nearly as large as its point estimate (0.05), indicating the beta is not reliably distinguishable from zero. Its R-squared of 0.002 confirms JNJ's returns are almost entirely idiosyncratic -- the market explains essentially none of its variation. For such stocks, the CAPM framework provides limited predictive value because the market risk factor is irrelevant.

## So what?

When building a DCF model, the cost of equity is the most consequential assumption after the growth rate. Using a single "market average" discount rate for all stocks introduces systematic bias -- overvaluing high-beta stocks and undervaluing low-beta ones. Estimate beta from at least 3 years of data, report the standard error, and use the Merrill Lynch adjusted beta (shrunk toward 1.0) for stocks with low R-squared to reduce estimation noise. For defensive stocks like JNJ and PG where market beta is near zero, consider supplementing CAPM with a build-up method that adds company-specific risk premiums.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
