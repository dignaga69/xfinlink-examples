# How to Build a Sector Correlation Matrix for Portfolio Diversification in Python

Diversification only works if your holdings don't move in lockstep. A sector correlation matrix shows which sectors hedge each other and which are redundant -- essential for portfolio construction.

## Code

See [`sector-correlation-matrix-python.py`](sector-correlation-matrix-python.py)

## Output

```
=== Sector Correlation Matrix (1Y Daily Returns) ===
             Energy  Financials  Industrials   Tech  ConsStaples  Utilities  Healthcare  ConsDisc
Energy        1.000       0.059        0.061 -0.049        0.100      0.093       0.023    -0.013
Financials    0.059       1.000        0.615  0.448        0.194      0.126       0.419     0.613
Industrials   0.061       0.615        1.000  0.572        0.285      0.347       0.473     0.632
Tech         -0.049       0.448        0.572  1.000       -0.152      0.061       0.164     0.624
ConsStaples   0.100       0.194        0.285 -0.152        1.000      0.410       0.426     0.198
Utilities     0.093       0.126        0.347  0.061        0.410      1.000       0.270     0.136
Healthcare    0.023       0.419        0.473  0.164        0.426      0.270       1.000     0.359
ConsDisc     -0.013       0.613        0.632  0.624        0.198      0.136       0.359     1.000

Most correlated pairs:
  Financials ↔ Industrials: 0.615
  Tech ↔ ConsDisc: 0.624
  Industrials ↔ ConsDisc: 0.632

Least correlated pairs (best diversifiers):
  Tech ↔ ConsStaples: -0.152
  Energy ↔ Tech: -0.049
  Energy ↔ ConsDisc: -0.013
```

## Discussion

Energy is the standout diversifier -- nearly zero correlation with every other sector (highest is 0.100 with Consumer Staples). This means adding energy to a tech-heavy portfolio provides genuine diversification, not just the illusion of it.

The Tech-Consumer Staples pair at -0.152 is the only negative correlation in the matrix, making them natural hedges. On the other end, Industrials-Consumer Discretionary at 0.632 move almost in lockstep -- owning both adds little diversification value.

The tight cluster of Financials-Industrials-ConsDisc (all above 0.61) confirms these are all "economic growth" bets that rise and fall together.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
