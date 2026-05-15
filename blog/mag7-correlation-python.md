# How Correlated Are the Magnificent 7? Intra-Group Correlation in Python

## What's the question?

The "Magnificent 7" -- Apple, Amazon, Meta, Microsoft, Nvidia, Tesla, and Alphabet -- are frequently treated as a single trade by market commentators and passive index investors. This framing implies that these stocks move together and that concentrating in all of them is equivalent to a single leveraged bet on large-cap technology. But if the individual stocks within the group move independently of each other, then holding multiple Mag 7 names actually provides diversification. The question is empirical: what is the pairwise correlation structure within this group, and does it support the "one trade" narrative?

## The approach

Six of the seven Magnificent 7 stocks are used to build a clean correlation matrix (GOOGL is excluded to keep the matrix to a readable 6x6 format). One year of daily returns is fetched for each, pivoted into wide format, and the Pearson correlation coefficient is computed for all 15 unique pairs. The three highest and three lowest correlations are extracted to identify which pairs are most redundant and which provide the most independence.

## Code

```python
import itertools
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["AAPL", "AMZN", "META", "MSFT", "NVDA", "TSLA"]

prices = xfl.prices(tickers, period="1y", fields=["return_daily"])

pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot[tickers]

corr = pivot.corr()

print("=== Magnificent 7 Intra-Group Correlation (1Y) ===")
print("(Which of these mega-caps move independently?)")
print()

header = f"{'ticker':<8}" + "  ".join(f"{t:>6}" for t in tickers)
print(header)

for row in tickers:
    values = "  ".join(f"{corr.loc[row, c]:6.3f}" for c in tickers)
    print(f"{row:<8}{values}")

pairs = []
for a, b in itertools.combinations(tickers, 2):
    pairs.append((a, b, corr.loc[a, b]))

pairs.sort(key=lambda x: x[2])

print("\nLowest correlation (most independent):")
for a, b, c in pairs[:3]:
    print(f"  {a} / {b}: {c:.3f}")

print("\nHighest correlation (most redundant):")
for a, b, c in pairs[-3:]:
    print(f"  {a} / {b}: {c:.3f}")
```

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

## What this tells us

The most striking result is the AAPL-MSFT pair at 0.128 -- the two largest companies in the world by market capitalization barely move together on a daily basis. This low correlation is partly explained by their different revenue profiles: Apple derives the majority of its revenue from consumer hardware with product cycle seasonality, while Microsoft's revenue is dominated by enterprise cloud subscriptions and software licensing. Despite both being classified as "Big Tech," their business fundamentals respond to different demand signals.

Apple's low correlation extends beyond Microsoft. Its three lowest pairs (MSFT at 0.128, META at 0.195, NVDA at 0.236) are all well below the threshold where diversification benefits diminish. Apple functions as a partial diversifier within the Mag 7 group itself.

The highest correlation in the matrix is AMZN-META at 0.443, which reflects their shared exposure to digital advertising revenue and consumer spending cycles. The META-NVDA and MSFT-NVDA pairs at 0.393 likely reflect the AI infrastructure theme that links GPU demand (Nvidia) to the cloud platforms (Meta, Microsoft) deploying those GPUs.

The maximum correlation of 0.443 is well below the 0.6-0.7 range where diversification benefits substantially erode. By this measure, the Magnificent 7 are not one trade -- they are a collection of loosely related businesses with moderate correlation that provides genuine intra-group diversification.

## So what?

For investors concerned about Mag 7 concentration in index funds, the correlation data provides some reassurance: holding all six names is not the same as holding a single leveraged position. However, the AMZN-META-NVDA cluster at 0.39-0.44 does represent a correlated sub-group. Investors seeking to reduce Mag 7 exposure efficiently should note that removing Apple would eliminate the most independent member of the group, while removing one of the AMZN-META-NVDA cluster would have less impact on overall portfolio diversification.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
