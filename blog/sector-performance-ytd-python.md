# How to Compare Sector Performance YTD Using Python

Sector rotation is one of the most reliable macro signals — when money flows from defensives into cyclicals (or vice versa), it tells you what the market thinks about the economy. By tracking YTD returns across all 11 GICS sectors via SPDR ETFs, you can see where the market is allocating capital right now.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== Sector Performance YTD (via SPDR ETFs) ===
  Energy          XLE   +24.6%  vol=23.9%  ++++++++++++++++++++++++
  Technology      XLK   +21.9%  vol=24.9%  +++++++++++++++++++++
  Materials       XLB   +13.8%  vol=19.1%  +++++++++++++
  Industrials     XLI   +11.7%  vol=19.9%  +++++++++++
  Real Estate     XLRE  +10.1%  vol=14.8%  ++++++++++
  Cons Staples    XLP   +8.4%  vol=14.9%  ++++++++
  Utilities       XLU   +4.8%  vol=16.7%  ++++
  Cons Disc       XLY   +0.7%  vol=19.6%  
  Comm Svcs       XLC   -0.7%  vol=14.7%  
  Financials      XLF   -6.5%  vol=16.8%  ------
  Health Care     XLV   -7.3%  vol=14.9%  -------

Sector spread: 31.9% (best vs worst)
Best:  Energy (XLE) at +24.6%
Worst: Health Care (XLV) at -7.3%
```

The 31.9% spread between the best and worst sectors is enormous — simply being in the right sector mattered more than stock selection this year. Energy leads at +24.6%, likely driven by commodity price strength, while Health Care trails at -7.3%, weighed down by regulatory uncertainty and patent cliffs. The interesting signal is Consumer Discretionary at near-zero (+0.7%) — this is the sector most sensitive to consumer spending, and its flat performance suggests the market sees neither boom nor recession ahead.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
