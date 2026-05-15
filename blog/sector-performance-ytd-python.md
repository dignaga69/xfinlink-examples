# How to Compare Sector Performance YTD Using Python

## What's the question?

Where is capital flowing across equity sectors this year? Sector rotation — the movement of investment capital from one industry group to another — is one of the most reliable indicators of the market's macroeconomic consensus. When money moves from defensive sectors (utilities, consumer staples) into cyclicals (energy, industrials), it signals expectations of economic expansion. The reverse signals caution. Tracking year-to-date returns across all 11 GICS sectors quantifies this rotation in real time.

## The approach

Each GICS sector (Global Industry Classification Standard, the taxonomy used by S&P and MSCI) is represented by its corresponding SPDR ETF. We retrieve year-to-date daily returns for all 11 sector ETFs, compound the daily returns into a single YTD total return per sector, and calculate annualized volatility (daily standard deviation multiplied by the square root of 252 trading days). The spread between the best and worst sectors measures dispersion — a wide spread indicates strong sector rotation rather than a uniform market move.

## Code

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

## Output

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

## What this tells us

The 31.9% spread between the best and worst sectors is substantial. Being in the right sector has mattered more than stock selection within a sector this year. Energy leads at +24.6%, driven by commodity price strength, while Health Care trails at -7.3%, weighed down by regulatory uncertainty and patent expiration timelines.

Consumer Discretionary at near-zero (+0.7%) is a notable data point. This sector is the most sensitive to consumer spending, and its flat performance suggests the market sees neither acceleration nor contraction in household demand.

## So what?

Sector-level return and volatility data provides a concise view of the market's macro positioning. A wide spread confirms that sector allocation is currently a primary driver of portfolio outcomes. Investors benchmarking against broad indices should understand whether their performance gap stems from stock selection or sector exposure — this screen answers that question directly.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
