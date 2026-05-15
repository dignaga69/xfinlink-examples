# How to Screen REITs by Dividend Yield and Valuation in Python

## What's the question?

Real estate investment trusts (REITs) are required by law to distribute at least 90% of their taxable income as dividends, making dividend yield the primary return mechanism for REIT investors. But yield alone is incomplete: a high yield may signal value or distress, depending on the underlying valuation. How do major REITs compare across dividend yield, price-to-earnings (PE), price-to-book (P/B), and debt-to-equity (D/E) -- and what do those metrics reveal about how the market values different REIT sub-sectors?

## The approach

Six REITs spanning distinct sub-sectors are evaluated: Realty Income (O, net lease), American Tower (AMT, cell towers), VICI Properties (VICI, gaming/net lease), Public Storage (PSA, self-storage), Welltower (WELL, healthcare facilities), and Equity Residential (EQR, apartments). Three years of annual metrics are fetched for each, and the most recent values are compared. The four metrics -- dividend yield, PE ratio, P/B ratio, and D/E ratio -- are standard equity valuation measures, though their interpretation requires REIT-specific context because GAAP earnings systematically understate REIT profitability due to depreciation accounting.

## Code

```python
import xfinlink as xfl

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

tickers = ["O", "AMT", "VICI", "PSA", "WELL", "EQR"]

metrics = xfl.metrics(
    tickers,
    period="3y",
    fields=["pe_ratio", "pb_ratio", "dividend_yield", "debt_to_equity"],
    period_type="annual",
)

print("=== REIT Dividend & Valuation Screen ===")

results = []
for ticker in tickers:
    m = metrics[metrics["ticker"] == ticker].sort_values("period_end")
    if m.empty:
        continue

    latest = m.iloc[-1]
    div_yield = latest["dividend_yield"] * 100 if latest["dividend_yield"] else 0

    results.append({
        "ticker": ticker,
        "entity_name": latest.get("entity_name", ticker),
        "dividend_yield": div_yield,
        "pe_ratio": latest["pe_ratio"],
        "pb_ratio": latest["pb_ratio"],
        "debt_to_equity": latest["debt_to_equity"],
    })

results.sort(key=lambda x: x["dividend_yield"], reverse=True)

for r in results:
    name = r["entity_name"][:24]
    print(
        f"  {r['ticker']:<6} {name:<24}"
        f"  yield={r['dividend_yield']:4.1f}%"
        f"  PE={r['pe_ratio']:6.1f}"
        f"  P/B={r['pb_ratio']:5.1f}"
        f"  D/E={r['debt_to_equity']:5.2f}"
    )
```

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

## What this tells us

VICI Properties leads on dividend yield (6.2%) while also carrying the lowest PE ratio (10.9) and a P/B near book value (1.1). This is the profile of a classic value REIT: its casino-backed triple-net lease structure generates predictable cash flows with minimal operating expenses, and the market prices it accordingly. The combination of high yield and low valuation multiples suggests the market perceives limited growth upside rather than elevated risk.

American Tower's metrics require sub-sector context. Its P/B ratio of 22.8 and D/E of 9.32 appear alarming in isolation, but tower REITs operate an asset-light model where the balance sheet carries substantial goodwill from acquisitions. The book value of cell tower assets understates their economic value because depreciated book values do not reflect the recurring revenue these assets generate under long-term contracts.

Welltower's PE of 156.5 is the most misleading number in the table. Healthcare REITs report large depreciation charges on aging physical properties, which suppresses GAAP net income. The industry-standard valuation metric for REITs is Funds From Operations (FFO), which adds depreciation back to net income. WELL's FFO-based valuation would be substantially lower than its PE implies.

The broader pattern across these six REITs confirms that PE ratio is a poor valuation tool for the REIT sector. Dividend yield and P/B ratio provide more useful comparisons because they are less distorted by the depreciation accounting that makes GAAP earnings unreliable for asset-heavy businesses.

## So what?

When evaluating REITs, replace PE ratio with FFO-based multiples (P/FFO) as the primary earnings valuation metric. Use dividend yield as the starting point for comparison, then examine P/B and D/E to understand whether the yield is driven by value (low P/B, moderate leverage) or by capital structure (high leverage amplifying distributions). A REIT with a high yield, low P/B, and moderate D/E (like VICI) has a different risk profile than one with a high yield funded by aggressive leverage.

*Built with [xfinlink](https://xfinlink.com) -- free financial data API for Python. `pip install xfinlink`*
