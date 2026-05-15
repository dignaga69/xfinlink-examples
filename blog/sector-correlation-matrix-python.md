# How to Build a Sector Correlation Matrix for Portfolio Diversification in Python

## What's the question?

Diversification is the only free lunch in finance, but it only works when holdings respond to different economic forces. A portfolio split evenly across eight sector ETFs appears diversified, yet if those sectors move in lockstep, the portfolio behaves like a single concentrated bet. The core question is empirical: which U.S. equity sectors provide genuine return independence, and which are redundant from a risk perspective?

A correlation matrix quantifies this. Each cell contains the Pearson correlation coefficient between two sectors' daily return series, ranging from -1 (perfect inverse movement) to +1 (perfect co-movement). Values near zero indicate statistical independence -- the ideal condition for diversification.

## The approach

Eight SPDR sector ETFs serve as proxies for the major segments of the U.S. equity market: Technology (XLK), Financials (XLF), Healthcare (XLV), Energy (XLE), Consumer Discretionary (XLY), Consumer Staples (XLP), Industrials (XLI), and Utilities (XLU). One year of daily returns is fetched for each, pivoted into a wide-format DataFrame (one column per sector), and the pairwise Pearson correlation is computed across all 28 unique pairs. The three highest and three lowest correlations are extracted to identify the most redundant and most diversifying combinations.

## Code

```python
import itertools
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["XLK", "XLF", "XLV", "XLE", "XLY", "XLP", "XLI", "XLU"]

sector_labels = {
    "XLK": "Tech",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLY": "ConsDisc",
    "XLP": "ConsStaples",
    "XLI": "Industrials",
    "XLU": "Utilities",
}

prices = xfl.prices(tickers, period="1y", fields=["return_daily"])

pivot = prices.pivot_table(index="date", columns="ticker", values="return_daily")
pivot = pivot.rename(columns=sector_labels)

col_order = ["Energy", "Financials", "Industrials", "Tech",
             "ConsStaples", "Utilities", "Healthcare", "ConsDisc"]
pivot = pivot[col_order]

corr = pivot.corr()

print("=== Sector Correlation Matrix (1Y Daily Returns) ===")
header = "             " + "  ".join(f"{c:>11}" for c in col_order)
print(header)

for row_label in col_order:
    values = "  ".join(f"{corr.loc[row_label, c]:11.3f}" for c in col_order)
    print(f"{row_label:<13}{values}")

pairs = []
for a, b in itertools.combinations(col_order, 2):
    pairs.append((a, b, corr.loc[a, b]))

pairs.sort(key=lambda x: x[2])

print("\nMost correlated pairs:")
for a, b, c in pairs[-3:]:
    print(f"  {a} ↔ {b}: {c:.3f}")

print("\nLeast correlated pairs (best diversifiers):")
for a, b, c in pairs[:3]:
    print(f"  {a} ↔ {b}: {c:.3f}")
```

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

## What this tells us

Energy is the standout diversifier in this matrix. Its highest correlation with any other sector is 0.100 (Consumer Staples), and it is slightly negative with both Technology (-0.049) and Consumer Discretionary (-0.013). Adding energy exposure to a portfolio dominated by growth sectors provides genuine risk reduction, not merely the appearance of it.

The Technology-Consumer Staples pair at -0.152 is the only meaningfully negative correlation in the entire matrix. These two sectors respond to opposing economic conditions: technology benefits from risk appetite and growth expectations, while consumer staples attract capital during defensive rotations. This inverse relationship makes them natural hedges within an equity-only portfolio.

At the other extreme, Financials, Industrials, and Consumer Discretionary form a tightly correlated cluster with all pairwise correlations above 0.61. These three sectors are all proxies for the same underlying factor -- economic growth expectations. Holding all three does not meaningfully diversify; it triples down on a single macroeconomic bet.

## So what?

For portfolio construction, the actionable finding is that sector selection matters more than sector count. An eight-sector portfolio where half the weight sits in the Financials-Industrials-ConsDisc cluster is less diversified than a four-sector portfolio that pairs Technology with Consumer Staples and adds Energy. The correlation matrix provides the empirical basis for those allocation decisions. Before adding a new sector position, check its correlation against existing holdings -- if it exceeds 0.5 with anything already in the portfolio, the marginal diversification benefit is limited.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
