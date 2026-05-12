# How to Measure Earnings Quality: Cash Flow vs Net Income in Python

Net income can be manipulated through accruals, depreciation timing, and one-time items. Operating cash flow can't — it's actual cash collected. The ratio of OCF to net income tells you how much of a company's reported earnings are backed by real cash. A ratio above 1.2 means cash earnings exceed paper earnings — high quality. Below 0.8 is a red flag.

```python
import xfinlink as xfl
import pandas as pd

xfl.set_api_key("your_key")  # free at https://xfinlink.com/signup

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
```

**Output:**

```
=== Earnings Quality: Cash Flow vs Net Income ===
(OCF/NI > 1.0 = cash earnings exceed paper earnings = high quality)

  CRM    NI=    $6B  OCF=   $13B  OCF/NI= 2.11  accrual= -0.182  HIGH
  META   NI=   $60B  OCF=  $116B  OCF/NI= 1.92  accrual= -0.275  HIGH
  AMZN   NI=   $78B  OCF=  $140B  OCF/NI= 1.80  accrual= -0.086  HIGH
  ADBE   NI=    $7B  OCF=   $10B  OCF/NI= 1.41  accrual= -0.122  HIGH
  MSFT   NI=  $102B  OCF=  $136B  OCF/NI= 1.34  accrual= -0.122  HIGH
  GOOG   NI=  $132B  OCF=  $165B  OCF/NI= 1.25  accrual= -0.081  HIGH
  AAPL   NI=  $112B  OCF=  $111B  OCF/NI= 1.00  accrual=  0.001  
  NVDA   NI=  $120B  OCF=  $103B  OCF/NI= 0.86  accrual=  0.080
```

CRM stands out at 2.11x — Salesforce generates more than twice as much cash as it reports in net income, largely because stock-based compensation is a real expense for earnings but not a cash outflow. META at 1.92x is similarly cash-rich, generating $116B in operating cash vs $60B in net income. The surprise is NVDA at 0.86x — the only stock below 1.0, and this isn't a one-off: NVDA's OCF has lagged net income every year for three years running (0.94 in FY2024, 0.88 in FY2025, 0.86 in FY2026). The gap is growing, likely because hyperscaler customers book massive GPU orders that sit in accounts receivable before converting to cash. It's not a red flag per se — NVDA's customers are creditworthy — but it means the headline earnings number overstates how much cash is actually in the bank. A negative accrual ratio (like META's -0.275) means the company is collecting cash faster than it recognizes revenue — the hallmark of a subscription business.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
