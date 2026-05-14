# DELL: Why Stitching Historical Price Data Together Is Wrong

Dell Inc went private in 2013. Dell Technologies re-IPO'd in 2018. They share the same ticker "DELL" but are different legal entities with different financials. If your data vendor stitches their price series together, your returns and analytics are wrong. Here's how entity resolution prevents this.

## Code

See [`dell-entity-resolution-prices-python.py`](dell-entity-resolution-prices-python.py)

## Output

```
=== DELL: Two Companies, One Ticker ===

  DELL INC
    Entity ID: 10408 | Valid: 1988-06-22 → 2013-10-29

  DELL TECHNOLOGIES INC
    Entity ID: 65047 | Valid: 2018-12-28 → present

=== New Dell Technologies — First Trading Days (Dec 2018) ===
      date           entity_name  close  volume
2018-12-31 DELL TECHNOLOGIES INC  48.87 5818707
2019-01-02 DELL TECHNOLOGIES INC  47.12 6108745
2019-01-03 DELL TECHNOLOGIES INC  45.13 6902591
2019-01-04 DELL TECHNOLOGIES INC  46.02 8906759
2019-01-07 DELL TECHNOLOGIES INC  46.32 4925854
2019-01-08 DELL TECHNOLOGIES INC  46.87 7286293

=== Dell Technologies — Recent (1 week) ===
      date           entity_name  close   volume
2026-05-07 DELL TECHNOLOGIES INC 230.27  4842310
2026-05-08 DELL TECHNOLOGIES INC 260.46 12046171
2026-05-11 DELL TECHNOLOGIES INC 247.04 11195114
2026-05-12 DELL TECHNOLOGIES INC 238.94  7124144
2026-05-13 DELL TECHNOLOGIES INC 243.87  4985109

=== Key Insight ===
New Dell first close: $48.87 (Dec 2018)
Current close:        $243.87

These are DIFFERENT companies. Stitching them together would be wrong.
Entity resolution prevents this — each entity has its own ID.
```

## Discussion

Dell Inc (entity 10408) and Dell Technologies (entity 65047) are legally and financially distinct companies separated by a 5-year gap where DELL traded as a private company. If you naively pull "DELL" historical data without entity resolution, you'd get a time series that jumps from Dell Inc's pre-privatization price to Dell Technologies' post-IPO price — a discontinuity that would produce fake returns and corrupt any backtest. The entity_id system ensures you're always comparing the same company's data across time.

---

Built with [xfinlink](https://xfinlink.com) -- free financial data API for US equities. No credit card, no rate limits.
