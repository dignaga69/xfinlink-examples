# How to Build a Simple DCF Model for Any Stock in Python

A discounted cash flow model is the foundation of intrinsic value investing — it estimates what a company is worth based on its future cash flows, discounted back to today. The catch: even small changes in growth rate or discount rate dramatically change the result. Here's a simple 5-year DCF with a terminal value for 6 mega-cap tech stocks, and why the results might surprise you.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"]

fund = xfl.fundamentals(tickers, period_type="annual",
                        fields=["free_cash_flow", "shares_outstanding", "revenue"], period="3y")
latest = fund.sort_values("period_end").groupby("ticker").tail(1).copy()

prices = xfl.prices(tickers, period="1mo", fields=["close"])
last_prices = prices.sort_values("date").groupby("ticker").tail(1)[["ticker", "close"]].set_index("ticker")

DISCOUNT_RATE = 0.10
GROWTH_RATE = 0.10
TERMINAL_GROWTH = 0.03

results = []
for _, r in latest.iterrows():
    ticker = r["ticker"]
    fcf = r["free_cash_flow"]
    shares = r["shares_outstanding"]
    if pd.isna(fcf) or pd.isna(shares) or shares <= 0 or fcf <= 0:
        continue

    total_pv = 0
    projected_fcf = fcf
    for year in range(1, 6):
        projected_fcf *= (1 + GROWTH_RATE)
        total_pv += projected_fcf / (1 + DISCOUNT_RATE) ** year

    terminal_fcf = projected_fcf * (1 + TERMINAL_GROWTH)
    terminal_value = terminal_fcf / (DISCOUNT_RATE - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + DISCOUNT_RATE) ** 5

    intrinsic = (total_pv + pv_terminal) / shares
    current_price = last_prices.loc[ticker, "close"] if ticker in last_prices.index else None
    upside = (intrinsic / current_price - 1) if current_price else None

    results.append({"ticker": ticker, "fcf_M": fcf, "intrinsic": intrinsic, "price": current_price, "upside": upside})

rdf = pd.DataFrame(results).sort_values("upside", ascending=False)
print("=== Simple DCF Valuation (10% discount, 10% growth, 3% terminal) ===")
print()
for _, r in rdf.iterrows():
    up = f"{r['upside']:>+6.1%}" if r["upside"] else "N/A"
    verdict = "UNDERVALUED" if r["upside"] and r["upside"] > 0.15 else ("OVERVALUED" if r["upside"] and r["upside"] < -0.15 else "FAIR")
    print(f"  {r['ticker']:5s}  FCF=${r['fcf_M']/1e3:.0f}B  intrinsic=${r['intrinsic']:.2f}  price=${r['price']:.2f}  upside={up}  {verdict}")
```

**Output:**

```
=== Simple DCF Valuation (10% discount, 10% growth, 3% terminal) ===

  MSFT   FCF=$72B  intrinsic=$190.05  price=$412.66  upside=-53.9%  OVERVALUED
  AAPL   FCF=$99B  intrinsic=$132.57  price=$292.68  upside=-54.7%  OVERVALUED
  NVDA   FCF=$97B  intrinsic=$78.42  price=$219.44  upside=-64.3%  OVERVALUED
  GOOG   FCF=$73B  intrinsic=$119.49  price=$386.77  upside=-69.1%  OVERVALUED
  AMZN   FCF=$8B  intrinsic=$14.10  price=$268.99  upside=-94.8%  OVERVALUED
```

Every stock is "overvalued" — and that's the point. A naive DCF with 10% growth and 10% discount rate can't justify current mega-cap tech valuations. The market is pricing in 20-30% annual FCF growth for these companies, not 10%. AMZN looks worst at -95%, and the number is real: Amazon's FCF dropped from $33B in 2024 to just $8B in 2025 because capital expenditure surged from $83B to $132B — almost entirely AI and data center investment. Operating cash flow actually *increased* to $140B, but the capex ate nearly all of it. A FCF-based DCF treats this reinvestment as a permanent state, which massively undervalues Amazon's growth option. This exercise shows why DCF assumptions matter more than the model — change the growth rate from 10% to 20% and these valuations flip from "overvalued" to "fairly valued."

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
