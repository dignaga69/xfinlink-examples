# AAPL vs XOM: Do Individual Stocks Have Seasonal Patterns?

SPY seasonality is well-known. But do individual stocks have their own patterns? Apple has product launch cycles (September iPhone events), Exxon has seasonal energy demand. Here's 5 years of monthly data for both.

## Code

See [`aapl-vs-xom-seasonality-python.py`](aapl-vs-xom-seasonality-python.py)

## Output

```
=== AAPL Monthly Seasonality (2021-2025, 5 complete years) ===
  Jan  avg= -0.2%  wins=20%  n=5  
  Feb  avg= -2.1%  wins=40%  n=5  ----
  Mar  avg= +1.0%  wins=60%  n=5  ++
  Apr  avg= -0.8%  wins=40%  n=5  -
  May  avg= +0.3%  wins=40%  n=5  
  Jun  avg= +4.6%  wins=80%  n=5  +++++++++
  Jul  avg= +6.7%  wins=100%  n=5  +++++++++++++
  Aug  avg= +2.4%  wins=60%  n=5  ++++
  Sep  avg= -3.3%  wins=40%  n=5  ------
  Oct  avg= +3.9%  wins=60%  n=5  +++++++
  Nov  avg= +5.4%  wins=80%  n=5  ++++++++++
  Dec  avg= -0.1%  wins=60%  n=5  

=== XOM Monthly Seasonality (2021-2025, 5 complete years) ===
  Jan  avg= +8.1%  wins=80%  n=5  ++++++++++++++++
  Feb  avg= +6.0%  wins=80%  n=5  ++++++++++++
  Mar  avg= +5.2%  wins=80%  n=5  ++++++++++
  Apr  avg= +0.9%  wins=80%  n=5  +
  May  avg= +0.2%  wins=40%  n=5  
  Jun  avg= +1.2%  wins=60%  n=5  ++
  Jul  avg= +2.2%  wins=60%  n=5  ++++
  Aug  avg= +0.6%  wins=60%  n=5  +
  Sep  avg= +0.6%  wins=40%  n=5  +
  Oct  avg= +5.5%  wins=60%  n=5  +++++++++++
  Nov  avg= -0.7%  wins=60%  n=5  -
  Dec  avg= -1.3%  wins=40%  n=5  --
```

## Discussion

The patterns are strikingly different. AAPL's best months are July (+6.7%, 100% win rate) and November (+5.4%) -- July aligns with the pre-earnings run-up and November with holiday season optimism. AAPL's worst month is September (-3.3%), which is counterintuitive given iPhone launch events -- the "buy the rumor, sell the news" effect in action. XOM's pattern is the inverse: Q1 dominance (Jan +8.1%, Feb +6.0%, Mar +5.2%) driven by winter heating demand, with Q4 weakness (Nov -0.7%, Dec -1.3%). The two stocks have essentially zero overlap in their strong months, making them natural calendar-based diversifiers.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
