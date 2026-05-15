# How to Calculate CAPM Alpha and Beta with Regression in Python

## What's the question?

The Capital Asset Pricing Model (CAPM) predicts that a stock's expected return is a linear function of its sensitivity to the overall market. Beta measures that sensitivity: a beta of 1.5 means the stock is expected to move 1.5% for every 1% move in the market. Alpha is the residual -- the portion of a stock's return that CAPM cannot explain through market exposure alone. Positive alpha means the stock outperformed what its market sensitivity would predict; negative alpha means it lagged. The question is: for a set of major U.S. stocks, how much of their return is explained by market exposure (beta), and how much is genuine idiosyncratic outperformance or underperformance (alpha)?

## The approach

CAPM is estimated via ordinary least squares (OLS) regression. For each stock, daily excess returns (stock return minus the risk-free rate) are regressed against the market's daily excess returns (SPY return minus the risk-free rate). The slope of the regression line is beta, the intercept is daily alpha (annualized by multiplying by 252 trading days), and R-squared measures the fraction of the stock's return variance explained by market movements. A 5% annualized risk-free rate is assumed, consistent with prevailing Treasury yields.

Eight stocks spanning multiple sectors are tested: AAPL, MSFT, NVDA, AMZN, META, XOM, JNJ, and JPM. The interpretation threshold is set at +/-5% annualized alpha: above +5% is classified as OUTPERFORM, below -5% as UNDERPERFORM, and within the range as FAIR.

## Code

```python
import numpy as np
from scipy import stats
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "XOM", "JNJ", "JPM"]
benchmark = "SPY"
rf_annual = 0.05
rf_daily = rf_annual / 252

all_tickers = tickers + [benchmark]
prices = xfl.prices(all_tickers, period="1y", fields=["return_daily"])

pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot.dropna()

spy_excess = pivot[benchmark] - rf_daily

print(f"=== CAPM Regression: Alpha, Beta, R² (1Y vs SPY, Rf={int(rf_annual*100)}%) ===")
print()
header = f"{'Ticker':<10}{'Beta':>6}   {'Alpha (ann)':>11}   {'R²':>5}   {'Ann Return':>10}        {'Interpretation'}"
print(header)
print("-" * len(header))

results = []

for ticker in tickers:
    stock_excess = pivot[ticker] - rf_daily

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        spy_excess.values, stock_excess.values
    )

    beta = slope
    alpha_daily = intercept
    alpha_annual = alpha_daily * 252
    r_squared = r_value ** 2

    total_return = (1 + pivot[ticker]).prod() - 1
    ann_return = total_return

    if alpha_annual > 0.05:
        interp = "OUTPERFORM"
    elif alpha_annual < -0.05:
        interp = "UNDERPERFORM"
    else:
        interp = "FAIR"

    results.append((ticker, beta, alpha_annual, r_squared, ann_return, interp))

results.sort(key=lambda x: x[2], reverse=True)

for ticker, beta, alpha_annual, r_squared, ann_return, interp in results:
    print(
        f"{ticker:<10}"
        f"{beta:6.2f}   "
        f"{alpha_annual:+10.1%}   "
        f"{r_squared:5.3f}   "
        f"{ann_return:+10.1%}   "
        f"{'':>8}{interp}"
    )
```

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

## What this tells us

JNJ is the most striking result in this analysis. It delivered +55.5% with a beta of 0.06 and an R-squared of 0.002 -- meaning virtually none of its return is explained by market movements. Its +39.4% alpha is almost entirely idiosyncratic, driven by company-specific factors (product approvals, litigation outcomes, spin-off activity) rather than broad market direction. For practical purposes, JNJ behaved as a market-neutral stock this year.

XOM's negative beta (-0.25) indicates that energy moved inversely to the broader market during this period. Despite this contrarian behavior, XOM still delivered +38.7% in absolute returns, producing +35.3% in alpha. A negative-beta stock with positive alpha is the theoretical ideal for portfolio diversification: it contributes returns while hedging market drawdowns.

Nvidia's alpha of +22.3% is notable because it exists on top of already-high market exposure (beta of 1.75). NVDA returned +74.2% for the year; CAPM attributes approximately 52 percentage points of that to its amplified market sensitivity, leaving 22.3% as genuine outperformance. Its R-squared of 0.397 is the highest in the group, confirming that market exposure is a meaningful driver of NVDA returns -- but not the only one.

META and MSFT show large negative alphas (-33.7% and -29.3%), indicating significant underperformance relative to what their market betas would predict. META's beta of 1.47 implies it should have captured amplified market gains, yet it returned -6.0% -- a substantial shortfall that reflects company-specific headwinds.

The low R-squared values across the board (ranging from 0.002 to 0.397) indicate that the single-factor CAPM explains a minority of these stocks' return variance. Multi-factor models (Fama-French three-factor, Carhart four-factor) would likely explain more of the variance by incorporating size, value, and momentum factors.

## So what?

Alpha and beta decomposition separates skill (or luck) from market exposure. A portfolio manager who delivered +74% by holding NVDA at 1.75x beta took substantially more market risk than one who delivered +55% with JNJ at 0.06x beta. The alpha metric makes this comparison explicit. When evaluating stock performance or portfolio manager returns, always decompose the total return into its beta-driven and alpha-driven components -- raw returns alone conflate market participation with genuine outperformance.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
