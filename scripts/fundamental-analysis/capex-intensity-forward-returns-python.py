# Full write-up: https://xfinlink.com/blog/capex-intensity-forward-returns-python

import xfinlink as xfl
import pandas as pd

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["AAPL", "MSFT", "AMZN", "META", "XOM", "CAT", "UNH", "HD"]

# -- Fetch 5Y annual fundamentals ------------------------------------------
df = xfl.fundamentals(
    tickers,
    period_type="annual",
    fields=["revenue", "capital_expenditures", "free_cash_flow"],
    period="5y",
)

# -- Compute capex intensity and YoY growth --------------------------------
df = df.sort_values(["ticker", "period_end"])
df["capex_abs"] = df["capital_expenditures"].abs()
df["intensity"] = df["capex_abs"] / df["revenue"]
df["capex_yoy"] = df.groupby("ticker")["capex_abs"].pct_change()

# -- Latest annual period per ticker ---------------------------------------
latest = df.sort_values("period_end").groupby("ticker").tail(1).copy()
latest = latest.sort_values("intensity", ascending=False)

print("=== Capex Intensity: Who Is Investing the Most? (Latest Annual) ===")
header = (
    f"{'Ticker':6s}  {'Period':>12s}  {'Revenue':>12s}  {'Capex':>12s}  "
    f"{'Intensity':>10s}  {'Capex YoY':>10s}"
)
print(header)
print("-" * 65)

for _, r in latest.iterrows():
    rev_str = f"${r['revenue'] / 1e3:>8.0f}B"
    capex_str = f"${r['capex_abs'] / 1e3:>8.0f}B"
    intensity_str = f"{r['intensity']:>9.1%}"
    yoy_str = f"{r['capex_yoy']:>+9.1%}" if pd.notna(r["capex_yoy"]) else "      N/A"
    print(
        f"{r['ticker']:6s}  {str(r['period_end'])[:10]:>12s}  {rev_str:>12s}  "
        f"{capex_str:>12s}  {intensity_str:>10s}  {yoy_str:>10s}"
    )

# -- AMZN trajectory -------------------------------------------------------
print("\n=== AMZN Capex Trajectory ===")
amzn = df[df["ticker"] == "AMZN"].dropna(subset=["capex_abs"])
for _, r in amzn.iterrows():
    yoy_str = f"YoY={r['capex_yoy']:+.1%}" if pd.notna(r["capex_yoy"]) else "YoY=N/A"
    print(
        f"  {str(r['period_end'])[:10]}  "
        f"capex=${r['capex_abs'] / 1e3:.0f}B  "
        f"intensity={r['intensity']:.1%}  "
        f"{yoy_str}"
    )

# -- META trajectory -------------------------------------------------------
print("\n=== META Capex Trajectory ===")
meta = df[df["ticker"] == "META"].dropna(subset=["capex_abs"])
for _, r in meta.iterrows():
    yoy_str = f"YoY={r['capex_yoy']:+.1%}" if pd.notna(r["capex_yoy"]) else "YoY=N/A"
    print(
        f"  {str(r['period_end'])[:10]}  "
        f"capex=${r['capex_abs'] / 1e3:.0f}B  "
        f"intensity={r['intensity']:.1%}  "
        f"{yoy_str}"
    )
