# How to Screen Healthcare Stocks by Valuation in Python

Healthcare spans pharma, biotech, devices, and insurance -- each with different valuation norms. Screening by PE, P/S, and dividend yield across the sector reveals which sub-segments are cheap and which the market is paying up for.

## Code

See [`healthcare-valuation-screen-python.py`](healthcare-valuation-screen-python.py)

## Output

```
=== Healthcare Sector Valuation Screen ===
  MRK    MERCK & CO INC          PE=  15.3  P/S=  4.2  yield= 2.9%  ROE= 34.7%
  BMY    BRISTOL MYERS SQUIBB C  PE=  16.1  P/S=  2.4  yield= 4.5%  ROE= 38.2%
  PFE    PFIZER INC              PE=  19.0  P/S=  2.4  yield= 6.7%  ROE=  9.0%
  JNJ    JOHNSON & JOHNSON       PE=  20.1  P/S=  5.7  yield= 2.3%  ROE= 32.9%
  ABT    ABBOTT LABORATORIES     PE=  22.2  P/S=  3.2  yield= 2.9%  ROE= 12.5%
  AMGN   AMGEN INC               PE=  23.2  P/S=  4.8  yield= 2.9%  ROE= 89.1%
  TMO    THERMO FISHER SCIENTIF  PE=  25.5  P/S=  3.8  yield= 0.4%  ROE= 12.6%
  UNH    UNITEDHEALTH GROUP INC  PE=  29.1  P/S=  0.8  yield= 2.3%  ROE= 12.0%
  LLY    LILLY ELI & CO          PE=  42.1  P/S= 14.0  yield= 0.6%  ROE= 77.8%
  ABBV   ABBVIE INC              PE=  85.9  P/S=  5.9  yield= 3.3%  ROE=-129.2%

Note: ABBV has negative ROE (-129.2%) — likely negative equity from acquisitions
```

## Discussion

MRK and BMY are the cheapest at 15-16x PE with strong ROE (35-38%) and meaningful dividend yields -- classic big pharma value. PFE offers the highest yield at 6.7% but at the cost of low ROE (9%), reflecting its post-COVID revenue decline.

LLY at 42x PE and 14x P/S is the premium growth name, justified by its GLP-1 obesity drug pipeline. AMGN's ROE of 89% is inflated by buyback-driven low equity (same artifact as AAPL).

UNH is notable for having the lowest P/S (0.8x) in the group -- health insurers process enormous revenue but keep thin margins, making P/S misleading for MCOs.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
