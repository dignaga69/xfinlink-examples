# Full write-up: https://xfinlink.com/blog/sector-performance-ytd-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

# One SPDR ETF per GICS sector
sector_tickers = {
    "XLK": "Technology", "XLF": "Financials", "XLV": "Health Care",
    "XLE": "Energy", "XLY": "Cons Disc", "XLP": "Cons Staples",
    "XLI": "Industrials", "XLU": "Utilities", "XLRE": "Real Estate",
    "XLB": "Materials", "XLC": "Comm Svcs",
}
tickers = list(sector_tickers.keys())

# Pull YTD prices
df = xfl.prices(tickers, period="ytd", fields=["close", "return_daily"])

# Calculate YTD total return per sector
ytd = df.sort_values("date").groupby("ticker").agg(
    ytd_return=("return_daily", lambda x: (1 + x).prod() - 1),
    vol=("return_daily", lambda x: x.std() * (252**0.5)),
).round(4)
ytd["sector"] = ytd.index.map(sector_tickers)
ytd = ytd.sort_values("ytd_return", ascending=False)

print("=== Sector Performance YTD (via SPDR ETFs) ===")
for _, r in ytd.iterrows():
    bar = "+" * max(0, int(r["ytd_return"] * 100)) + "-" * max(0, int(-r["ytd_return"] * 100))
    print(f"  {r['sector']:14s}  {r.name:4s}  {r['ytd_return']:+.1%}  vol={r['vol']:.1%}  {bar}")
print()

spread = ytd["ytd_return"].max() - ytd["ytd_return"].min()
print(f"Sector spread: {spread:.1%} (best vs worst)")
print(f"Best:  {ytd.iloc[0]['sector']} ({ytd.index[0]}) at {ytd.iloc[0]['ytd_return']:+.1%}")
print(f"Worst: {ytd.iloc[-1]['sector']} ({ytd.index[-1]}) at {ytd.iloc[-1]['ytd_return']:+.1%}")
