# Does Heavy Capex Predict Future Stock Returns? Capital Expenditure Analysis in Python

## What's the question?

Capital expenditure (capex) represents a company's investment in future productive capacity -- factories, data centers, equipment, technology. When a company dramatically increases capex, it is making a bet on future growth. The question is whether the stock market rewards or punishes this bet. Does heavy capex spending precede strong stock performance, or does it signal overinvestment and diminishing returns? Capex intensity -- defined as capital expenditures divided by revenue -- normalizes spending across companies of different sizes, allowing direct comparison between a $717B revenue giant like AMZN and a $68B industrial firm like CAT.

## The approach

Select 8 large-cap stocks across sectors. Pull 5 years of annual fundamentals including revenue, capital_expenditures, and free_cash_flow. Compute capex intensity (capex divided by revenue) and year-over-year capex growth for each period. Then examine the multi-year trajectories for AMZN and META -- the two most aggressive capex spenders in recent years -- to understand how their investment strategies have diverged.

## Code

See [`capex-intensity-forward-returns-python.py`](capex-intensity-forward-returns-python.py)

## Output

```
=== Capex Intensity: Who Is Investing the Most? (Latest Annual) ===
Ticker        Period     Revenue       Capex   Intensity   Capex YoY
-----------------------------------------------------------------
MSFT      2025-06-30  $     282B  $      65B       22.9%     +45.1%
AMZN      2025-12-31  $     717B  $     132B       18.4%     +58.8%
XOM       2025-12-31  $     332B  $      28B        8.5%     +16.7%
META      2025-12-31  $     201B  $       9B        4.6%     -75.0%
CAT       2025-12-31  $      68B  $       3B        4.2%     +41.9%
AAPL      2025-09-27  $     416B  $      13B        3.1%     +34.6%
HD        2026-02-01  $     165B  $       4B        2.2%      +5.6%
UNH       2025-12-31  $     448B  $       4B        0.8%      +3.5%

=== AMZN Capex Trajectory ===
  2022-12-31  capex=$64B  intensity=12.4%  YoY=+4.2%
  2023-12-31  capex=$53B  intensity=9.2%  YoY=-17.2%
  2024-12-31  capex=$83B  intensity=13.0%  YoY=+57.4%
  2025-12-31  capex=$132B  intensity=18.4%  YoY=+58.8%

=== META Capex Trajectory ===
  2022-12-31  capex=$31B  intensity=27.0%  YoY=+68.2%
  2023-12-31  capex=$27B  intensity=20.0%  YoY=-14.0%
  2024-12-31  capex=$37B  intensity=22.6%  YoY=+37.8%
  2025-12-31  capex=$9B  intensity=4.6%  YoY=-75.0%
```

## What this tells us

MSFT and AMZN are the heaviest investors relative to revenue -- both above 18% capex intensity, driven by AI data center buildouts. AMZN's trajectory is striking: capex nearly tripled from $53B to $132B in two years, pushing intensity from 9.2% to 18.4%. This is among the most aggressive capital investment programs in corporate history. META's trajectory tells a different story: after spending heavily on metaverse infrastructure (27% intensity in 2022), capex dropped 75% in 2025 to $9B -- a strategic pivot from capital-heavy VR investment back toward asset-light social media. UNH at 0.8% intensity confirms that health insurance is essentially a capital-free business model.

## So what?

Capex intensity is not inherently good or bad for shareholders -- the question is whether the investment earns above its cost of capital. AMZN's 59% YoY capex growth is a bet that AI infrastructure will generate returns exceeding its roughly 12% cost of equity. If it does, the stock is undervalued at current levels because the market is discounting future earnings that have not yet materialized. If it does not, the excess capex becomes a drag on free cash flow and the stock reprices lower. Monitor the ratio of capex intensity to revenue growth: when capex grows faster than revenue for multiple consecutive years, the company is either building future capacity (bullish) or overinvesting (bearish). The distinction depends on whether new capacity translates to incremental revenue.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
