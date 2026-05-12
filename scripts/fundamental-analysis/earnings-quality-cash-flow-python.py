# Full write-up: https://xfinlink.com/blog/earnings-quality-cash-flow-python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("YOUR_API_KEY")  # free at https://xfinlink.com/signup

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "CRM", "ADBE"]
df = xfl.fundamentals(tickers, period_type="annual",
                       fields=["revenue", "net_income", "operating_cash_flow"], period="3y")

latest = df.sort_values("period_end").groupby("ticker").tail(1).copy()
latest["ocf_to_ni"] = latest["operating_cash_flow"] / latest["net_income"]
latest["accrual_ratio"] = (latest["net_income"] - latest["operating_cash_flow"]) / latest["revenue"]
latest = latest.sort_values("ocf_to_ni", ascending=False)

print("=== Earnings Quality: Cash Flow vs Net Income ===")
print("(OCF/NI > 1.0 = cash earnings exceed paper earnings = high quality)")
print()
for _, r in latest.iterrows():
    ni = f"${r['net_income']/1e3:.0f}B"
    ocf = f"${r['operating_cash_flow']/1e3:.0f}B" if pd.notna(r["operating_cash_flow"]) else "N/A"
    ratio = f"{r['ocf_to_ni']:.2f}" if pd.notna(r["ocf_to_ni"]) else "N/A"
    acc = f"{r['accrual_ratio']:.3f}" if pd.notna(r["accrual_ratio"]) else "N/A"
    quality = "HIGH" if pd.notna(r["ocf_to_ni"]) and r["ocf_to_ni"] > 1.2 else ("LOW" if pd.notna(r["ocf_to_ni"]) and r["ocf_to_ni"] < 0.8 else "")
    print(f"  {r['ticker']:5s}  NI={ni:>7s}  OCF={ocf:>7s}  OCF/NI={ratio:>5s}  accrual={acc:>7s}  {quality}")
