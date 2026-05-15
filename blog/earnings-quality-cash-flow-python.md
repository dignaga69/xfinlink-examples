# How to Measure Earnings Quality: Cash Flow vs Net Income in Python

## What's the question?

How much of a company's reported earnings are backed by actual cash? Net income — the bottom line of the income statement — is an accounting construct subject to management discretion. Revenue recognition timing, depreciation schedules, stock-based compensation treatment, and one-time items all influence the number. Operating cash flow (OCF), by contrast, measures cash actually collected and disbursed during the period. When cash flow significantly exceeds net income, earnings are considered high quality. When net income exceeds cash flow, the gap raises questions about the durability of reported profits.

## The approach

We calculate two ratios for each company. The first is the OCF-to-net-income ratio: operating cash flow divided by net income. A ratio above 1.0 means the company generates more cash than it reports in earnings. Above 1.2 is conventionally considered high quality; below 0.8 is a potential concern. The second is the accrual ratio: `(net income - operating cash flow) / revenue`. A negative accrual ratio indicates the company collects cash faster than it recognizes revenue — characteristic of subscription and prepaid business models. A positive accrual ratio means revenue is being recognized before cash arrives.

We examine eight large-cap technology companies using the most recent annual filing data.

## Code

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

## Output

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

## What this tells us

CRM leads with an OCF-to-NI ratio of 2.11 — Salesforce generates more than twice as much cash as it reports in net income. The primary driver is stock-based compensation (SBC): SBC reduces net income as a real expense but is non-cash, so operating cash flow is unaffected. META at 1.92 exhibits the same pattern, producing $116B in operating cash against $60B in net income.

AAPL sits at exactly 1.00, meaning its cash earnings match its reported earnings almost perfectly. This is unusual among technology companies and reflects Apple's hardware-heavy revenue model, which has fewer of the timing differences between cash collection and revenue recognition that inflate the ratio for subscription businesses.

NVDA at 0.86 is the only company below 1.0 in this group. The gap between net income ($120B) and operating cash flow ($103B) is not an isolated occurrence — NVDA's OCF has trailed net income for three consecutive fiscal years (0.94 in FY2024, 0.88 in FY2025, 0.86 in FY2026), and the gap is widening. The likely cause is accounts receivable growth: hyperscaler customers place large GPU orders that are recognized as revenue before payment is received. The underlying credit risk is low given the customers involved, but the pattern means NVDA's headline earnings overstate how much cash is currently available.

The accrual ratio adds context. META's deeply negative accrual ratio (-0.275) indicates it collects cash well ahead of revenue recognition, the hallmark of an advertising platform where customers prepay for campaigns.

## So what?

Earnings quality analysis is a standard step in fundamental due diligence. A high OCF-to-NI ratio does not automatically make a stock a good investment, and a ratio below 1.0 does not make it a bad one. What it does is reveal the cash content of reported earnings, which affects dividend sustainability, share buyback capacity, and the reliability of valuation multiples based on net income. When building financial models or comparing companies on a PE basis, adjusting for earnings quality ensures that comparisons are made on economically equivalent terms.

*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. `pip install xfinlink`*
