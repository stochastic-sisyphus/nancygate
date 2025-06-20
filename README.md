# nancygate 2.0 - political intelligence analysis pipeline

a comprehensive modular system for analyzing political trading patterns, insider correlations, and market-moving signals across multiple data sources.

## overview

nancygate has evolved from a congressional trading tracker to a full political intelligence engine. the system now integrates multiple real-time data sources to identify behavioral patterns, timing anomalies, and potential market-moving events before they become public knowledge.

## key features

### core capabilities
- **multi-source data integration**: congressional trades, form 4 filings, news events, lobbying data
- **modular signal detection**: pluggable architecture for easy addition of new signal types
- **real-time enrichment**: news correlation, insider matching, volume anomaly detection
- **pattern analysis**: member networks, sector rotation, timing patterns
- **interactive dashboard**: streamlit-based visualization with real-time filtering

### signal detection modules
- **traditional signals**:
  - quick reporting (trades reported within 3 days)
  - committee sector alignment
  - unusual transaction sizes
  - options trading activity
  - cluster trading patterns
  - pre-announcement timing

- **advanced signals** (v2.0):
  - news timing correlation
  - executive parallel trades
  - volume anomalies
  - policy impact detection
  - perfect market timing
  - coordinated rings

### data enrichment
- **news integration**: asknews, tavily, serper apis for real-time event correlation
- **form 4 matching**: sec insider trading correlation with congressional trades
- **lobbying overlay**: cross-reference with active lobbying campaigns
- **market data**: price/volume validation via polygon.io

## installation

1. ensure python 3.8+ is installed
2. clone the repository
3. install dependencies:
```bash
pip install -r requirements.txt
```

4. configure api keys in `.env`:
```bash
NANCYGATE_API_KEY=your_quiverquant_key
ASKNEWS_API_KEY=your_asknews_key
TAVILY_API_KEY=your_tavily_key
SERPER_API_KEY=your_serper_key
```

## usage

### fetch congressional data
```bash
python nancygate_cli.py fetch-all --max-pages 5
```

### enrich with real-time data
```bash
python nancygate_cli.py enrich --enrich-news --enrich-form4
```

### analyze with modular signals
```bash
python nancygate_cli.py analyze --use-modular
```

### launch interactive dashboard
```bash
python nancygate_cli.py dashboard
```

the dashboard provides:
- real-time filtering by date, member, ticker, signal strength
- interactive visualizations of trading patterns
- high-signal trade alerts
- pattern analysis insights
- intelligence feed with latest signals

### quick analysis
```bash
# analyze specific ticker
python nancygate_cli.py quick-analysis --ticker NVDA

# analyze specific member
python nancygate_cli.py quick-analysis --member "Pelosi"
```

### comprehensive enrichment (v2.0)
```bash
# enrich with all political intelligence sources
python nancygate_cli.py enrich-full --enrich-all

# or select specific enrichments
python nancygate_cli.py enrich-full --enrich-lobbying --enrich-votes --enrich-market
```

the comprehensive enrichment adds:
- **lobbying data**: cross-reference trades with lobbying activity (note: opensecrets api discontinued april 2025, using alternative sources)
- **voting records**: match trades to congressional votes via propublica api
- **market validation**: price/volume analysis to detect perfect timing

## architecture

```
nancygate/
├── config/          # configuration and api keys
├── fetch/           # data fetching modules
│   ├── api_client.py
│   ├── fetcher.py
│   ├── news_enricher.py    # real-time news integration
│   └── form4_fetcher.py    # sec insider data
├── enrich/          # signal detection and analysis
│   ├── signal_engine.py
│   ├── pattern_detector.py
│   ├── advanced_signals.py
│   └── modular_signals.py  # pluggable signal system
├── export/          # output formatting
├── dashboard/       # streamlit visualization
└── data/           # local data storage
```

## modular signal system

the v2.0 architecture allows easy addition of new signal detectors:

```python
class CustomSignalDetector(SignalDetector):
    def detect(self, trades_df):
        # your detection logic
        pass
    
    def get_signal_name(self):
        return "CUSTOM_SIGNAL"
    
    def get_signal_weight(self):
        return 5

# register your detector
engine = ModularSignalEngine()
engine.register_detector(CustomSignalDetector())
```

## output formats

### export directory
- csv files with full analysis and signal scores
- excel workbooks with multiple analysis sheets:
  - summary metrics
  - all trades with signals
  - high signal trades
  - member performance
  - ticker momentum
  - sector rotation
  - insider networks
  - timing patterns

### dashboard
- web-based interface accessible at `http://localhost:8501`
- real-time filtering and visualization
- exportable charts and data

## api integrations

- **quiverquant**: congressional trading data
- **asknews**: real-time news with timestamp accuracy
- **tavily**: semantic news search and summarization
- **serper**: google search fallback for rare events
- **sec edgar**: form 4 insider trading data
- **propublica congress api**: voting records and bill tracking
- **polygon.io**: market data validation (optional)
- **yahoo finance**: fallback market data source

### api status notes:
- **opensecrets api**: discontinued april 15, 2025. alternative lobbying sources:
  - senate lobbying disclosure database
  - house lobbying disclosures
  - followthemoney.org api
  - fec api for campaign finance data

## future roadmap

- legislative vote correlation
- executive appointment tracking
- lobbying spend analysis
- esg compliance scoring
- automated alert system
- api endpoints for external integration

## troubleshooting

1. **missing api keys**: ensure all required keys are in `.env`
2. **no data found**: run `fetch-all` before analysis
3. **dashboard errors**: check streamlit is installed
4. **memory issues**: use `--max-pages` to limit data

## privacy & compliance

all data is stored locally. the system only accesses public data sources and apis. no private or material non-public information is collected or analyzed. 