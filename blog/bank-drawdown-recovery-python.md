# How to Analyze Drawdown and Recovery for Bank Stocks in Python

Bank stocks are cyclical and sensitive to interest rate expectations. Drawdown analysis reveals which banks bounce back fastest and which stay underwater.

## Code

See [`bank-drawdown-recovery-python.py`](bank-drawdown-recovery-python.py)

## Output

```
=== Bank Stock Drawdown Analysis (1Y) ===
  WFC   WELLS FARGO & CO        max_dd=-23.7%  on 2026-05-11  recovery=not yet  now=-22.0%  1y= -1.1%
  GS    GOLDMAN SACHS GROUP IN  max_dd=-19.8%  on 2026-03-13  recovery=not yet  now=-3.1%  1y=+56.7%
  MS    MORGAN STANLEY          max_dd=-19.3%  on 2026-03-12  recovery=   34d  now=-0.8%  1y=+48.3%
  BAC   BANK OF AMERICA CORP    max_dd=-18.4%  on 2026-03-13  recovery=not yet  now=-11.3%  1y=+14.7%
  C     CITIGROUP INC           max_dd=-14.8%  on 2026-03-12  recovery=   28d  now=-5.0%  1y=+67.3%

Avg max drawdown: -19.2%
```

## Discussion

Citigroup had the shallowest drawdown (-14.8%) AND the best 1-year return (+67.3%), while recovering in just 28 days. WFC is the outlier -- its max drawdown hit just two days ago (-23.7%) and it's the only bank stock with a negative 1Y return (-1.1%). The March 2026 drawdown cluster (GS, MS, BAC, C all bottoming March 12-13) suggests a sector-wide shock, likely tied to rate expectations. The average bank drawdown of -19.2% is comparable to the broader market.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
