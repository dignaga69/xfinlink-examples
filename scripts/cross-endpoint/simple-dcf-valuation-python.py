# Full write-up: https://xfinlink.com/blog/simple-dcf-valuation-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

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
