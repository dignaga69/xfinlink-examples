# Which Sectors Won Over 5 Years? Sector Rotation Analysis in Python

## What's the question?

Over short periods, sector performance is dominated by news and sentiment. Over 5 years, it reflects structural trends -- the rise of AI spending (technology), the post-COVID rate cycle (financials), the energy transition debate (energy). Comparing 5-year total returns across sectors reveals which structural bets paid off and which did not.

## The approach

Use 8 SPDR sector ETFs spanning 2021 through 2025. For each, compute the 5-year total return, annualized return, annualized volatility, and Sharpe ratio using a risk-free rate of 3% (reflecting the average over the period, which included both near-zero and elevated short-term rates).

## Code

See [`five-year-sector-rotation-python.py`](five-year-sector-rotation-python.py)

## Output

```
=== 5-Year Sector Total Return Ranking (2021-2025) ===
Sector         Ticker   5Y Total   Ann Ret   Ann Vol   Sharpe
------------------------------------------------------------
Financials        XLF    +88.3%   +13.5%    18.9%   +0.56
Industrials       XLI    +79.5%   +12.4%    17.2%   +0.55
Healthcare        XLV    +37.1%    +6.5%    14.5%   +0.24
Energy            XLE    +17.8%    +3.3%    34.7%   +0.01
ConsStaples       XLP    +16.4%    +3.1%    13.0%   +0.01
Technology        XLK    +12.6%    +2.4%    33.4%   -0.02
ConsDisc          XLY    -25.1%    -5.6%    32.9%   -0.26
Utilities         XLU    -30.2%    -6.9%    28.1%   -0.35

5-year sector spread: 118% (Financials vs Utilities)
```

## What this tells us

Financials and Industrials dominated the 5-year period -- both classic "old economy" sectors benefiting from the rising rate environment and infrastructure spending. Technology's modest +12.6% over 5 years appears counterintuitive given the AI narrative, but it reflects the 2022 growth stock crash that erased much of the 2021 gains. The subsequent recovery, while strong, was concentrated in a few names rather than the broad sector ETF. Energy's +17.8% with 34.7% volatility is the worst risk-adjusted return among positive sectors -- high volatility with low payoff. Consumer Discretionary and Utilities both posted negative 5-year returns, with Utilities suffering most from the rate-driven rotation out of yield proxies.

## So what?

Sector allocation has a larger impact on long-term returns than most investors assume. The 118-percentage-point spread between the best and worst sectors over 5 years exceeds most individual stock selection effects. For long-term allocation, monitor structural factors (interest rates, fiscal policy, technology adoption curves) rather than short-term momentum -- the sectors that led over 5 years are not the same ones leading over the most recent 1 year.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
