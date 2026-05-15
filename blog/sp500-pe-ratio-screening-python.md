# How to Screen Blue-Chip Stocks by P/E Ratio in Python

## What's the question?

The price-to-earnings ratio (P/E) -- a stock's current price divided by its earnings per share -- is the most widely used valuation metric in equity analysis. A low P/E suggests the market expects modest future growth or is discounting near-term risk, while a high P/E implies the market is pricing in substantial earnings expansion. When applied across a diversified basket of blue-chip stocks, P/E screening reveals which sectors the market considers mature and which it values for growth. What does the valuation landscape look like across 30 major S&P 500 companies spanning all 11 GICS sectors?

## The approach

We retrieve the most recent annual valuation metrics for 30 blue-chip stocks selected to cover every GICS sector (Global Industry Classification Standard -- the standard sector taxonomy used by index providers). For each stock, we pull the P/E ratio, price-to-book ratio (P/B, which compares market price to accounting book value), and earnings yield (the inverse of P/E, expressed as a percentage).

After filtering out companies with negative or missing P/E ratios -- which typically indicates a loss-making period and renders the metric uninterpretable -- we rank the universe from cheapest to most expensive. Summary statistics provide context for whether the current valuation regime is elevated relative to historical norms.

## Code

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# 30 blue-chip S&P 500 stocks across all 11 GICS sectors
tickers = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",  # Tech / Comm / Consumer
    "JPM", "BAC", "GS", "BRK.B", "V",          # Financials
    "UNH", "JNJ", "PFE", "LLY", "ABBV",        # Healthcare
    "XOM", "CVX", "COP",                        # Energy
    "PG", "KO", "PEP", "WMT", "COST",          # Consumer Staples / Disc
    "CAT", "HON", "UPS",                        # Industrials
    "NEE", "DUK",                               # Utilities
    "AMT", "PLD",                               # Real Estate
]

# Fetch valuation metrics — latest annual period for each
metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["pe_ratio", "pb_ratio", "earnings_yield", "dividend_yield"],
                      period="3y")

# Keep only the most recent period per ticker
metrics = metrics.sort_values("period_end").groupby("ticker").tail(1)

# Drop rows where PE is missing or negative (unprofitable)
valid = metrics.dropna(subset=["pe_ratio"])
valid = valid[valid["pe_ratio"] > 0].copy()

# Top 10 cheapest by P/E
cheapest = valid.nsmallest(10, "pe_ratio")[["ticker", "entity_name", "period_end", "pe_ratio", "pb_ratio", "earnings_yield"]]
print("=== 10 Cheapest Blue Chips by P/E Ratio ===")
print(cheapest.to_string(index=False))
print()

# Top 10 most expensive by P/E
expensive = valid.nlargest(10, "pe_ratio")[["ticker", "entity_name", "period_end", "pe_ratio", "pb_ratio", "earnings_yield"]]
print("=== 10 Most Expensive Blue Chips by P/E Ratio ===")
print(expensive.to_string(index=False))
print()

# Summary stats
print("=== P/E Summary (30 Blue Chips) ===")
print(f"Median P/E: {valid['pe_ratio'].median():.1f}")
print(f"Mean P/E:   {valid['pe_ratio'].mean():.1f}")
print(f"Min P/E:    {valid['pe_ratio'].min():.1f} ({valid.loc[valid['pe_ratio'].idxmin(), 'ticker']})")
print(f"Max P/E:    {valid['pe_ratio'].max():.1f} ({valid.loc[valid['pe_ratio'].idxmax(), 'ticker']})")
```

## Output

```
=== 10 Cheapest Blue Chips by P/E Ratio ===
ticker               entity_name period_end  pe_ratio  pb_ratio  earnings_yield
   BAC      BANK OF AMERICA CORP 2025-12-31     13.85      1.23        0.081500
   UPS UNITED PARCEL SERVICE INC 2025-12-31     15.26      4.51        0.076110
   JPM       JPMORGAN CHASE & CO 2025-12-31     15.30      2.28        0.069085
    GS   GOLDMAN SACHS GROUP INC 2025-12-31     18.04      2.19        0.062884
   COP            CONOCOPHILLIPS 2025-12-31     18.09      2.18        0.056886
   PFE                PFIZER INC 2025-12-31     19.47      1.74        0.051610
   DUK          DUKE ENERGY CORP 2025-12-31     19.79      1.88        0.051033
   JNJ         JOHNSON & JOHNSON 2025-12-28     20.17      6.58        0.049986
   XOM          EXXON MOBIL CORP 2025-12-31     21.88      2.34        0.047475
    PG       PROCTER & GAMBLE CO 2025-06-30     22.44      6.54        0.046690

=== 10 Most Expensive Blue Chips by P/E Ratio ===
ticker           entity_name period_end  pe_ratio  pb_ratio  earnings_yield
  ABBV            ABBVIE INC 2025-12-31     85.89   -109.61        0.011790
  COST COSTCO WHOLESALE CORP 2025-08-31     55.58     15.40        0.018038
   WMT           WALMART INC 2026-01-31     47.69     10.42        0.021091
   CAT       CATERPILLAR INC 2025-12-31     47.62     19.55        0.021312
  NVDA           NVIDIA CORP 2026-01-25     43.16     32.68        0.023358
   LLY        LILLY ELI & CO 2025-12-31     42.48     34.66        0.022441
   PLD              PROLOGIS 2025-12-31     39.97      2.49        0.025088
  AAPL             Apple Inc 2025-09-27     38.53     57.26        0.026532
  AMZN        AMAZON COM INC 2025-12-31     37.82      7.10        0.026627
  GOOG          ALPHABET INC 2025-12-31     36.57     11.51        0.027660

=== P/E Summary (30 Blue Chips) ===
Median P/E: 28.1
Mean P/E:   31.7
Min P/E:    13.8 (BAC)
Max P/E:    85.9 (ABBV)
```

## What this tells us

Banks dominate the cheapest end of the screen. BAC, JPM, and GS all trade below 20x earnings, reflecting a persistent market discount applied to financial sector earnings, which investors view as more cyclical and harder to forecast than other sectors. Energy companies (COP, XOM) and defensive staples (PG) also cluster in the low-P/E range.

At the expensive end, ABBV's 86x P/E requires careful interpretation. AbbVie's near-term earnings were compressed by the Humira patent cliff -- the expiration of exclusivity on its best-selling drug -- so the elevated ratio reflects the market pricing in an earnings recovery rather than overvaluation in the conventional sense. Its negative P/B ratio (driven by negative book value from acquisition goodwill write-downs) reinforces that this is a company where headline ratios must be read in context.

The median P/E of 28.1 for this blue-chip basket exceeds the long-run S&P 500 average of approximately 20x, consistent with an extended period of elevated equity valuations.

## So what?

P/E is a useful first-pass filter, but it requires context to be actionable. A low P/E can indicate genuine undervaluation, or it can reflect justified skepticism about future earnings (a value trap). A high P/E can signal overvaluation, or it can reflect temporary earnings compression that the market expects to reverse. The productive next step after a P/E screen is to examine the earnings trajectory: is the P/E high because the price is elevated, or because the E is temporarily depressed? Combining P/E with earnings yield and earnings growth rate converts a simple ranking into a defensible investment thesis.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
