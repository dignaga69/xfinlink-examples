# How to Screen Dividend Stocks by Yield and Quality in Python

## What's the question?

Dividend yield -- the annual dividend payment divided by the stock price -- is the most commonly used metric for identifying income-producing stocks. However, a high yield alone is not a reliable indicator of investment quality. A stock can yield 6% because its price has collapsed in anticipation of a dividend cut, or because its earnings are declining and the payout is unsustainable. The productive question is not which stocks have the highest yield, but which stocks combine meaningful yield with the financial health to sustain it. How do you screen for yield while simultaneously filtering for quality?

## The approach

We start with 15 well-known dividend-paying stocks, including several Dividend Aristocrats -- companies that have increased their dividend for at least 25 consecutive years. For each stock, we retrieve the dividend yield, P/E ratio, and return on equity (ROE, which measures net income as a percentage of shareholders' equity and indicates how efficiently a company generates profit from its capital base).

A quality filter is then applied with three simultaneous conditions: dividend yield above 2%, P/E ratio between 0 and 25 (excluding unprofitable companies and those trading at extreme valuations), and ROE above 15% (indicating strong capital efficiency). Stocks that pass all three criteria represent the intersection of income and financial strength.

## Code

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

# Dividend aristocrats and other well-known dividend payers
tickers = [
    "JNJ", "PG", "KO", "PEP", "MCD",
    "MMM", "T", "VZ", "XOM", "CVX",
    "ABBV", "IBM", "HD", "WMT", "LOW",
]

# Get dividend yield and payout metrics
metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["dividend_yield", "pe_ratio", "roe", "fcf_per_share", "earnings_yield"],
                      period="3y")

# Keep most recent period per ticker
latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.dropna(subset=["dividend_yield"])
latest = latest.sort_values("dividend_yield", ascending=False)

print("=== Dividend Yield Ranking (Annual, Most Recent) ===")
cols = ["ticker", "entity_name", "period_end", "dividend_yield", "pe_ratio", "roe"]
print(latest[cols].to_string(index=False))
print()

# Calculate a simple quality score: yield > 2%, PE < 25, ROE > 15%
quality = latest[
    (latest["dividend_yield"] > 0.02) &
    (latest["pe_ratio"] > 0) &
    (latest["pe_ratio"] < 25) &
    (latest["roe"] > 0.15)
].copy()
print("=== Quality Dividend Stocks (yield>2%, PE<25, ROE>15%) ===")
print(quality[cols].to_string(index=False) if len(quality) > 0 else "None found")
```

## Output

```
=== Dividend Yield Ranking (Annual, Most Recent) ===
ticker                      entity_name period_end  dividend_yield  pe_ratio       roe
    VZ       VERIZON COMMUNICATIONS INC 2025-12-31        0.058080     11.60  0.162416
     T                      A T & T INC 2025-12-31        0.043943      8.31  0.173554
   CVX                     CHEVRON CORP 2025-12-31        0.037479     27.53  0.065964
   PEP                      PEPSICO INC 2025-12-27        0.035975     26.05  0.403803
  ABBV                       ABBVIE INC 2025-12-31        0.032805     85.89 -1.292355
   IBM INTERNATIONAL BUSINESS MACHS COR 2025-12-31        0.029009     20.71  0.324461
    HD                   HOME DEPOT INC 2026-02-01        0.028515     22.67  1.104815
    PG              PROCTER & GAMBLE CO 2025-06-30        0.027908     22.44  0.305524
   XOM                 EXXON MOBIL CORP 2025-12-31        0.027289     21.88  0.111201
    KO                     COCA COLA CO 2025-12-31        0.026010     25.80  0.407442
   MCD                   MCDONALDS CORP 2025-12-31        0.025273     23.74 -4.781128
   JNJ                JOHNSON & JOHNSON 2025-12-28        0.023100     20.17  0.328706
   LOW              LOWES COMPANIES INC 2026-01-30        0.020573     19.48 -0.670969
   MMM                            3M CO 2025-12-31        0.020313     23.96  0.691195
   WMT                      WALMART INC 2026-01-31        0.007220     47.69  0.219772

=== Quality Dividend Stocks (yield>2%, PE<25, ROE>15%) ===
ticker                      entity_name period_end  dividend_yield  pe_ratio      roe
    VZ       VERIZON COMMUNICATIONS INC 2025-12-31        0.058080     11.60 0.162416
     T                      A T & T INC 2025-12-31        0.043943      8.31 0.173554
   IBM INTERNATIONAL BUSINESS MACHS COR 2025-12-31        0.029009     20.71 0.324461
    HD                   HOME DEPOT INC 2026-02-01        0.028515     22.67 1.104815
    PG              PROCTER & GAMBLE CO 2025-06-30        0.027908     22.44 0.305524
   JNJ                JOHNSON & JOHNSON 2025-12-28        0.023100     20.17 0.328706
   MMM                            3M CO 2025-12-31        0.020313     23.96 0.691195
```

## What this tells us

The quality filter reduces the universe from 15 stocks to 7, and the exclusions are instructive. CVX is eliminated despite a 3.7% yield because its ROE of 6.6% falls below the 15% threshold, indicating relatively inefficient capital deployment for an energy company. ABBV is excluded for its negative ROE, a consequence of write-downs related to the Humira patent expiration. MCD and LOW both show negative ROE -- in their case, driven by negative shareholders' equity resulting from aggressive share repurchase programs rather than operational weakness, though the metric remains disqualifying under a mechanical screen.

VZ and T lead the quality-filtered list with yields of 5.8% and 4.4%, respectively, combined with moderate P/E ratios and ROE above the 15% threshold. HD presents an anomalous ROE of 110%, which results from negative book value caused by extensive share buybacks. The metric is technically accurate but overstates the operational efficiency.

## So what?

A dividend yield screen without quality filters will consistently surface value traps -- stocks with high yields that are about to cut their dividends or experience further price declines. Adding P/E and ROE thresholds transforms a yield-only ranking into a quality-income screen that eliminates the most common failure modes. For a more robust implementation, consider adding free cash flow payout ratio (dividends divided by free cash flow) to verify that dividends are funded by cash generation rather than debt issuance, and examine the dividend growth history to confirm sustainability.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
