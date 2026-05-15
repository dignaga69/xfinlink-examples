# Which Large Caps Have the Highest Free Cash Flow Yield? FCF Screening in Python

## What's the question?

Earnings can be manipulated through accruals and accounting choices. Free cash flow (FCF) -- the cash a company generates after capital expenditures -- is harder to inflate. FCF yield (FCF per share divided by share price) measures how much real cash generation an investor receives per dollar invested. A high FCF yield combined with a reasonable P/E ratio suggests genuine value; a low FCF yield despite low P/E may indicate aggressive accounting or high capital requirements.

## The approach

Select 10 large-cap stocks across sectors. Pull FCF per share from the metrics endpoint, current price from the prices endpoint, and compute FCF yield. Compare to earnings yield (the inverse of P/E) to identify discrepancies between accounting earnings and actual cash generation. JPM is excluded because banks lack traditional free cash flow due to the nature of financial intermediation.

## Code

See [`fcf-yield-ranking-python.py`](fcf-yield-ranking-python.py)

## Output

```
=== Free Cash Flow Yield Ranking (Latest Annual) ===
Ticker   FCF/Share     Price   FCF Yield      PE   E Yield
-------------------------------------------------------
ABBV         10.08    210.77        4.8%    89.3      1.1%
UNH          17.70    399.09        4.4%    30.2      3.3%
MRK           5.00    113.41        4.4%    15.6      6.5%
PG            6.00    142.71        4.2%    21.9      4.8%
HD           12.70    304.35        4.2%    21.4      4.7%
XOM           5.70    152.78        3.7%    22.8      4.6%
MSFT          9.64    409.43        2.4%    30.0      3.3%
AAPL          6.72    298.21        2.3%    40.0      2.6%
CAT          19.17    920.22        2.1%    48.9      2.1%
```

## What this tells us

ABBV leads at 4.8% FCF yield despite having the highest P/E (89.3x). This divergence -- high FCF yield with high P/E -- occurs because ABBV's GAAP earnings are depressed by Allergan acquisition amortization, but its cash generation is strong. Conversely, MRK has the lowest P/E (15.6x) and the highest earnings yield (6.5%) but only a moderate FCF yield (4.4%), meaning its cash conversion is not as efficient as earnings alone suggest. AAPL and MSFT cluster around 2.3-2.4% FCF yield, placing them at the expensive end of the spectrum for cash generation, though both have fortress balance sheets that may justify a premium.

## So what?

Screen by FCF yield rather than P/E to avoid value traps. A stock that looks cheap on P/E but has low FCF yield may be capitalizing expenses, using aggressive revenue recognition, or requiring heavy ongoing capital expenditure. For income-oriented investors, FCF yield is a better predictor of sustainable dividends than earnings yield -- a company cannot distribute cash it does not generate.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
