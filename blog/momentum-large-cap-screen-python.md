# How to Rank Large-Cap Stocks by Momentum in Python

## What's the question?

Which large-cap stocks have the strongest recent price trends, and are those trends accelerating or fading? Momentum — the tendency of stocks that have performed well recently to continue performing well, and vice versa — is the most extensively documented factor anomaly in academic finance. Jegadeesh and Titman's 1993 paper demonstrated that buying recent winners and selling recent losers produces excess returns over 3-to-12-month horizons. Ranking large caps by trailing returns across multiple time frames reveals not only which stocks are running hot but also whether the underlying trend is strengthening or deteriorating.

## The approach

We compute total returns over three overlapping time horizons — 6 months, 3 months, and 1 month — for 15 large-cap stocks across technology, healthcare, financials, energy, and consumer sectors. Comparing returns across these windows reveals momentum structure. A stock with strong 6-month and 3-month returns but a weak 1-month return may be losing momentum. Conversely, a stock with weak 6-month returns but a strong 1-month return may be at the beginning of a recovery. The 3-month return serves as the primary ranking criterion, representing the intermediate-term trend most commonly used in momentum strategies.

## Code

See [`momentum-large-cap-screen-python.py`](momentum-large-cap-screen-python.py)

## Output

```
=== 3-Month Momentum Ranking (15 Large Caps) ===
  UNH    $  384.44  6mo=+19.6%  3mo=+39.4%  1mo=+26.3%
  AMZN   $  268.99  6mo= +8.3%  3mo=+28.9%  1mo=+12.8%
  AVGO   $  428.43  6mo=+19.5%  3mo=+24.6%  1mo=+15.3%
  NVDA   $  219.44  6mo=+10.2%  3mo=+15.5%  1mo=+16.3%
  AAPL   $  292.68  6mo= +8.6%  3mo= +6.6%  1mo=+12.4%
  COST   $  999.47  6mo= +9.2%  3mo= +0.2%  1mo= +0.1%
  MSFT   $  412.66  6mo=-18.4%  3mo= -0.2%  1mo=+11.3%
  V      $  323.86  6mo= -3.3%  3mo= -0.5%  1mo= +6.4%
  XOM    $  149.68  6mo=+26.6%  3mo= -1.0%  1mo= -1.9%
  JPM    $  300.00  6mo= -5.3%  3mo= -6.9%  1mo= -3.2%
  LLY    $  966.99  6mo= +0.0%  3mo= -7.4%  1mo= +2.9%
  CRM    $  177.49  6mo=-26.6%  3mo= -8.5%  1mo= +7.6%
  PG     $  143.36  6mo= -1.5%  3mo= -8.9%  1mo= -1.2%
  META   $  598.86  6mo= -5.2%  3mo=-11.6%  1mo= -4.9%
  HD     $  311.40  6mo=-15.9%  3mo=-18.3%  1mo= -7.7%
```

## What this tells us

UNH leads with +39.4% over 3 months, producing a 57.7 percentage point spread between the best and worst performers (UNH at +39.4% versus HD at -18.3%). This degree of dispersion within a universe of exclusively large-cap names is substantial and indicates that momentum signals are generating meaningful differentiation even among the most liquid, widely followed stocks.

XOM presents an instructive divergence across time frames: it has the strongest 6-month return (+26.6%) but a negative 3-month return (-1.0%) and a negative 1-month return (-1.9%). This pattern — strong long-term momentum with fading short-term performance — indicates a trend that has peaked and is now decelerating. MSFT shows the opposite pattern: -18.4% over 6 months but +11.3% in the most recent month, consistent with a potential trend reversal and early-stage recovery.

CRM exhibits a similar reversal signature with its 1-month return (+7.6%) sharply contrasting its 6-month return (-26.6%), suggesting that selling pressure may be exhausting.

## So what?

Momentum rankings are diagnostic, not prescriptive. The academic literature shows that momentum strategies generate excess returns on average but are subject to occasional sharp reversals (momentum crashes). The multi-timeframe view presented here adds information beyond a single-horizon ranking by revealing trend structure — whether momentum is accelerating, stable, or fading. Portfolio managers use this information to time position entry and exit, while risk managers use it to identify crowded trades where multiple momentum signals converge on the same names.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
