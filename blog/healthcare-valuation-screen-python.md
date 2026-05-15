# How to Screen Healthcare Stocks by Valuation in Python

## What's the question?

Which healthcare sub-segments are trading at a premium and which offer relative value? Healthcare is not a single industry — it spans pharmaceuticals, biotechnology, medical devices, managed care organizations (MCOs), and life science tools, each with different growth profiles, margin structures, and valuation conventions. A PE ratio that signals "cheap" in pharma may be normal in med-tech and expensive in managed care. Screening by multiple valuation metrics across the sector reveals where the market is allocating premium multiples and where it sees risk.

## The approach

We retrieve the most recent annual metrics for 10 large-cap healthcare companies and compare them on four dimensions. Price-to-earnings ratio (PE) measures how much investors pay per dollar of earnings. Price-to-sales ratio (P/S) captures how the market values each dollar of revenue, which is particularly useful for comparing companies with different margin profiles. Dividend yield provides a measure of cash return to shareholders. Return on equity (ROE) measures profitability relative to book equity, though it can be distorted by buybacks and acquisition accounting that reduce or invert book equity.

The combination of these four metrics across companies with distinct business models highlights how valuation norms vary by sub-segment within healthcare.

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

## What this tells us

MRK and BMY are the cheapest names in the group at 15-16x PE, with strong ROE (35-38%) and meaningful dividend yields. These are the classic big pharma value profiles — mature franchises generating substantial cash flow with limited growth expectations priced in. PFE offers the highest yield in the group at 6.7%, but at the cost of low ROE (9.0%), reflecting its post-COVID revenue decline and the market's skepticism about its pipeline replacement cycle.

LLY commands the highest premium at 42x PE and 14x P/S, justified by its GLP-1 obesity drug franchise, which the market views as a multi-decade growth opportunity. The nearly 3x premium over MRK on a PE basis quantifies exactly how much the market is paying for LLY's growth pipeline versus MRK's mature portfolio.

AMGN's ROE of 89.1% is inflated by the same buyback-driven equity reduction seen in companies like AAPL — it reflects capital structure rather than exceptional operating performance.

UNH is notable for its P/S ratio of 0.8x, the lowest in the group by a wide margin. This is characteristic of managed care organizations: health insurers process enormous revenue (UNH's annual revenue exceeds $448B) but retain thin margins after medical claims are paid. P/S is structurally misleading for MCOs and should not be compared directly to pharmaceutical P/S ratios.

ABBV's extreme PE of 85.9x and negative ROE of -129.2% are both artifacts of the Allergan acquisition, which created negative book equity through acquisition accounting adjustments.

## So what?

Healthcare valuation analysis requires sub-segment context. Comparing a pharma company's PE to a managed care company's PE without adjusting for structural differences in growth, margin, and capital intensity produces misleading conclusions. This screen provides the raw data for such comparisons while flagging the accounting artifacts (negative equity from acquisitions, buyback-inflated ROE) that distort standard metrics. Investors evaluating healthcare exposure should select the valuation metric most appropriate for each sub-segment rather than applying a single metric uniformly across the sector.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
