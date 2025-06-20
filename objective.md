quiver quant api key = 8e52d77555c830932c8343a44c426f6d20e876fd
server url : https://api.quiverquant.com

---
| **Step**                      | **What it is**          | **What you need**                   | **What you do**                                                                    | **What you get**                | **What you create**                                  | **What to tell them**                                     |
| ----------------------------- | ----------------------- | ----------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| **1. Project Setup**          | Environment to work in  | IDE (e.g., VS Code), terminal       | Create new folder, init Python env (`venv`)                                        | Clean workspace                 | `/nancygate-api-fetch/` project dir                  | "Local Python environment initialized for API project."   |
| **2. API Auth Setup**         | Store and use API key   | API key, `.env` file                | Create `.env`, add `API_KEY=value`, load with `os.environ` or `dotenv`             | Secure key access               | `.env` file (not committed)                          | "API key stored securely, loaded from `.env`."            |
| **3. Test API Connection**    | Ensure the API works    | Endpoint URL, auth headers          | Send basic test GET request                                                        | JSON response (200 OK)          | `test_response.json` (optional)                      | "API responsive and returning expected data."             |
| **4. Fetch Full Dataset**     | Get all raw data        | Full API URL, query params (if any) | Paginate if needed, loop through results                                           | Complete JSON dataset           | `raw_response.json` or directly to DF                | "Full insider trading dataset pulled via API."            |
| **5. Normalize Data**         | Flatten JSON → tabular  | Python (pandas), nested fields      | Extract relevant fields, flatten nested parts (e.g., `description`, `transaction`) | Clean tabular structure         | `trades_df`                                          | "Raw data normalized to flat dataframe."                  |
| **6. Clean + Transform**      | Format + enrich data    | pandas                              | Convert dates, amounts; extract info from text (`options`, `type`, `position`)     | Clean, analysis-ready dataframe | `cleaned_trades.csv`                                 | "Data cleaned and enriched with derived variables."       |
| **7. Save CSVs**              | Deliverable format      | pandas `.to_csv()`                  | Export to file(s)                                                                  | CSV output                      | `insider_trades_raw.csv`, `insider_trades_clean.csv` | "CSV outputs are ready for Excel or pivot use."           |
| **8. Optional: Preview Tool** | Quick inspection/filter | Google Sheets or Streamlit          | Upload/share or build quick filter UI                                              | Preview dashboard               | `insider_dashboard.ipynb` or Sheets link             | "You can interactively filter the dataset here."          |
| **9. Log Time**               | For invoicing           | Start/end timestamps                | Record hours worked per task                                                       | Time log                        | `work_log.txt` or `invoice_template.xlsx`            | "Here's the breakdown of hours and tasks for billing."    |
| **10. Deliver**               | Final handoff           | All outputs + log                   | Bundle CSVs, readme, time log                                                      | Client-ready deliverable        | Folder or ZIP: `nancygate_deliverables/`             | "All files delivered: raw + clean CSVs, work log, notes." |



Absolutely. Here's your **structured, step-by-step cheat sheet** for the NancyGate API pipeline:

---

# 📈 Insider Trading API Workflow Cheat Sheet

| **Step**                      | **What it is**          | **What you need**                   | **What you do**                                                                    | **What you get**                | **What you create**                                  | **What to tell them**                                     |
| ----------------------------- | ----------------------- | ----------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| **1. Project Setup**          | Environment to work in  | IDE (e.g., VS Code), terminal       | Create new folder, init Python env (`venv`)                                        | Clean workspace                 | `/nancygate-api-fetch/` project dir                  | "Local Python environment initialized for API project."   |
| **2. API Auth Setup**         | Store and use API key   | API key, `.env` file                | Create `.env`, add `API_KEY=value`, load with `os.environ` or `dotenv`             | Secure key access               | `.env` file (not committed)                          | "API key stored securely, loaded from `.env`."            |
| **3. Test API Connection**    | Ensure the API works    | Endpoint URL, auth headers          | Send basic test GET request                                                        | JSON response (200 OK)          | `test_response.json` (optional)                      | "API responsive and returning expected data."             |
| **4. Fetch Full Dataset**     | Get all raw data        | Full API URL, query params (if any) | Paginate if needed, loop through results                                           | Complete JSON dataset           | `raw_response.json` or directly to DF                | "Full insider trading dataset pulled via API."            |
| **5. Normalize Data**         | Flatten JSON → tabular  | Python (pandas), nested fields      | Extract relevant fields, flatten nested parts (e.g., `description`, `transaction`) | Clean tabular structure         | `trades_df`                                          | "Raw data normalized to flat dataframe."                  |
| **6. Clean + Transform**      | Format + enrich data    | pandas                              | Convert dates, amounts; extract info from text (`options`, `type`, `position`)     | Clean, analysis-ready dataframe | `cleaned_trades.csv`                                 | "Data cleaned and enriched with derived variables."       |
| **7. Save CSVs**              | Deliverable format      | pandas `.to_csv()`                  | Export to file(s)                                                                  | CSV output                      | `insider_trades_raw.csv`, `insider_trades_clean.csv` | "CSV outputs are ready for Excel or pivot use."           |
| **8. Optional: Preview Tool** | Quick inspection/filter | Google Sheets or Streamlit          | Upload/share or build quick filter UI                                              | Preview dashboard               | `insider_dashboard.ipynb` or Sheets link             | "You can interactively filter the dataset here."          |
| **9. Log Time**               | For invoicing           | Start/end timestamps                | Record hours worked per task                                                       | Time log                        | `work_log.txt` or `invoice_template.xlsx`            | "Here's the breakdown of hours and tasks for billing."    |
| **10. Deliver**               | Final handoff           | All outputs + log                   | Bundle CSVs, readme, time log                                                      | Client-ready deliverable        | Folder or ZIP: `nancygate_deliverables/`             | "All files delivered: raw + clean CSVs, work log, notes." |



---

security: Storing API Key• Save the API key in a .env file:iniCopyEditNANCYGATE_API_KEY=your_key_here• Load it using os.environ or dotenv when calling the API3. Calling the API• Use the API docs or inspect an example endpoint• Start with a basic GET request• Ensure the response is:• Status code 200• JSON• Includes all expected fields (e.g., ticker, date, transaction type, amount, legislator)4. Parse the Response• Convert the JSON into a flat structure (each trade = one row)• Normalize nested objects (e.g., descriptions, filings, names) if necessary• Remove duplicates or null rows if they exist5. Save as CSV• Export to: insider_trades_raw.csv• Use a clean, normalized column format:• name, ticker, trade_type, amount, transaction_date, report_date, description, option_type, etc.• Confirm CSV opens cleanly in Excel and Google Sheets6. Make It Digestible• If needed, create a filtered/pivot-ready version:• Convert string amounts to floats• Format dates cleanly• Create simple derived columns:• is_option_trade = True/False• option_position = call/put/exercise/none• position_direction = long/short/unknown7. Deliverables insider_trades_raw.csv (Optional) insider_trades_clean.csv Hour log (record exact time spent) Short README or bullet summary for the team (see below)


---
Setup
 Local nancygate/ folder already I madre it we are in it✅
 Subfolders general guide:
fetch/, enrich/, export/, data and way to view and filter sort, config/ ✅
u must create algorithm to get meaning and most powerful combos that actually can learn from the trades 
 API key config will go in config ✅
🔹 Prioritization
✅ Export Formats: CSV and Excel
✅ Signal Flags:
 Trade reported < 3 days after execution
 Member trades in own committee's sector
 Timing around earnings dates
🔹  Action Needed From You Right Now.
generate:
all scripts
Modular CLI/data pipeline
Flagging engine
CSV+Excel output formatters

---

not just a script, but a full modular pipeline.

---

## 💥 NancyGate Pipeline – Real Version

### 🔻 **SYSTEM STRUCTURE**

#### `nancygate_pipeline/`

```
├── fetch/
│   ├── quiver_api.py              # Batch pulls from QuiverQuant
│   └── ticker_sector_mapper.py    # Maps tickers to sectors
├── enrich/
│   └── committees.py              # Auto maps politicians → committee data
├── export/
│   ├── format_csv.py              # Writes filtered + pivotable CSV
│   └── export_to_sheets.py        # Optional GSheet sync
├── dashboard/
│   └── app.py                     # Streamlit app for trade exploration
├── config/
│   └── keys.toml                  # API keys + config values
└── nancygate_runner.py            # Main CLI launcher
```

---

## 🧠 What It Actually Does

### ✅ 1. **Batch Fetches from QuiverQuant**

* All trades, Pelosi-only, by ticker, by date range
* Automatically saves JSON + DataFrame
* Deduplicates + merges daily if rerun

### ✅ 2. **Auto-Enriches the Data**

* Pulls real-time politician → committee mapping

  * Source: [House](https://clerk.house.gov) + [Senate](https://www.senate.gov)
* Maps tickers → sectors using Yahoo Finance fallback

  * Optional: OpenFIGI fallback
* Calculates:

  * Implied position (Long/Short/Call/Put)
  * Trade lag (report vs execution)
  * Estimated trade value midpoint

### ✅ 3. **Exports Ready-to-Pivot CSV**

* Filterable by:

  * Politician
  * Ticker
  * Sector
  * Amount
  * Position
  * Committee

### ✅ 4. **Interactive data 

* Timeline of trades by politician
* Ticker frequency heatmap
* Filter by sector, party, committee, dollar value
* Pelosi ≠ only option, but she can be default

---

## What You Need to Do 

1. I have QuiverQuant API key
2. CSV
3. list of tickers, reps, or committees that are best to prioritize and algorithm that shows 

addition want trade signal logic included

---


* Build the full folder structure
* Generate Eda and scripts
*  auto-mapping + enrichment logic
build it fully

