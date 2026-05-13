# How to Rank Large-Cap Stocks by Momentum in Python

Momentum is the most documented factor anomaly. Ranking by trailing returns shows which stocks are running hot and which are lagging.

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

## Discussion

UNH leads at +39.4% over 3 months. The 57.7% spread between UNH (+39.4%) and HD (-18.3%) shows massive dispersion even among large caps.

XOM is interesting: strongest 6-month return (+26.6%) but negative over 3 months (-1.0%), meaning it peaked early and has been fading. MSFT shows the opposite pattern: -18.4% over 6 months but +11.3% in the last month -- a potential recovery signal.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
