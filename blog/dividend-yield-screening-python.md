# How to Screen Dividend Stocks by Yield and Quality in Python

High dividend yield is easy to find — but high yield with sustainable profitability is the real screen. A stock yielding 6% with a P/E of 8 and declining ROE might be a value trap. Here's how to screen 15 well-known dividend payers by yield, then filter for quality using P/E and return on equity thresholds.

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

**Output:**

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

VZ tops the yield ranking at 5.8%, and it passes the quality filter with a low P/E of 11.6 and ROE above 15%. The quality filter cuts the list from 15 to 7 — notably excluding CVX (low ROE), ABBV (negative ROE from Humira write-downs), MCD (negative equity), and WMT (sky-high P/E). HD stands out with a 2.9% yield and an extraordinary ROE of 110% — driven by its negative book value from aggressive buybacks, which technically inflates the metric but signals a very shareholder-friendly capital allocation.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
