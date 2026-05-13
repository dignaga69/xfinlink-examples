# How Correlated Are the Magnificent 7? Intra-Group Correlation in Python

The "Magnificent 7" are often treated as one trade. But if they move independently, concentrating in all of them is diversification. If they move together, it's just leverage. Here's the correlation matrix.

## Code

See [`mag7-correlation-python.py`](mag7-correlation-python.py)

## Output

```
=== Magnificent 7 Intra-Group Correlation (1Y) ===
(Which of these mega-caps move independently?)

ticker   AAPL   AMZN   META   MSFT   NVDA   TSLA
ticker
AAPL    1.000  0.285  0.195  0.128  0.236  0.286
AMZN    0.285  1.000  0.443  0.320  0.319  0.278
META    0.195  0.443  1.000  0.349  0.393  0.248
MSFT    0.128  0.320  0.349  1.000  0.393  0.253
NVDA    0.236  0.319  0.393  0.393  1.000  0.378
TSLA    0.286  0.278  0.248  0.253  0.378  1.000

Lowest correlation (most independent):
  AAPL / MSFT: 0.128
  AAPL / META: 0.195
  AAPL / NVDA: 0.236

Highest correlation (most redundant):
  META / NVDA: 0.393
  MSFT / NVDA: 0.393
  AMZN / META: 0.443
```

## Discussion

The surprise: AAPL and MSFT have the lowest correlation (0.128) -- the two largest companies in the world barely move together on a daily basis. This means owning both is genuine diversification within mega-cap tech. On the other end, AMZN and META at 0.443 are the most correlated pair, likely because both are advertising/e-commerce businesses sensitive to the same consumer spending signals. Overall, the max correlation in the group is only 0.44 -- far below the 0.6-0.7 threshold where diversification breaks down. The Magnificent 7 aren't one trade.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
