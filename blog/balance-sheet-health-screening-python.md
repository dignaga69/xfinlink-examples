# How to Screen Stocks by Balance Sheet Health in Python

## What's the question?

Strong earnings do not guarantee financial survival. A company can report record profits and still face insolvency if its short-term obligations exceed its liquid assets or if its debt burden becomes unserviceable during an economic contraction. The balance sheet quantifies these risks through three categories of ratios: liquidity ratios (current ratio, quick ratio) measure the ability to pay bills due within one year, leverage ratios (debt-to-equity, debt-to-assets) measure how heavily the company depends on borrowed capital, and interest coverage (operating income divided by interest expense) measures how many times over the company can meet its debt service obligations from current earnings. Among ten major U.S. equities, which carry the strongest balance sheets and which show signs of financial strain?

## The approach

The xfinlink metrics endpoint retrieves precomputed balance sheet ratios for a batch of tickers in a single call. The most recent annual period for each company is extracted and presented in two views: a liquidity ranking sorted by current ratio, and a leverage ranking sorted by debt-to-equity. A watch list applies two standard credit analysis thresholds to flag elevated risk: a current ratio below 1.0 (meaning current liabilities exceed current assets) or a debt-to-equity ratio above 2.0 (indicating the company has borrowed more than twice its equity base). The screen covers ten stocks across technology, financials, healthcare, energy, and telecommunications to ensure sector diversity.

## Code

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "JNJ", "XOM", "T"]

metrics = xfl.metrics(tickers, period_type="annual",
                      fields=["current_ratio", "quick_ratio", "debt_to_equity", "debt_to_assets", "interest_coverage", "cash_per_share"],
                      period="3y")

latest = metrics.sort_values("period_end").groupby("ticker").tail(1)
latest = latest.sort_values("current_ratio", ascending=False)

print("=== Balance Sheet Health: Liquidity Ratios ===")
print(latest[["ticker", "entity_name", "current_ratio", "quick_ratio", "cash_per_share"]].to_string(index=False))
print()

print("=== Leverage Ratios ===")
lev = latest.sort_values("debt_to_equity", ascending=True)
print(lev[["ticker", "entity_name", "debt_to_equity", "debt_to_assets", "interest_coverage"]].to_string(index=False))
print()

risky = latest[(latest["current_ratio"] < 1) | (latest["debt_to_equity"] > 2)]
print("=== Watch List: Weak Balance Sheets ===")
if len(risky) > 0:
    for _, r in risky.iterrows():
        flags = []
        if r["current_ratio"] < 1:
            flags.append(f"current_ratio={r['current_ratio']:.2f}")
        if r["debt_to_equity"] is not None and r["debt_to_equity"] > 2:
            flags.append(f"debt/equity={r['debt_to_equity']:.2f}")
        print(f"  {r['ticker']}: {', '.join(flags)}")
else:
    print("  All clear")
```

## Output

```
=== Balance Sheet Health: Liquidity Ratios ===
ticker         entity_name  current_ratio  quick_ratio  cash_per_share
  META  Meta Platforms Inc       2.598767          NaN             NaN
  TSLA           TESLA INC       2.164407     1.773665          4.4023
  GOOG        ALPHABET INC       2.005334          NaN          2.5404
  MSFT      MICROSOFT CORP       1.353446     1.346804          4.0711
   XOM    EXXON MOBIL CORP       1.152800     0.835103          2.5769
  AMZN      AMAZON COM INC       1.050815     0.875017          8.0700
   JNJ   JOHNSON & JOHNSON       1.027676     0.765492          8.1784
     T         A T & T INC       0.906136          NaN          2.6046
  AAPL           Apple Inc       0.893293     0.858770          2.4466
   JPM JPMORGAN CHASE & CO            NaN          NaN          8.0639

=== Leverage Ratios ===
ticker         entity_name  debt_to_equity  debt_to_assets  interest_coverage
  TSLA           TESLA INC        0.099261        0.059163          12.884615
  GOOG        ALPHABET INC        0.112090        0.078193         175.324728
  MSFT      MICROSOFT CORP        0.116898        0.064866          53.890147
   XOM    EXXON MOBIL CORP        0.143801        0.083077          69.437811
  AMZN      AMAZON COM INC        0.160809        0.080806          35.169305
   JPM JPMORGAN CHASE & CO        0.178723        0.014639          32.590513
  META  Meta Platforms Inc        0.271585        0.161193          76.400000
   JNJ   JOHNSON & JOHNSON        0.587818        0.240615          34.554068
     T         A T & T INC        1.065040        0.320606           3.551146
  AAPL           Apple Inc        1.170534        0.240248                NaN

=== Watch List: Weak Balance Sheets ===
  T: current_ratio=0.91
  AAPL: current_ratio=0.89
```

## What this tells us

Two companies trigger the watch list, and they illustrate the critical distinction between voluntary and involuntary balance sheet weakness. Apple carries the highest debt-to-equity ratio in the group (1.17) and a current ratio of 0.89, both of which would ordinarily signal concern. However, Apple generates approximately $100 billion in annual operating cash flow, which renders traditional liquidity thresholds less informative. The company deliberately maintains a leveraged balance sheet to fund share repurchases at a cost of debt lower than its cost of equity -- a rational capital allocation decision for a business with highly predictable revenue.

AT&T presents a materially different risk profile. Its current ratio of 0.91 is paired with interest coverage of only 3.6x, the lowest in the group by a substantial margin. At that level, a moderate decline in operating income could impair the company's ability to service its debt without asset sales or refinancing. The combination of thin liquidity and constrained interest coverage represents genuine balance sheet stress rather than a deliberate capital structure choice.

On the opposite end, Tesla maintains the most conservative balance sheet with a debt-to-equity ratio of 0.10, funded primarily through equity and retained earnings. Alphabet records interest coverage of 175x, a level at which debt obligations are effectively immaterial to financial health.

## So what?

Balance sheet analysis provides information that income statement metrics cannot: whether a company can withstand adverse conditions without external financing. The distinction between Apple and AT&T demonstrates that identical ratio thresholds can signal entirely different risk levels depending on cash flow predictability and debt service capacity. When screening for financial health, interest coverage is the most discriminating single metric -- companies above 10x have substantial margin for error, while those below 5x require careful examination of their debt maturity schedules and refinancing options.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
