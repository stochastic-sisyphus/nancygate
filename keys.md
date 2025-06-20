
# NancyGate API Configuration
# Congressional Trading Data
NANCYGATE_API_KEY=8e52d77555c830932c8343a44c426f6d20e876fd

# News and Search APIs
ASKNEWS_API_KEY=q3AISOrlTmcUdX1blKa~dUePJT
ASKNEWS_CLIENT_ID=ebe8726b-56b3-4d44-8965-845f4fd2f6d2
TAVILY_API_KEY=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
SERPER_API_KEY=41e31e9a95a6080ffd5521c30a71b6406ba6ee74
EXA_API_KEY=af383f63-15aa-48ff-ade4-2f974a638efd

# Market Data APIs
POLYGON_API_KEY=4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd
POLYGON_ACCESS_KEY_ID=7b6b5af0-4605-48d3-8e86-cd2ec12fd774
POLYGON_SECRET_ACCESS_KEY=4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd
POLYGON_S3_ENDPOINT=https://files.polygon.io
POLYGON_BUCKET=flatfiles

# SEC and Government APIs
SEC_API_KEY=f4dcdfa079d2991dbc3aa9ea3a014cc02e74d0765b61d4d9c2e250b699af4a15
DATA_GOV_API_KEY=v7nY2deTisoO7TyOElGexjmvDld6DndvUPgONSft

# Other APIs
JINA_API_KEY=jina_72ff43e1a71b40b4b7fd4fcbab2699d2EHnKXR7Wubdap4hWwtqzzrTynEre
FIRECRAWL_API_KEY=fc-df4b431fc6e64aeeb8d6b1a85927f43f
LINKSUP_API_KEY=cb054ecf-bb45-42df-8f21-85a0dc196653

# Environment Settings
ENVIRONMENT=development
DEBUG=True


---

quiver quant api key = 8e52d77555c830932c8343a44c426f6d20e876fd
server url : https://api.quiverquant.com

polygon.io key name "Default" , Key = 4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd , API Access Default 4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd , Accessing Flat Files (S3) Name Default , Access Key ID 7b6b5af0-4605-48d3-8e86-cd2ec12fd774 , Secret Access Key
4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd . S3 Endpoint https://files.polygon.io , Bucket flatfiles .

---
sec-api.io api key = f4dcdfa079d2991dbc3aa9ea3a014cc02e74d0765b61d4d9c2e250b699af4a15
---

Capital.com Public API (1.0.0)
Base URL: https://api-capital.backend-capital.com/
Base demo URL: https://demo-api-capital.backend-capital.com/
In order to use the endpoints a session should be launched. This can be done using the POST ​​/session endpoint.
Session is active for 10 minutes. In case your inactivity is longer than this period then an error will occur upon next request.
The API covers the full range of available instruments, licences and trading functionality.

app.linksup.so api key = cb054ecf-bb45-42df-8f21-85a0dc196653
---
asknews.app Client ID : ebe8726b-56b3-4d44-8965-845f4fd2f6d2 ,  Client Secret : q3AISOrlTmcUdX1blKa~dUePJT .

---
jina ai api key = jina_72ff43e1a71b40b4b7fd4fcbab2699d2EHnKXR7Wubdap4hWwtqzzrTynEre

---
serper api = 41e31e9a95a6080ffd5521c30a71b6406ba6ee74
---
firecrawl fc-df4b431fc6e64aeeb8d6b1a85927f43f
---
Exa: af383f63-15aa-48ff-ade4-2f974a638efd
---
tavily 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

---
api.data.gov api key = v7nY2deTisoO7TyOElGexjmvDld6DndvUPgONSft
Account Email: vanessa.beckk1@gmail.com
Account ID: 77c30d29-fa64-4a67-aff9-f56287b8e1b8

 available on Congress.gov. This repository contains information on accessing and using the Congress.gov API, as well as documentation on available endpoints.

Within the Congress.gov API, responses are returned in XML or JSON formats. An <api-root> element will be visible for responses returned in XML.

For every request, three elements are returned:

The Request element contains information about the API request itself. This includes the format and the <contentType>; this is essentially the information you might expect to see in a request header.
The Pagination element contains a count of how many total data items are contained within the response, a URL containing the next page of results; and, if the offset is greater than 1, a URL containing the previous page of results.
The Data element, the name of which changes depending on the endpoint utilized (i.e. <bills> for the bill endpoint, <amendments> for the amendment endpoint, etc.). This element contains a list of all data items returned by your API call.
Keys
An API key is required for access. Sign up for a key here.

Learn more on how you can use your API key to access the Congress.gov API on api.data.gov.

Versioning
The current version of the API is version 3 (v3). Prior versions were used by the Government Publishing Office (GPO) for its Bulk Data Repository, and other clients.

Rate Limit
The rate limit is set to 5,000 requests per hour.

Limit and Offset
By default, the API returns 20 results starting with the first record. The 20 results limit can be adjusted up to 250 results. If the limit is adjusted to be greater than 250 results, only 250 results will be returned. The offset, or the starting record, can also be adjusted to be greater than 0.

Coverage and Estimated Update Times for Congress.gov Collections
Coverage information for Congress.gov collections data in the API can be found at Coverage Dates for Congress.gov Collections on Congress.gov. This page also provides estimated update times for Congress.gov collections.

Support
Congress.gov staff will monitor and respond to any issues created in this repository, and will initiate actions, as necessary. Before creating an issue in the repository, please review existing issues and add a comment to any issues relevant to yours.

Change Management
Congress.gov staff will issue change management communication through the ChangeLog so that consumers are able to adjust accordingly. The ChangeLog will contain information on updates to the API, the impacted endpoints, and the expected production release date. Milestones are also used to tag issues with expected production release date information.

Relevant Privacy Policies
API keys and user registration follow the data.gov privacy policy. Read more here.
API content follows the Library of Congress privacy policy. Read more here.

---


To verify if the Capitol Trades API is real, examine its data sources, endpoints, and cross-check results with official disclosures.

TLDR

Check the API’s data against official congressional financial disclosures, inspect its endpoints, and look for community validation or documentation. Treat all unofficial APIs with skepticism until you’ve confirmed their provenance and accuracy.

Key Steps to Verify the Capitol Trades API

1. Source Validation
 • The most reliable data on congressional trades comes from the official Clerk of the House and Senate financial disclosure websites.
 • Download a few recent disclosures from these official sources and compare them to the API’s output for the same politicians and dates.

2. Endpoint Inspection
 • Use browser developer tools to watch the network traffic when you interact with capitoltrades.com (https://capitoltrades.com).
 • See if the API endpoints return plausible, structured data (JSON, etc.) and if the data matches what’s displayed on the site.

3. Cross-Reference with Other Sources
 • Compare the API’s data with other aggregators like Quiver Quantitative or Senate Stock Watcher.
 • Consistency across multiple sources increases confidence in the data’s authenticity.

4. Community and Documentation
 • Search for developer discussions on GitHub, Reddit, or Stack Overflow about the API.
 • If others have reverse-engineered or validated the API, you’ll often find code samples, bug reports, or warnings.

5. Transparency and Updates
 • Real, trustworthy APIs often provide update logs, data provenance, and clear documentation.
 • If the API is a black box, be extra cautious—especially if you’re using it for research or public reporting.

Systems Thinking Perspective

Think of this as a feedback loop: the API is only as trustworthy as its data sources and the transparency of its processes. If you can trace the data lineage from the API back to official government filings, you can be reasonably confident in its authenticity. If not, treat it as a potentially useful—but unverified—tool.

---

*Almost* Real-Time Intraday Stock Tracker
Data
Hey Squad! 

I've recently put together an intraday stock price tracker that collects candlestick data using Yahoo Finance API, with configurable collection intervals and market hours enforcement. While not perfectly real-time, this implementation will provide granular enough data to produce approximately the same candles as the main stream providers. This API is not meant for high-frequency collection, and is currently limited in its functionality and scope.

Contrary to many other Yahoo Finance interfaces which collect historical data, this project collects intraday price data and aggregates the data into a candle over a specified time interval. A candle is a simple data structure holding the open, high, low and closing price of a stock over a predefined interval.

CandleCollector is originally designed to work in the ESP32 ecosystem, as these devices provide a small form factor, low power, wifi-connected interface to run this repetitive and low compute task.

Your basic steps to get started are:

Clone the GitHub repo: https://github.com/melo-gonzo/CandleCollector.git

Set up config.h file with your time zone in TimeConfig

Set up config.h with the appropriate settings for market hours in StockConfig

Set desired candle collection and query interval in StockConfig

Add your WiFi credentials to credentials.h

Upload to your client of choice.

Candle data is currently only stored on device, and can be monitored through serial output. I plan to integrate an easy-to-use database soon that anyone can easily set up on their own. This will enable many more possibilities to tie this into your own algotrading frameworks.CandleCollector
A real-time stock price tracker that collects candlestick data using Yahoo Finance API, with configurable collection intervals and market hours enforcement. While not perfectly real-time, this implementation will provide granular enough data to produce approximately the same candles as the main stream providers. This API is not meant for high-frequency collection, and is currently limited in its functionality and scope.

Contrary to many other Yahoo Finance interfaces which collect historical data, this project collects intraday price data and aggregates the data into a candle over a specified time interval. A candle is a simple data structure holding the open, high, low and closing price of a stock over a predefined interval.

CandleCollector is originally designed to work in the ESP32 ecosystem, as these devices provide a small form factor, low power, wifi-connected interface to run this repetitive and low compute task.

Overview
This project implements a stock price tracking system that:

Fetches real-time stock prices from Yahoo Finance (designed to be interchangeable with other API's)
Creates time-aligned candlestick data (default 1-minuted candles starting at the beginning of each minute)
Respects market trading hours (does not query outside of trading hours)
Provides test data simulation option
Stores a configurable number of historical candles
Features
Real-time price tracking with configurable intervals
Time-synchronized candlestick creation
Market hours enforcement (configurable)
Weekend detection and handling
Automatic NTP time synchronization
Test data generation mode
Circular buffer for historical candle storage
Detailed serial output logging
A future milestone of CandleCollector is to write data to a database, which allow for more candle storage, and would be accessible from other devices. This will enable features such as integrating CandleCollector into algorithmic trading platforms, visualization services, and others. The default 1-minute candles are recommended so that longer candle time-frames can be automatically constructed by querying the buffer or database in the desired size.

Configuration
All configuration is managed through the Config class in config.h and a credentials.h file for WiFi. Key settings include:

Time Settings
TimeConfig time = {
    .timezone = "PST8PDT",    // Timezone string
    .ntpServer1 = "pool.ntp.org",
    .ntpServer2 = "time.nist.gov"
};
Stock Tracking Settings
StockConfig stock = {
    .symbol = "SPY",          // Stock symbol to track
    .useTestData = false,     // Toggle test data mode
    .updateIntervalMs = 5000, // Price update frequency (ms)
    .candleDurationSec = 60,  // Candle duration in seconds
    .maxCandles = 20,         // Maximum candles to store on device buffer
    .marketHours = {
        .startHour = 6,       // Market open hour (24hr format)
        .startMinute = 30,    // Market open minute
        .endHour = 13,        // Market close hour
        .endMinute = 0,       // Market close minute
        .enforceHours = true  // Toggle market hours enforcement
    }
};
Using test data will automatically toggle enforceHours to false.

Credentials Setup
For security reasons, WiFi credentials are stored in a separate file that is not tracked by version control.

Copy the credentials template:

cp credentials_template.h credentials.h
Edit credentials.h and add your WiFi credentials:

namespace StockTracker {
namespace Credentials {

constexpr const char* WIFI_SSID = "your_actual_ssid";
constexpr const char* WIFI_PASSWORD = "your_actual_password";

} // namespace Credentials
} // namespace StockTracker
The credentials.h file is included in .gitignore to prevent accidentally committing your credentials.

Important Notes
Market Hours:

Market hours are in local time (configured timezone)
Automatically detects and skips weekends
Disabled when using test data
Can be toggled with enforceHours setting
Test Mode:

Set useTestData = true to use simulated price data
Generates random walk prices around a base value
Ignores market hours constraints
Time Synchronization:

Requires working internet connection for NTP sync
Candlesticks align to interval boundaries
All timestamps are converted to configured timezone
Setup Instructions
Configure WiFi settings in config.h
Adjust market hours for your timezone
Set desired candle duration and update interval
Upload to client (nominally and ESP32 family board)
Monitor via Serial output (115200 baud)
Serial Output
The system provides detailed status updates via Serial, including:

Connection status
Market open/close notifications
Candlestick data (open, high, low, close)
Time synchronization status
Next market open time when market is closed
Dependencies
ESP32 Arduino Core
WiFi library
HTTPClient library
ArduinoJson library
Time library
Memory Considerations
Each candle uses approximately 32 bytes
Default configuration stores 20 candles
Adjust maxCandles based on your client's available memory
Error Handling
Failed price fetches are logged and skipped
Network disconnections are handled gracefully
Invalid/missing data points are ignored
Time sync failures prevent operation until resolved
Contributing
Create a fork of the repo, and hack away! If submitting a pull request, please insure to install pre-commit, or the PR will fail.

pip install pre-commit
pre-commit install
After this, pre-commit hooks will be run to format code.

Feel free to submit issues and pull requests for:

Additional features
Bug fixes
Documentation improvements
Configuration options
Features Needed
[] Volume tracking
[] Optional database storage (firebase)
About
A real-time stock price tracker.

Resources
 Readme
License
 MIT license
 Activity
Stars
 0 stars
Watchers
 0 watching
Forks
 0 forks
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Languages
C++
100.0%
Suggested workflows
Based on your tech stack
CMake based, multi-platform projects logo
CMake based, multi-platform projects
Build and test a CMake based project on multiple platforms.
SLSA Generic generator logo
SLSA Generic generator
Generate SLSA3 provenance for your existing release workflows
C/C++ with Make logo
C/C++ with Make
Build and test a C/C++ project using Make.
More workflows
Footer
