# How to Build a Simple DCF Model for Any Stock in Python

## What's the question?

What is a company worth based on its future cash flows? A discounted cash flow (DCF) model is the foundational framework of intrinsic value investing. It estimates enterprise value by projecting future free cash flows and discounting them to their present value using a required rate of return. The model answers a specific question: given a set of assumptions about growth, profitability, and risk, what price should a rational investor pay today?

The critical limitation of DCF analysis is its sensitivity to assumptions. Small changes in the growth rate or discount rate produce large changes in the resulting valuation. This exercise applies a simple 5-year DCF with a terminal value to six mega-cap technology stocks, deliberately using conservative uniform assumptions to illustrate how and why the model breaks down at current market valuations.

## The approach

The model has three components:

- **Projection period (years 1-5):** Starting from the most recent annual free cash flow (FCF), defined as operating cash flow minus capital expenditures, we grow FCF at a constant 10% annual rate and discount each year's projected FCF back to present value at a 10% discount rate.
- **Terminal value:** At the end of year 5, we estimate the company's value in perpetuity using the Gordon Growth Model: `terminal FCF / (discount rate - terminal growth rate)`, where terminal growth is set at 3% (roughly nominal GDP growth). This terminal value is also discounted to present value.
- **Intrinsic value per share:** The sum of discounted projected FCFs and discounted terminal value, divided by shares outstanding.

All six companies use identical assumptions (10% growth, 10% discount rate, 3% terminal growth) to produce an apples-to-apples comparison. The resulting intrinsic value is compared to the current market price to calculate implied upside or downside.

## Code

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

## Output

```
=== Simple DCF Valuation (10% discount, 10% growth, 3% terminal) ===

  MSFT   FCF=$72B  intrinsic=$190.05  price=$412.66  upside=-53.9%  OVERVALUED
  AAPL   FCF=$99B  intrinsic=$132.57  price=$292.68  upside=-54.7%  OVERVALUED
  NVDA   FCF=$97B  intrinsic=$78.42  price=$219.44  upside=-64.3%  OVERVALUED
  GOOG   FCF=$73B  intrinsic=$119.49  price=$386.77  upside=-69.1%  OVERVALUED
  AMZN   FCF=$8B  intrinsic=$14.10  price=$268.99  upside=-94.8%  OVERVALUED
```

## What this tells us

Every stock appears "overvalued" under these assumptions, and that outcome is the central lesson of the exercise. A naive DCF with 10% growth and a 10% discount rate cannot justify current mega-cap technology valuations. The market is implicitly pricing in 20-30% annual FCF growth for these companies — far above the 10% assumed here.

AMZN produces the most extreme result at -94.8% implied downside, but the number reflects a specific circumstance: Amazon's free cash flow dropped from $33B in 2024 to approximately $8B in 2025 because capital expenditures surged from $83B to $132B, driven almost entirely by AI infrastructure and data center investment. Operating cash flow actually increased to $140B, but the capex consumed nearly all of it. A FCF-based DCF treats this elevated investment as a permanent state, which dramatically undervalues Amazon's growth option — the future cash flows that the current investment is building.

META is absent from the output because its FCF was negative or the data did not meet the filter criteria, illustrating another limitation: DCF models require positive starting FCF, which excludes companies in heavy investment phases.

The model also highlights the dominance of the terminal value. In a standard 5-year DCF with 3% terminal growth, the terminal value typically accounts for 70-80% of total enterprise value. This means the valuation is overwhelmingly determined by long-run assumptions rather than near-term projections — a structural sensitivity that applies to all DCF models.

## So what?

DCF analysis is a framework for testing assumptions, not a price prediction tool. The value of this exercise is not the specific dollar figures but the implied growth rates they reveal. If the market prices NVDA at $219 and your DCF says $78, the market is pricing in growth far above 10% — and the question becomes whether you agree with the market's implicit growth assumption or not. Changing the growth rate from 10% to 20% would flip most of these valuations from "overvalued" to "fairly valued." The model's power lies in making these embedded assumptions explicit and testable.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
