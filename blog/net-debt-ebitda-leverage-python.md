# Which Industrials Are Overleveraged? Net Debt to EBITDA Screening in Python

## What's the question?

Debt-to-equity ratios are the most common leverage metric, but they can be misleading because equity book values vary widely due to accounting choices such as buybacks, goodwill impairment, and revaluation reserves. Net debt to EBITDA -- total debt minus cash, divided by earnings before interest, taxes, depreciation, and amortization -- measures how many years of operating earnings it would take to repay all outstanding debt. It is the leverage metric preferred by credit analysts and debt covenants. A ratio below 2.0x is generally considered conservative. Between 2.0x and 4.0x is moderate. Above 4.0x indicates high leverage requiring strong and stable cash flows to service.

## The approach

Select 7 industrial and energy companies. Pull total_debt, cash_and_equivalents, and ebitda from fundamentals to compute net debt and the net debt to EBITDA ratio. Combine with metrics for debt-to-equity, interest coverage (EBIT divided by interest expense), and EV/EBITDA (enterprise value divided by EBITDA) to build a comprehensive leverage profile for each company.

## Code

See [`net-debt-ebitda-leverage-python.py`](net-debt-ebitda-leverage-python.py)

## Output

```
=== Net Debt / EBITDA: Leverage Screen (Industrials + Energy) ===
Ticker                    Company   ND/EBITDA     D/E   Int Cov   EV/EBITDA
------------------------------------------------------------------------
XOM              EXXON MOBIL CORP        0.4x    0.14     69.4x       10.0x
DE                     DEERE & CO        0.5x    0.53      3.0x       13.5x
LMT          LOCKHEED MARTIN CORP        1.9x    3.24      6.9x       14.4x
CAT               CATERPILLAR INC        2.0x    1.70       N/A       32.8x
RTX                    R T X CORP        2.0x    0.53     -5.3x       18.8x
HON     HONEYWELL INTERNATIONAL I        2.4x    2.51      6.0x       16.6x
BA                      BOEING CO        8.2x   11.42      1.5x       44.0x
```

## What this tells us

XOM and DE are the least leveraged at 0.4-0.5x -- capable of repaying all net debt from less than one year of operating earnings. Boeing is the clear outlier at 8.2x, meaning it would take over 8 years of current EBITDA to service its net debt. BA also has the weakest interest coverage (1.5x) and the highest debt-to-equity (11.42), confirming its balance sheet is under significant strain. RTX's negative interest coverage (-5.3x) indicates that interest expense exceeded operating income for the period -- an accounting anomaly likely driven by restructuring charges.

## So what?

For credit analysis or distressed investing, net debt to EBITDA is more informative than debt-to-equity because it accounts for cash reserves and uses operating earnings rather than book equity. Covenants in leveraged loan agreements typically trigger at 4.0-5.0x net debt to EBITDA. BA at 8.2x would breach most standard covenants, which explains why its debt is priced at a premium to investment-grade peers.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
