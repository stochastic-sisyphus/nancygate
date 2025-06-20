# troubleshooting guide for comprehensive congressional trading data

## the problem
you need comprehensive congressional trading data (all members, not just popular ones like pelosi), but:
- quiverquant api has strict rate limits
- the data is sparse and delayed
- you need real insights from complete data

## solution 1: use firecrawl to scrape quiverquant

### setup
1. make sure firecrawl api key is in your .env:
```bash
FIRECRAWL_API_KEY=fc-df4b431fc6e64aeeb8d6b1a85927f43f
```

2. run the comprehensive fetch:
```bash
python nancygate_cli.py fetch-comprehensive --max-pages 10
```

or use the standalone script:
```bash
python run_comprehensive_fetch.py
```

### if firecrawl doesn't work
- check your internet connection
- verify the api key is valid
- try fewer pages: --max-pages 2

## solution 2: use capitol trades api

### setup
```bash
python -c "from fetch.capitol_trades_scraper import CapitolTradesScraper; from config import Settings; s = CapitolTradesScraper(Settings()); df = s.fetch_all_trades(); print(f'fetched {len(df)} trades')"
```

## solution 3: use multiple sources

combine data from:
- quiverquant (api)
- capitol trades (scraping)
- house.gov official disclosures
- senate.gov financial disclosures

## solution 4: use existing data files

you already have data in your data/ directory:
- congress_trades_complete_20250618_222410.json (5000+ trades)
- recent_trades_30days_20250618_233711.json
- other historical files

to analyze existing data:
```bash
python nancygate_cli.py analyze --input-file congress_trades_complete_20250618_222410
```

## quick fix for dashboard

1. first install missing dependencies:
```bash
pip install streamlit plotly
```

2. use existing data:
```bash
python nancygate_cli.py dashboard
```

## comprehensive data sources

### official sources (most reliable)
- house financial disclosures: https://disclosures-clerk.house.gov/
- senate financial disclosures: https://efdsearch.senate.gov/

### aggregators (easier to use)
- quiverquant: https://www.quiverquant.com/congresstrading/
- capitol trades: https://www.capitoltrades.com/trades
- unusual whales: https://unusualwhales.com/politicians
- senate stock watcher: https://senatestockwatcher.com/
- house stock watcher: https://housestockwatcher.com/

### alternative scrapers
```python
# use selenium for javascript-heavy sites
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.capitoltrades.com/trades')
# extract data from page
```

## key insights for real analysis

you need:
1. **volume**: at least 1000+ trades for statistical significance
2. **coverage**: all 535 members of congress, not just famous ones
3. **recency**: trades from last 6 months minimum
4. **detail**: ticker, amount, date, transaction type, committee assignments

## working with what you have

your existing data files have comprehensive trades. to get insights:

```bash
# analyze existing comprehensive data
python nancygate_cli.py analyze --input-file congress_trades_complete_20250618_222410

# enrich with news and form 4 data
python nancygate_cli.py enrich --input-file congress_trades_complete_20250618_222410

# generate specialized reports
python nancygate_cli.py specialized-reports --report-type all
```

## debugging api issues

1. test quiverquant connection:
```bash
python nancygate_cli.py test-connection
```

2. check rate limits:
- quiverquant: 1000 requests/hour
- if hitting limits, wait 1 hour or use firecrawl

3. verify api key:
```bash
curl "https://api.quiverquant.com/beta/bulk/congresstrading?page=1&apikey=YOUR_KEY"
```

## next steps

1. use your existing comprehensive data (5000+ trades)
2. enrich it with news and insider data
3. run full analysis with modular signals
4. generate reports for real insights

the data you need is already there - you just need to analyze it properly! 