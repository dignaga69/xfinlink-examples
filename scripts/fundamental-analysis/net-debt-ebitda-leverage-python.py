# Full write-up: https://xfinlink.com/blog/net-debt-ebitda-leverage-python

import xfinlink as xfl
import pandas as pd

xfl.api_key = "YOUR_API_KEY"  # free at https://xfinlink.com/signup

# -- Configuration ----------------------------------------------------------
tickers = ["XOM", "DE", "LMT", "CAT", "RTX", "HON", "BA"]

# -- Fetch fundamentals for net debt calculation ----------------------------
fund = xfl.fundamentals(
    tickers,
    period_type="annual",
    fields=["total_debt", "cash_and_equivalents", "ebitda"],
    period="2y",
)

# -- Fetch metrics for D/E, interest coverage, EV/EBITDA -------------------
met = xfl.metrics(
    tickers,
    period_type="annual",
    fields=["debt_to_equity", "interest_coverage", "ev_ebitda"],
    period="2y",
)

# -- Latest period per ticker (fundamentals) --------------------------------
fund_latest = fund.sort_values("period_end").groupby("ticker").tail(1).copy()
met_latest = met.sort_values("period_end").groupby("ticker").tail(1).copy()

# -- Merge and compute net debt / EBITDA ------------------------------------
merged = fund_latest.merge(
    met_latest[["ticker", "debt_to_equity", "interest_coverage", "ev_ebitda"]],
    on="ticker",
    how="left",
)

merged["net_debt"] = merged["total_debt"] - merged["cash_and_equivalents"]
merged["nd_ebitda"] = merged["net_debt"] / merged["ebitda"]
merged = merged.sort_values("nd_ebitda")

# -- Print results ---------------------------------------------------------
print("=== Net Debt / EBITDA: Leverage Screen (Industrials + Energy) ===")
header = (
    f"{'Ticker':6s}  {'Company':>28s}  {'ND/EBITDA':>10s}  {'D/E':>6s}  "
    f"{'Int Cov':>8s}  {'EV/EBITDA':>10s}"
)
print(header)
print("-" * 72)

for _, r in merged.iterrows():
    name = str(r["entity_name"])[:28]
    nd_ebitda_str = f"{r['nd_ebitda']:.1f}x" if pd.notna(r["nd_ebitda"]) else "N/A"
    de_str = f"{r['debt_to_equity']:.2f}" if pd.notna(r["debt_to_equity"]) else "N/A"
    ic_str = f"{r['interest_coverage']:.1f}x" if pd.notna(r["interest_coverage"]) else "N/A"
    ev_str = f"{r['ev_ebitda']:.1f}x" if pd.notna(r["ev_ebitda"]) else "N/A"
    print(
        f"{r['ticker']:6s}  {name:>28s}  {nd_ebitda_str:>10s}  {de_str:>6s}  "
        f"{ic_str:>8s}  {ev_str:>10s}"
    )
