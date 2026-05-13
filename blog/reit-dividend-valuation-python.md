# How to Screen REITs by Dividend Yield and Valuation in Python

REITs are required to distribute 90% of taxable income as dividends, making yield the primary metric. But comparing REITs by PE and P/B reveals which sub-sectors (net lease, towers, healthcare, storage, residential) the market values most.

## Code

See [`reit-dividend-valuation-python.py`](reit-dividend-valuation-python.py)

## Output

```
=== REIT Dividend & Valuation Screen ===
  VICI   VICI PROPERTIES INC        yield= 6.2%  PE=  10.9  P/B=  1.1  D/E= 1.22
  O      REALTY INCOME CORP         yield= 5.1%  PE=  53.4  P/B=  1.5  D/E= 0.65
  EQR    EQUITY RESIDENTIAL         yield= 4.2%  PE=  22.4  P/B=  2.2  D/E= 0.80
  PSA    PUBLIC STORAGE             yield= 3.9%  PE=  34.5  P/B=  5.9  D/E= 1.11
  AMT    AMERICAN TOWER CORP        yield= 3.8%  PE=  33.1  P/B= 22.8  D/E= 9.32
  WELL   WELLTOWER INC              yield= 1.3%  PE= 156.5  P/B=  3.6  D/E= 0.46
```

## Discussion

VICI leads on yield (6.2%) with the lowest PE (10.9) and P/B near book value (1.1) -- the classic value REIT, backed by casino properties with triple-net leases. AMT's extreme P/B of 22.8 and D/E of 9.32 reflect tower REITs' asset-light model with massive goodwill from acquisitions. WELL's 156x PE is misleading -- healthcare REITs use Funds From Operations (FFO) not earnings, and WELL's depressed GAAP earnings are driven by depreciation on aging properties. For REITs, dividend yield and P/B are more relevant valuation metrics than PE.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
