# Daily Content Generation Prompt

Open Claude Code in ~/Desktop/xfinlink. Paste everything below the line.

---

Generate 5 xfinlink example scripts for today.

**Context:**
- xfinlink codebase is here in ~/Desktop/xfinlink — read xfinlink/client.py for current API signatures, field names, and method parameters
- Examples repo: ~/Desktop/xfinlink-examples — manifest.json, staging/, scripts/, blog/, x-posts/
- Run all scripts from ~/Desktop/xfinlink so `import xfinlink` works with the local package

**Rules:**

1. Read ~/Desktop/xfinlink-examples/manifest.json first. Do not repeat any (category + ticker_set + methodology) combination from the last 30 days.

2. Randomly select 5 categories from this list of 20:
   momentum_screening, mean_reversion, volatility_analysis, drawdown_analysis, dividend_screening, valuation_ratios, growth_screening, profitability_analysis, earnings_quality, balance_sheet_health, sector_comparison, index_constituent_analysis, index_rebalancing, factor_construction, dcf_valuation, correlation_beta, seasonality, entity_resolution_showcase, ticker_recycling, multi_endpoint_pipeline

3. For each, generate THREE outputs:

   a. **Blog article** (markdown): SEO-friendly title that matches what someone would actually Google (e.g. "How to Screen S&P 500 Stocks by P/E Ratio in Python"), 2-3 sentence motivation, full working code with inline comments, actual output from running it, 2-3 sentence discussion of results. End with: `*Built with [xfinlink](https://xfinlink.com) — free financial data API for Python. \`pip install xfinlink\`*`. Save to ~/Desktop/xfinlink-examples/staging/success/{slug}.md

   b. **Python script** (.py): the code from the article with a header comment: `# Full write-up: https://xfinlink.com/blog/{slug}`. Save to ~/Desktop/xfinlink-examples/staging/success/{slug}.py

   c. **X post draft** (~200-280 chars): hook with the finding (not the tool), key result or 2-3 lines of code, placeholder [BLOG_LINK]. Save to ~/Desktop/xfinlink-examples/staging/success/{slug}_x.txt

4. Set API key before running: `xfl.set_api_key("xfl_91cda643688e76bd182665c64ca6aedc")`

5. Run each script from ~/Desktop/xfinlink. Capture and include the actual output in the blog article.

6. **Sanity checks after running:**
   - Revenue should be positive for non-pre-revenue companies
   - Market cap should be reasonable (not $0 or $999T)
   - Dates should be ordered correctly
   - DataFrames should not be empty

7. **Failure handling:**
   - If the error contains "xfinlink" or "XfinlinkError" or HTTP 4xx/5xx → BUG. Save script + full traceback to ~/Desktop/xfinlink-examples/staging/bugs/{slug}_bug.txt. Generate a replacement script.
   - If it's a Python error (ImportError, KeyError, etc.) → BAD_CODE. Retry once with error context. If still fails, discard and generate a replacement.
   - Target: 5 successes. Hard cap: 10 total attempts.

8. **Differentiators (soft rule):** Where the analysis naturally calls for it, leverage entity resolution (DELL, GM, FB/META) or survivorship-bias-free index data (use historical constituents via as_of parameter). Don't force it — 1-2 out of 5 is the right frequency.

9. After all 5 succeed, update ~/Desktop/xfinlink-examples/manifest.json with entries for each:
   ```json
   {
     "date": "YYYY-MM-DD",
     "category": "category_name",
     "title": "Article Title",
     "tickers": ["AAPL", "MSFT"],
     "status": "success",
     "blog_slug": "slug-name",
     "script_path": "scripts/category/slug.py"
   }
   ```

10. Print a summary at the end: which categories were selected, which succeeded, which failed (and why), and how many bugs were found.
