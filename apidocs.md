# api docs


---

# app.linksup.so  

Linkup API Documentation home pagelight logo
Search...



Navigation
API Reference
/search
API Reference
/search
The /search endpoint allows you to retrieve web content.

POST
/
search

Try it

cURL

Python

JavaScript

PHP

Go

Java

Copy

Ask AI
curl --request POST \
  --url https://api.linkup.so/v1/search \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "q": "What is Microsoft'\''s 2024 revenue?",
  "depth": "deep",
  "outputType": "sourcedAnswer",
  "structuredOutputSchema": "<string>",
  "includeImages": "false",
  "fromDate": "2025-01-01",
  "toDate": "2025-01-01"
}'

200

Copy

Ask AI
{
  "answer": "Microsoft's revenue for fiscal year 2024 was $245.1 billion, reflecting a 16% increase from the previous year.",
  "sources": [
    {
      "name": "Microsoft 2024 Annual Report",
      "url": "https://www.microsoft.com/investor/reports/ar24/index.html",
      "snippet": "Highlights from fiscal year 2024 compared with fiscal year 2023 included: Microsoft Cloud revenue increased 23% to $137.4 billion.\nMore broadly, we continued to see sustained revenue growth from migrations as customers turn to Azure. Azure Arc is helping customers streamline their transition, as they secure, develop, and operate workloads with Azure services anywhere. We have 36,000 Arc customers, up 90 percent year-over-year.\nWith our acquisition of Activision Blizzard King, which closed October 2023, we’ve added hundreds of millions of players to our ecosystem. We now have 20 franchises that have generated over $1 billion in lifetime revenue—from Candy Crush, Diablo, and Halo, to Warcraft, Elder Scrolls, and Gears of War.\nGrowth depends on our ability to reach new users in new markets such as frontline workers, small and medium businesses, and growth markets, as well as add value to our core product and service offerings to span AI and productivity categories such as communication, collaboration, analytics, security, and compliance. Office Commercial revenue is mainly affected by a combination of continued installed base growth and average revenue per user expansion, as well as the continued shift from Office licensed on-premises to Office 365.\nGrowth depends on our ability to reach new users, add value to our core product set with new features including AI tools, and continue to expand our product and service offerings into new markets. Office Consumer revenue is mainly affected by the percentage of customers that buy Office with their new devices and the continued shift from Office licensed on-premises to Microsoft 365 Consumer subscriptions."
    },
    {
      "name": "Microsoft's Financial Results in FY24 Q4 – AGOLUTION",
      "url": "https://agolution.com/en/microsoft/financial-reporting/2024-q4/",
      "snippet": "What did the other quarterly figures look like and how did Microsoft fare in fiscal year 2024 as a whole? Microsoft’s revenue amounted to $64.7 billion - and increased by 15%.\nWhat did the other quarterly figures look like and how did Microsoft fare in fiscal year 2024 as a whole? Microsoft’s revenue amounted to $64.7 billion - and increased by 15%.\nThe Xbox and Gaming segment recorded a remarkable jump in revenue of 61%, with the majority of this increase being due to the acquisition of Activision Blizzard King by Microsoft at the end of last year. Since then, Microsoft has owned popular video games such as “Call of Duty”, “Overwatch” and “Candy Crush”. The results for Microsoft’s fiscal year 2024 as compared to fiscal year 2023 were as follows.\nMicrosoft achieved total revenue of $245.1 billion, an increase of 16%. The operating income amounted to $109.4 billion and increased by 24%. Total net income amounted to $88.1 billion and increased by 22%. Earnings per share amounted to $11.8 - here too there was an increase of 22%. Solid fiscal year 2024: Microsoft remains one of the market leaders in the era of AI.\nThe third quarter of Microsoft’s 2024 fiscal year was again characterized by strong cloud results."
    },
    {
      "name": "Microsoft Revenue 2010-2024 | MSFT | MacroTrends",
      "url": "https://www.macrotrends.net/stocks/charts/MSFT/microsoft/revenue",
      "snippet": "Microsoft revenue for the quarter ending December 31, 2024 was $69.632B, a 12.27% increase year-over-year.\nMicrosoft annual/quarterly revenue history and growth rate from 2010 to 2024. Revenue can be defined as the amount of money a company receives from its customers in exchange for the sales of goods or services. Revenue is the top line item on an income statement from which all costs and expenses are subtracted to arrive at net income.\nMicrosoft revenue for the quarter ending December 31, 2024 was $69.632B, a 12.27% increase year-over-year.\nMicrosoft annual revenue for 2023 was $211.915B, a 6.88% increase from 2022. Microsoft annual revenue for 2022 was $198.27B, a 17.96% increase from 2021."
    },
    {
      "name": "(MSFT) Microsoft Revenue: 1992-2025 Annual Revenue - WallStreetZen",
      "url": "https://www.wallstreetzen.com/stocks/us/nasdaq/msft/revenue",
      "snippet": "Microsoft revenue was $261.80B for the trailing 12 months ending Dec 31, 2024, with 12.3% growth year over year. Quarterly revenue for the quarter (Q4 2024) ending on Dec 31, 2024 was $69.6B, up 6.2% from last quarter. For the last reported fiscal year 2024 ending Jun 30, 2024, MSFT annual revenue was $245.1B, with 15.7% growth year-over-year."
    },
    {
      "name": "FY24 Q4 - Press Releases - Investor Relations - Microsoft",
      "url": "https://www.microsoft.com/en-us/investor/earnings/fy-2024-q4/press-release-webcast",
      "snippet": "REDMOND, Wash. — July 30, 2024 — Microsoft Corp. today announced the following results for the quarter ended June 30, 2024, as compared to the corresponding period of last fiscal year: · Revenue was $64.7 billion and increased 15% (up 16% in constant currency)\nMicrosoft Corp. today announced the following results for the fiscal year ended June 30, 2024, as compared to the corresponding period of last fiscal year: · Revenue was $245.1 billion and increased 16% (up 15% in constant currency)\n· Search and news advertising revenue excluding traffic acquisition costs increased 19% Microsoft returned $8.4 billion to shareholders in the form of share repurchases and dividends in the fourth quarter of fiscal year 2024.\nThe following table reconciles our financial results for the fiscal year ended June 30, 2024, reported in accordance with generally accepted accounting principles (GAAP) to non-GAAP financial results. Additional information regarding our non-GAAP definition is provided below.\nAll information in this release is as of June 30, 2024."
    },
    {
      "name": "Microsoft: June 2024 Q4 and FY24 Results - The ITAM Review",
      "url": "https://itassetmanagement.net/2024/08/06/microsoft-year-end-financial-results/",
      "snippet": "Microsoft Corp recently announced its June 2024 Q4 and FY24 end-of-year results. Looking at the overall results across all sectors, the total revenue for Microsoft increased by 16% to a total of $245.1 billion with a ...\nMicrosoft Corp recently announced its June 2024 Q4 and FY24 end-of-year results. Looking at the overall results across all sectors, the total revenue for Microsoft increased by 16% to a total of $245.1 billion with a net income of $88.1 billion.\nMicrosoft attributes this success to both its innovation and its customers ongoing trust. According to Amy Hood, executive vice president and CFO, they had a “solid quarter, highlighted by record bookings and Microsoft quarterly cloud revenue of $36.8 billion, up 21% year-over-year”.\nThis segment, which includes Office commercial and Office consumer revenue as well as LinkedIn and Dynamics Business Solutions revenue, saw a number of increases. Commercial products and cloud revenue increased by 12% driven by Office 365 commercial revenue growth of 13%. Microsoft also saw its M365 consumer base grow to 82.5 million.\nLastly, Dynamics products and cloud services revenue increased by 16%. This is a result of a 19% increase in Dynamics 365. The Intelligent Cloud segment (Microsoft’s top segment), which includes revenue from server products and cloud services, saw an increase of 19% in constant currency."
    },
    {
      "name": "FY24 Q4 - Performance - Investor Relations - Microsoft",
      "url": "https://www.microsoft.com/en-us/investor/earnings/fy-2024-q4/performance",
      "snippet": "Revenue increased $33.2 billion or 16% driven by growth across each of our segments. Intelligent Cloud revenue increased driven by Azure. Productivity and Business Processes revenue increased driven by Office 365 Commercial.\nMore Personal Computing revenue increased driven by Gaming.\nCost of revenue increased $8.3 billion or 13% driven by growth in Microsoft Cloud and Gaming, offset in part by a decline in Devices."
    },
    {
      "name": "Microsoft (NASDAQ:MSFT) Q4 2024 Earnings Report on 7/30/2024 - MarketBeat",
      "url": "https://www.marketbeat.com/earnings/reports/2024-7-30-microsoft-co-stock/",
      "snippet": "Microsoft Q4 2024 Earnings Report $388.49-8.50 (-2.14%) As of 03/3/2025 04:00 PM Eastern. Earnings History Forecast. Microsoft EPS Results. Actual EPS $2.95. Consensus EPS $2.90. Beat/Miss Beat by +$0.05. One Year Ago EPS $2.69. Microsoft Revenue Results. Actual Revenue $64.73 billion. Expected Revenue"
    },
    {
      "name": "FY24 Q4 - Performance - Investor Relations - Microsoft",
      "url": "https://www.microsoft.com/en-us/Investor/earnings/FY-2024-Q4/performance",
      "snippet": "Fiscal Year 2024 Compared with Fiscal Year 2023. Revenue increased $33.2 billion or 16% driven by growth across each of our segments. Intelligent Cloud revenue increased driven by Azure. ... Cost of revenue increased $8.3 billion or 13% driven by growth in Microsoft Cloud and Gaming, offset in part by a decline in Devices."
    },
    {
      "name": "Microsoft 2024 Q4 Earnings: Record cloud bookings as Azure growth holds | MSDynamicsWorld.com",
      "url": "https://msdynamicsworld.com/story/microsoft-2024-q4-earnings-record-cloud-bookings-azure-growth-holds",
      "snippet": "Microsoft reported Q4 2024 financial performance today with earnings per share of $2.95 on revenue of $64.7 billion, slightly exceeding analyst estimates.\nMicrosoft Cloud quarterly revenue was $36.8 billion, up 21%. Business highlights announced by the company include: Azure and other cloud services revenue growth of 29% Dynamics products and cloud services revenue increased 16% driven by Dynamics 365 revenue growth of 19% (up 20% in constant currency) ... Full year revenue for 2024 was $245.1 billion, with earnings per share of $11.80, up 22% from 2023.\nMicrosoft reported Q4 2024 financial performance today with earnings per share of $2.95 on revenue of $64.7 billion, slightly exceeding analyst estimates.\nLast quarter, Microsoft reported earnings per share of $2.94 on revenue of $61.9 billion, exceeding analyst estimates. A year ago, Microsoft reported earnings per share of $2.69 on revenue of $56.2 billion.\nFull-year revenue in 2023 was $211.9 billion with earnings of $9.68 per share. Joining MSDynamicsWorld.com gives you free, unlimited access to news, analysis, white papers, case studies, product brochures, and more. You can also receive periodic email newsletters with the latest relevant articles and content updates. Learn more about us here ... Building Stronger Partnerships: Strategies for Enhancing Microsoft ISV and VAR Collaboration Simplified Financial Reporting in Microsoft Dynamics 365 F&SCM / AX"
    }
  ]
}
Get your API key
Create a Linkup account for free to get your API key.

The /search endpoint is a context retrieve for online content. For a natural language query, it finds online information to ground your LLM’s answer, along with sources.

Our search is optimized for precision. Make sure to craft detailed prompts for optimal results. Learn more here.
Depending on the depth parameter, results may be faster (standard) or slower but more complete (deep).

If outputType is set to structured, you may provide a JSON structuredOutputSchema to dictate the response format.

JSON formats are tricky. Learn more about structured output in our guide.
Learn more about these parameters in Concepts.

Authorizations
​
Authorization
stringheaderrequired
Bearer authentication header of the form Bearer <token>, where <token> is your auth token.

Body
application/json
​
q
stringrequired
The natural language question for which you want to retrieve context.

Example:
"What is Microsoft's 2024 revenue?"

​
depth
enum<string>required
Defines the precision of the search. standard returns results faster; deep takes longer but yields more comprehensive results.

Available options: standard, deep 
Example:
"deep"

​
outputType
enum<string>required
The type of output you want to get. Use structured for a custom-formatted response defined by structuredOutputSchema.

Available options: sourcedAnswer, searchResults, structured 
​
structuredOutputSchema
string
Required only when outputType is structured. Provide a JSON schema (as a string) representing the desired response format. The root must be of type object.

​
includeImages
boolean
Defines whether the API should include images in its results.

Example:
"false"

​
fromDate
string
The date from which the search results should be considered, in ISO 8601 format (YYYY-MM-DD).

Example:
"2025-01-01"

​
toDate
string
The date until which the search results should be considered, in ISO 8601 format (YYYY-MM-DD).

Example:
"2025-01-01"

Response
200 - application/json
Successful response

Option 1
Option 2
Option 3
When you pick searchResults for the outputType parameter, you will get a list of search results related to your query.

​
results
object[]
Option 1
Option 2

Show child attributes

Prompting Guide
/credits/balance
x
linkedin
github
discord
Powered by Mintlify
/search - Linkup API Documentation


---
# https://open-api.capital.com/#section/FAQ/How-can-I-view-more-information-about-the-API-key

"
General information
Getting started
Available functionality
Examples and collections
Changelog
Authentication
Symbology
Orders and positions
FAQ
WebSocket API
REST API
General
Session
Accounts
Trading
Trading > Рositions
Trading > Orders
Markets Info > Markets
Markets Info > Prices
Markets Info > Client Sentiment
Watchlists
redocly logoAPI docs by Redocly
Capital.com Public API (1.0.0)
The Capital.com API allows direct access to the latest version of our trading engine.

General information
Base URL: https://api-capital.backend-capital.com/
Base demo URL: https://demo-api-capital.backend-capital.com/
In order to use the endpoints a session should be launched. This can be done using the POST ​​/session endpoint.
Session is active for 10 minutes. In case your inactivity is longer than this period then an error will occur upon next request.
The API covers the full range of available instruments, licences and trading functionality.
Getting started
To use the API the following simple steps should be taken:

Create a trading account
Note that a demo account can be used.
Turn on Two-Factor Authentication (2FA)
2FA should be turned on prior to API key generation. Instruction for 2FA enabling.
Generate an API key
To generate the API key, go to Settings > API integrations > Generate new key. There you will need to enter the label of the key, set the custom password for it and an optional expiration date, enter the 2FA code and that’s it.
You are all set!
Available functionality
Market data
Receive real-time prices for the whole range of available assets with the REST and WebSocket API.
Get the price history for the whole range of assets.
Trading functionality
Open positions, set stop and limit orders, set stop loss and take profit levels.
Review and change financial account settings (trading modes, leverage sizes).
Review trades and orders history.
Examples and collections
Postman collection: https://github.com/capital-com-sv/capital-api-postman
Trading bot based on the RSI indicator values: https://github.com/capital-com-sv/api-java-samples
Changelog
November 28, 2023
Added an opportunity to adjust the balance of the Demo account using the POST /accounts/topUp endpoint
October 05, 2023
Limit of 1 request per second is set for the POST /session endpoint.
August 04, 2023
Added an opportunity to view the whole list of available markets using the GET /markets endpoint
July 04, 2023
Set maximum date range for parameters from, to, lastPeriod to 1 day for the GET /history/activity
March 23, 2022
Limit of 1000 requests per hour is set for the POST /positions and POST /workingorders in Demo.
March 16, 2022
WebSocket API endpoints added to Swagger documentation.
February 10, 2022
Release of the first version of the REST and WebSocket API.
Authentication
How to start new session?
There are 2 ways to start the session:

Using your API key, login and password details.
Using your API key, login and encrypted password details.
Using your API key, login and password details
Here you should simply use the POST /session endpoint and mention the received in the platform’s Settings API key in the X-CAP-API-KEY header, login and API key password info in the identifier and password parameters. The value of the encryptedPassword parameter should be false.

Using your API key, login and encrypted password details
First of all you should use the GET ​/session​/encryptionKey and mention the generated in the platform’s Settings API key in the X-CAP-API-KEY header. As a response you will receive the encryptionKey and timeStamp parameters;
Using the received encryptionKey and timeStamp parameters you should encrypt your API key password using the AES encryption method.
Encryption request example:

public static String encryptPassword(String encryptionKey, Long timestamp, String password) {
    try {
        byte[] input = stringToBytes(password + "|" + timestamp);
        input = Base64.encodeBase64(input);
        KeyFactory keyFactory = KeyFactory.getInstance(RSA_ALGORITHM);
        PublicKey publicKey = keyFactory.generatePublic(new X509EncodedKeySpec(Base64.decodeBase64(stringToBytes(encryptionKey))));
        Cipher cipher = Cipher.getInstance(PKCS1_PADDING_TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] output = cipher.doFinal(input);
        output = Base64.encodeBase64(output);
        return bytesToString(output);
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
Encrypted password example:

encryptionKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1dOujgcFh/9n4JLJMY4VMWZ7aRrynwKXUC9RuoC8Qu5UOeskxgZ1q5DmAXjkes77KrLfFZYEKtrp2g1TB0MBkSALiyrG+Fl52vhET9/AWRhvHuFyskWI7tEtcGIaOB1FwR0EDO9bnylTaZ+Y9sPbLVA7loAtfaX3HW/TI9JDpdmgzXZ0KrwIxdMRzPxVqQXcA8yJL1m33pvo9mOJ0AsQ8FFuy+ctjI8l/8xUhe2Hk01rpMBXDwI1lSjnvuUUDvAtacxyYVlNsnRvbrMZYp7hyimm27RtvCUXhTX2A94tDB0MFLApURrki+tvTvw5ImDPN8qOdTUzbs8hNtVwTpSxPwIDAQAB";
timestamp = 1647440528194;
password = "1111qqqq";
// Result of password encryption with the encryptionKey
encryptedPassword = "hUxWlqKRhH6thdjJnR7DvdlGE7ABkcKHrzKDGeE7kQ7nKg91sw7BpYsLDqtxihnlHN2IEmFPZ/ZmOKBAwEAw9/vjELmAZDeKsu3Q6s+Koj4wt8giE1Sxv76JjjOB/667dEeL22IFO1rwTMZ1NS5DrfeYbTfOdQgA0v5eIOS3fH8Pp/mFHodibY28X+zIaNwk6Rcb49l6aiXwM1CAtDl359qK633a+sEB9TR0/C3EaRkuGg8wAQyQ0JERaSYOZ58Dx7pw//cmvk/U5dkQlgli2l6Ts2cMhqYXCD1ZlTDA/rLfl52lgnarfari3n0uh6LicmNeWXJBF5oxj3LCruVwMA==";
Go to the POST ​/session endpoint, set true value for the encryptedPassword parameter and mention the received in the platform’s Settings API key in the X-CAP-API-KEY header, login and prior encrypted API key password info in the identifier and password parameters
After starting the session
On starting the session you will receive the CST and X-SECURITY-TOKEN parameters in the response headers. CST is an authorization token, X-SECURITY-TOKEN shows which financial account is used for the trades. These headers should be passed on subsequent requests to the API. Both tokens are valid for 10 minutes after the last use.

Symbology
Financial accounts
accountId is the ID of your financial account. Each financial account has its unique ID. To view the full list of the available financial accounts, use the GET ​​/accounts endpoint. To find out which financial account is used for trading operations in the API please go to the GET ​/session endpoint. To change the financial account use: PUT ​/session.
Epic
Epic is the name of the market pair. You can use the GET /markets{?searchTerm} endpoint to find the market pairs you are interested in. A simple market name like ‘Bitcoin’ or ‘BTC’ can be requested with the searchTerm parameter and you will receive the full list of the market pairs associated with it. The GET ​/marketnavigation endpoint can be used to obtain asset group names. These names can be used with the GET ​​/marketnavigation​/{nodeId} endpoint to view the list of assets under the corresponding group.
Watchlists
The Watchlist is the list of assets which can be seen and created on the platform. The GET /watchlists endpoint returns the existing watchlists on your account. Each watchlist has an id parameter which can be used to obtain the corresponding list of assets: GET ​/watchlists​/{watchlistId}
Orders and positions
When opening a position using the POST /positions endpoint a dealReference parameter is included in the response. However, a successful response does not always mean that the position has been successfully opened. The status of the position can be confirmed using GET ​/confirms​/{dealReference}. This will produce the status of the position together with the affectedDeals array. Note that several positions can be opened at a time: this info will be shown in the affectedDeals array.
It is important to ensure that the correct trading mode is in use with the API. To find out which trading mode is set on your financial account use the GET ​/accounts​/preferences method. The hedgingMode parameter value shows whether the hedging mode is engaged. This value can be altered using endpoint: PUT ​/accounts​/preferences.
The leverages set for trades can be obtained using the GET ​​/accounts​/preferences endpoint. To change leverages, use PUT ​​/accounts​/preferences.
Note: Stop loss and take profit values cannot be set when conducting trades with real stocks.
FAQ
Which kind of APIs do you have?
On Capital.com we suggest both REST and WebSocket API. In case of WebSocket API real-time prices updates for max 40 instruments at a time.

Do you have any limitations on your API?
Yes, we do have several limitations in our Capital.com API. Here is the list:

You have max 100 attempts per 24hrs to successfully generate API keys.
The maximum request rate is 10 per second per user.
The maximum request rate is 1 per 0.1 seconds per user when opening positions or creating orders. Otherwise the position/order requests are going to be rejected.
WebSocket session duration is 10 minutes. In order to keep the session live use the ping endpoint.
REST session is also active for 10 minutes. In case your inactivity is longer than this period then an error will occur upon next request.
POST /session endpoint limit is 1 request per second per API key.
POST /positions and POST /workingorders endpoint limit is 1000 requests per hour in the Demo account.
POST /accounts/topUp endpoint limits: 10 requests per second and 100 requests per account per day.
The balance of the Demo account cannot exceed 100000.
The WebSocket API allows subscription to a maximum of 40 instruments.
WebSocket streaming falls off when the financial account is changed with the help of the PUT​ /session endpoint.
Does your API support all the instruments?
Yes, Capital.com API supports all of the instruments which you can find on the platform.

How to start using Capital.com API?
In order to start using our Capital.com API you should first of all generate an API key in the Settings > API integrations section on the platform. Upon doing so you will be able to use this key and your account credentials to authorise for the API usage with the POST /session method.

Can I use Capital.com API on the Demo account?
Sure. In order to use your Demo account with our API you should mention the following service as Base URL: https://demo-api-capital.backend-capital.com/

How to generate an API key?
In order to generate an API Key you should log in to your account, go to the Settings > API integrations section and click on the Generate API key button.

In case your 2FA is turned off you will be asked to switch on this function to ensure safe and secure keys usage.

Next you will be presented with the Generate new key window where you will be able to name your API Key, add an API key password and set an expiration date (if needed). By default the validity of the API key is 1 year.

After that you should enter your 2FA code and wait for an API Key to be generated. Once an API Key is generated you will see an API Key itself. Please, make sure to save this data as it is shown only once.

Congratulations. You should have successfully managed to integrate our API functionality. In case you have any questions - feel free to contact us (support@capital.com). We will be glad to help you.

Which kind of API Key privileges can I have?
Currently we have only 1 type of the API Keys privileges which allows trading. No Read Only API Keys can be generated.

What does a Custom password field mean during the API key generation process?
A Custom password field allows you to generate a separate password for your API key. You should use this Custom password for the API key in order to start the session.

How can I pause or launch an API key?
In order to pause or launch an API key you can click on the Pause or Play icons next to the API key in the Settings > API integrations section. This functionality allows you to either disable or enable a key when you need to do it without deleting a key itself and re-generating a new one.

How can I view more information about the API key?
In order to view more information about the API key you have generated please click on an Eye icon next to the key in the Settings > API integrations section.

I don't see my API Key. What could have happened?
There are 2 reasons for your API Key to be deleted:

your account status has changed to either SUSPENDED or BLOCKED;
your API Key has reached an expiration date.
In all other cases your API Keys should work as expected.

I see "****" instead of my API Key. How can I find a full API Key information?
According to the existing procedure the only moment you can see your API Key is during its creation. After that it will always be masked.

In case you have lost your API Key or didn't record it, you will have to create a new one and make sure that you store a new key in a secure place.

WebSocket API
In order to start using WebSocket connect to wss://api-streaming-capital.backend-capital.com/connect.

In order to keep the connection alive, ping service at least once every 10 minutes.

More information regarding the WebSocket API requests and responses parameters can be found in the table below:

Parameter	Description
destination	The subscription destination which performs as an analogue for the request endpoint in the REST API model.
correlationId	Is set to understand for which request the message was received. Helps to track the correlation between the subscription destination and response.
cst	Access token identifying the client. Can be received upon starting the session.
Is equal to CST parameter.
securityToken	Account token or account id identifying the client's current account. Can be received upon starting the session.
Is equal to X-SECURITY-TOKEN parameter.
payload	An object which contains the data regarding the corresponding markets.
Subscribe to market data
Destination: marketData.subscribe

Subscribe to the price updates by mentioning the epics
The maximum number of epics: 40

Request message example:

{
    "destination": "marketData.subscribe",
    "correlationId": "1",
    "cst": "zvkT26****nsHKk",
    "securityToken": "g6K90****QKvCS7",
    "payload": {
        "epics": [
            "OIL_CRUDE"
        ]
    }
}
Example of the response message about successful subscription:

{
    "status": "OK",
    "destination": "marketData.subscribe",
    "correlationId": "1",
    "payload": {
        "subscriptions": {
            "OIL_CRUDE": "PROCESSED"
        }
    }
}
Example of the response message with market data updates:

{
    "status": "OK",
    "destination": "quote",
    "payload": {
        "epic": "OIL_CRUDE",
        "product": "CFD",
        "bid": 93.87,
        "bidQty": 4976.0,
        "ofr": 93.9,
        "ofrQty": 5000.0,
        "timestamp": 1660297190627
    }
}
Unsubscribe from market data
Destination: marketData.unsubscribe

Unsubscribe from the prices updates

Request message example:

{
    "destination": "marketData.unsubscribe",
    "correlationId": "2",
    "cst": "zvkT26****nsHKk",
    "securityToken": "g6K90****QKvCS7",
    "payload": {
        "epics": [
            "OIL_CRUDE"
        ]
    }
}
Example of the response message about successful unsubscription:

{
    "status": "OK",
    "destination": "marketData.unsubscribe",
    "correlationId": "2",
    "payload": {
        "subscriptions": {
            "OIL_CRUDE": "PROCESSED"
        }
    }
}
Subscribe to OHLC market data
Destination: OHLCMarketData.subscribe

Subscribe to the candlestick bars updates by mentioning the epics, resolutions and bar type

List of request payload parameters:

Parameter	Format	Required?	Description
epics	string[]	YES	The list of instruments epics

Notes:
- Max number of epics is limited to 40
resolutions	string[]	NO	The list of resolutions of requested prices

Notes:
- Default value: MINUTE
- Possible values: MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY, WEEK
type	string	NO	Type of candlesticks

Notes:
- Default value: classic
- Possible values: classic, heikin-ashi
Request message example:

{
    "destination": "OHLCMarketData.subscribe",
    "correlationId": "3",
    "cst": "zvkT26****nsHKk",
    "securityToken": "g6K90****QKvCS7",
    "payload": {
        "epics": [
            "OIL_CRUDE",
            "AAPL"
        ],
        "resolutions": [
            "MINUTE_5"
        ],
        "type": "classic"
    }
}
Example of the response message about successful subscription:

{
    "status": "OK",
    "destination": "OHLCMarketData.subscribe",
    "correlationId": "3",
    "payload": {
        "subscriptions": {
            "OIL_CRUDE:MINUTE_5:classic": "PROCESSED",
            "AAPL:MINUTE_5:classic": "PROCESSED"
        }
    }
}
Example of the response message with market data updates:

{
    "status": "OK",
    "destination": "ohlc.event",
    "payload": {
        "resolution": "MINUTE_5",
        "epic": "AAPL",
        "type": "classic",
        "priceType": "bid",
        "t": 1671714000000,
        "h": 134.95,
        "l": 134.85,
        "o": 134.86,
        "c": 134.88
    }
}
Unsubscribe from OHLC market data
Destination: OHLCMarketData.unsubscribe

Unsubscribe from candlestick bars updates for specific epics, resolutions and bar types.

The general principle is as follows: you unsubscribe from the parameter you mention in the request. In case you mention epic you unsubscribe from all of the corresponding bar types and resolutions.

List of request payload parameters:

Parameter	Format	Required?	Description
epics	string[]	YES	The list of instruments epics to be unsubscribed
resolutions	string[]	NO	The list of price resolutions to be unsubscribed

Notes:
- Default value: All possible values
- Possible values: MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY, WEEK
types	string[]	NO	Types of candlesticks to be unsubscribed

Notes:
- Default value: all possible values
- Possible values: classic, heikin-ashi
Request message example:

// Unsubscribe from candlestick bars updates of OIL_CRUDE epic with MINUTE and MINUTE_5 resolutions and heikin-ashi candlestick type
{
    "destination": "OHLCMarketData.unsubscribe",
    "correlationId": "4",
    "cst": "zvkT26****nsHKk",
    "securityToken": "g6K90****QKvCS7",
    "payload": {
        "epics": [
            "OIL_CRUDE"
        ],
        "resolutions": [
            "MINUTE",
            "MINUTE_5"
        ],
        "types": [
            "heikin-ashi"
        ]
    }
}
Example of the response message about successful unsubscription:

{
    "status": "OK",
    "destination": "OHLCMarketData.unsubscribe",
    "correlationId": "4",
    "payload": {
        "subscriptions": {
            "OIL_CRUDE:MINUTE_5:heikin-ashi": "PROCESSED",
            "OIL_CRUDE:MINUTE:heikin-ashi": "PROCESSED"
        }
    }
}
Ping the service
Destination: ping

Ping the service for keeping the connection alive

Request message example:

{
    "destination": "ping",
    "correlationId": "5",
    "cst": "zvkT26****nsHKk",
    "securityToken": "g6K90****QKvCS7"
}
Response message example:

{
    "status": "OK",
    "destination": "ping",
    "correlationId": "5",
    "payload": {}
}
REST API
Find below the list of all available REST API endpoints

General
Get server time
Test connectivity to the API and get the current server time

Authentication is not required for this endpoint

Responses
200 OK

get
/api/v1/time


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/time", Method.Get);
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
{
"serverTime": 1649259764171
}
Ping the service
Ping the service to keep a trading session alive

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token or account id identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/ping


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/ping", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
{
"status": "OK"
}
Session
Encryption key
Get the encryption key to use in order to send the API key password in an encrypted form

header Parameters
X-CAP-API-KEY	
string
Example: ENTER_GENERATED_API_KEY
The API key obtained from Settings > API Integrations page on the Capital.com trading platform

Responses
200 OK

get
/api/v1/session/encryptionKey


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/session/encryptionKey", Method.Get);
request.AddHeader("X-CAP-API-KEY", "ENTER_GENERATED_API_KEY");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
{
"encryptionKey": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxOZgr4OMjNBMKpR+fZpxrDGGwDk3eGnrI+AvRq1X+psNZEjcQ/tR7XkXfy/BzhXKsrdJO4dqwFrULg03olkhapNpo0wr3Jhr3QLPOeX7bAvgL1pkg/1/ySX4ZPZ8tYuGFXRX0v/DeMYJFFiW1NjHS2phTlmVAHy6a5VRx/GmkvBxo/Xh6L0uaIZIbxNRoU1T+4oR7eaIVKtDL5uxX518EgvpU5QNFMg03Z+e5BTczCPR7xmnpKFMsu40zdICtdylxHXBupuh9zeQ5Rbx1xc72x3emUxL4PRCTh/t0gb9mCID4/AIQqSRykY9NpfkXGJV5mBN/3ZHJanHiE2mnVTlbwIBOOBA",
"timeStamp": 1649058606014
}
Session details
Returns the user's session details

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token or account id identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/session


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/session", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
{
"clientId": "12345678",
"accountId": "12345678901234567",
"timezoneOffset": 3,
"locale": "en",
"currency": "USD",
"streamEndpoint": "wss://api-streaming-capital.backend-capital.com/"
}
Create new session
Create a trading session, obtaining session tokens for subsequent API access

Session is active for 10 minutes. In case your inactivity is longer than this period then you need to create a new session

Endpoint limit: 1 request per second

List of request body parameters:

Parameter	Format	Required?	Description
identifier	string	YES	Client login identifier
password	string	YES	API key custom password
encryptedPassword	boolean	NO	Whether the password has been encrypted.
Default value: false
header Parameters
X-CAP-API-KEY	
string
Example: ENTER_GENERATED_API_KEY
The API key obtained from Settings > API Integrations page on the Capital.com trading platform

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request
401 Unauthorized
429 Too Many Requests

post
/api/v1/session


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"identifier": "ENTER_YOUR_EMAIL",
"password": "ENTER_YOUR_PASSWORD"
}
Response samples
200400401429
Content type
text/plain
Example

Success: Session created (basic password)
Success: Session created (basic password)

Copy
{
	"accountType": "CFD",
	"accountInfo": {
        "balance": 92.89,
        "deposit": 90.38,
        "profitLoss": 2.51,
        "available": 64.66
    },
	"currencyIsoCode": "USD",
	"currencySymbol": "$",
	"currentAccountId": "12345678901234567",
	"streamingHost": "wss://api-streaming-capital.backend-capital.com/",
	"accounts": [
        {
            "accountId": "12345678901234567",
            "accountName": "USD",
            "preferred": true,
            "accountType": "CFD",
            "currency": "USD",
            "symbol": "$",
            "balance": {
                "balance": 92.89,
                "deposit": 90.38,
                "profitLoss": 2.51,
                "available": 64.66
            }
        },
        {
            "accountId": "12345678907654321",
            "accountName": "EUR",
            "preferred": false,
            "accountType": "CFD",
            "currency": "EUR",
            "symbol": "€",
            "balance": {
                "balance": 0.0,
                "deposit": 0.0,
                "profitLoss": 0.0,
                "available": 0.0
            }
        }
	],
	"clientId": "12345678",
	"timezoneOffset": 3,
	"hasActiveDemoAccounts": true,
	"hasActiveLiveAccounts": true,
	"trailingStopsEnabled": false
}
Switches active account
Switch active account

List of request body parameters:

Parameter	Format	Required?	Description
accountId	string	YES	The identifier of the account being switched to
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

put
/api/v1/session


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"accountId": "12345678907654321"
}
Response samples
200400
Content type
application/json

Copy
{
"trailingStopsEnabled": false,
"dealingEnabled": true,
"hasActiveDemoAccounts": false,
"hasActiveLiveAccounts": true
}
Log out of the current session
Log out of the current session

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

delete
/api/v1/session


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/session", Method.Delete);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
text/plain

Copy
{
    "status": "SUCCESS"
}
Accounts
All accounts
Returns a list of accounts belonging to the logged-in client

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/accounts


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/accounts", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"accounts": [
{},
{}
]
}
Account preferences
Returns account preferences, i.e. leverage settings and trading mode

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/accounts/preferences


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/accounts/preferences", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"hedgingMode": false,
"leverages": {
"SHARES": {},
"CURRENCIES": {},
"INDICES": {},
"CRYPTOCURRENCIES": {},
"COMMODITIES": {}
}
}
Update account preferences
Update account preferences

List of request body parameters:

Parameter	Format	Required?	Description
leverages	object	NO	Set new leverage values
hedgingMode	boolean	NO	Enable or disable hedging mode
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

put
/api/v1/accounts/preferences


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
Expand allCollapse all
{
"leverages": {
"SHARES": 5,
"CURRENCIES": 10,
"INDICES": 20,
"CRYPTOCURRENCIES": 2,
"COMMODITIES": 5
},
"hedgingMode": false
}
Response samples
200400
Content type
application/json

Copy
{
"status": "SUCCESS"
}
Account activity history
Returns the account activity history

All query parameters are optional for this request

The maximum possible date range between from and to parameters is 1 day. If only one of the parameters is specified (from or to), the 1-day date range will be selected by default

Possible enum values for parameters in FIQL filter:

Parameter	ENUM
source	CLOSE_OUT, DEALER, SL, SYSTEM, TP, USER
status	ACCEPTED, CREATED, EXECUTED, EXPIRED, REJECTED, MODIFIED, MODIFY_REJECT, CANCELLED, CANCEL_REJECT, UNKNOWN
type	POSITION, WORKING_ORDER, EDIT_STOP_AND_LIMIT, SWAP, SYSTEM
query Parameters
from	
string
Example: from=2022-01-17T15:09:47
Start date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter

to	
string
Example: to=2022-01-17T15:10:05
End date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter

lastPeriod	
integer
Example: lastPeriod=600
Limits the timespan in seconds through to current time (not applicable if a date range has been specified). Cannot be bigger than current Unix timestamp value. Default = 600, max = 86400

detailed	
boolean
Example: detailed=true
Indicates whether to retrieve additional details about the activity. False by default

dealId	
string
Example: dealId={{dealId}}
Get activity information for specific dealId

filter	
string
Example: filter=source!=DEALER;type!=POSITION;status==REJECTED;epic==OIL_CRUDE,GOLD
Filter activity list using FIQL. List of supported parameters: epic, source, status, type

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
400 Bad Request

get
/api/v1/history/activity


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/history/activity?from=2022-01-17T15:09:47&to=2022-01-17T15:10:05&lastPeriod=600&detailed=true&dealId={{dealId}}&filter=source!=DEALER;type!=POSITION;status==REJECTED;epic==OIL_CRUDE,GOLD", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200400
Content type
application/json
Example

Success: Filter list by date
Success: Filter list by date

Copy
Expand allCollapse all
{
"activities": [
{},
{},
{}
]
}
Account transactions history
Returns the transaction history. By default returns the transactions within the last 10 minutes

All query parameters are optional for this request

query Parameters
from	
string
Example: from=2021-08-10T00:00:00
Start date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter

to	
string
Example: to=2021-09-10T00:00:01
End date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on dateUTC parameter

lastPeriod	
integer
Example: lastPeriod=600
Limits the timespan in seconds through to current time (not applicable if a date range has been specified). Cannot be bigger than current Unix timestamp value. Default = 600

type	
string
Example: type=DEPOSIT
Transaction type. Possible values: INACTIVITY_FEE, RESERVE, VOID, UNRESERVE, WRITE_OFF_OR_CREDIT, CREDIT_FACILITY, FX_COMMISSION, COMPLAINT_SETTLEMENT, DEPOSIT, WITHDRAWAL, REFUND, WITHDRAWAL_MONEY_BACK, TRADE, SWAP, TRADE_COMMISSION, TRADE_COMMISSION_GSL, NEGATIVE_BALANCE_PROTECTION, TRADE_CORRECTION, CHARGEBACK, ADJUSTMENT, BONUS, TRANSFER, CORPORATE_ACTION, CONVERSION, REBATE, TRADE_SLIPPAGE_PROTECTION

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/history/transactions


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/history/transactions?from=2021-08-10T00:00:00&to=2021-09-10T00:00:01&lastPeriod=600&type=DEPOSIT", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json
Example

Success: Get list of transactions within last hour
Success: Get list of transactions within last hour

Copy
Expand allCollapse all
{
"transactions": [
{},
{}
]
}
Adjust balance of Demo account
Adjust the balance of the current Demo account.

Note: The balance of the Demo account cannot exceed 100000.

Limits:

10 requests per second;
100 requests per account per day.
List of request body parameters:

Parameter	Format	Required?	Description
amount	number	YES	The amount of funds that will be added to the Demo account balance

Notes:
- Min value = -400000
- Max value = 400000
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

post
/api/v1/accounts/topUp


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"amount": 1000
}
Response samples
200400
Content type
application/json

Copy
{
"successful": true
}
Trading
Position/Order confirmation
Returns a deal confirmation for the given deal reference

In case of mentioning the order prefix formed because of the position creation the opened positions IDs will be shown in the affectedDeals array

path Parameters
dealReference
required
string
Example: {{dealReference}}
Deal reference for an unconfirmed trade

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/confirms/{dealReference}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/confirms/{{dealReference}}", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"date": "2022-04-06T07:32:19.193",
"status": "OPEN",
"dealStatus": "ACCEPTED",
"epic": "SILVER",
"dealReference": "o_fcc7e6c0-c150-48aa-bf66-d6c6da071f1a",
"dealId": "006011e7-0001-54c4-0000-000080560043",
"affectedDeals": [
{}
],
"level": 24.285,
"size": 1,
"direction": "BUY",
"guaranteedStop": false,
"trailingStop": false
}
Trading > Рositions
All positions
Returns all open positions for the active account

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/positions


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/positions", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"positions": [
{},
{}
]
}
Create position
Create orders and positions

Please note that when creating the position an order is created first with the 'o_' prefix in the dealReference parameter

List of request body parameters:

Parameter	Format	Required?	Description
direction	string	YES	Deal direction

Must be BUY or SELL
epic	string	YES	Instrument epic identifier
size	number	YES	Deal size
guaranteedStop	boolean	NO	Must be true if a guaranteed stop is required

Notes:
- Default value: false
- If guaranteedStop equals true, then set stopLevel, stopDistance or stopAmount
- Cannot be set if trailingStop is true
- Cannot be set if hedgingMode is true
trailingStop	boolean	NO	Must be true if a trailing stop is required

Notes:
- Default value: false
- If trailingStop equals true, then set stopDistance
- Cannot be set if guaranteedStop is true
stopLevel	number	NO	Price level when a stop loss will be triggered
stopDistance	number	NO	Distance between current and stop loss triggering price

Notes:
- Required parameter if trailingStop is true
stopAmount	number	NO	Loss amount when a stop loss will be triggered
profitLevel	number	NO	Price level when a take profit will be triggered
profitDistance	number	NO	Distance between current and take profit triggering price
profitAmount	number	NO	Profit amount when a take profit will be triggered
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

post
/api/v1/positions


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"epic": "SILVER",
"direction": "BUY",
"size": 1,
"guaranteedStop": true,
"stopLevel": 20,
"profitLevel": 27
}
Response samples
200400
Content type
application/json
Example

Success: Create simple position
Success: Create simple position

Copy
{
"dealReference": "o_98c0de50-9cd5-4481-8d81-890c525eeb49"
}
Single position
Returns an open position for the active account by deal identifier

path Parameters
dealId
required
string
Example: {{dealId}}
Permanent deal reference for a confirmed trade

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/positions/{dealId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/positions/{{dealId}}", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"position": {
"contractSize": 1,
"createdDate": "2022-04-06T10:49:52.056",
"createdDateUTC": "2022-04-06T07:49:52.056",
"dealId": "006011e7-0001-54c4-0000-00008056005e",
"dealReference": "p_006011e7-0001-54c4-0000-00008056005e",
"workingOrderId": "006011e7-0001-54c4-0000-00008056005c",
"size": 1,
"leverage": 20,
"upl": -0.022,
"direction": "BUY",
"level": 21.059,
"currency": "USD",
"guaranteedStop": false
},
"market": {
"instrumentName": "Silver",
"expiry": "-",
"marketStatus": "TRADEABLE",
"epic": "SILVER",
"symbol": "Natural Gas",
"instrumentType": "COMMODITIES",
"lotSize": 1,
"high": 21.167,
"low": 20.823,
"percentageChange": 1.8478,
"netChange": 0.381,
"bid": 21.037,
"offer": 21.057,
"updateTime": "2022-04-06T10:53:35.389",
"updateTimeUTC": "2022-04-06T07:53:35.389",
"delayTime": 0,
"streamingPricesAvailable": true,
"scalingFactor": 1,
"marketModes": []
}
}
Update position
Update the position

List of request body parameters:

Parameter	Format	Required?	Description
guaranteedStop	boolean	NO	Must be true if a guaranteed stop is required

Notes:
- Default value: false
- If guaranteedStop equals true, then set stopLevel, stopDistance or stopAmount
- Cannot be set if trailingStop is true
- Cannot be set if hedgingMode is true
trailingStop	boolean	NO	Must be true if a trailing stop is required

Notes:
- Default value: false
- If trailingStop equals true, then set stopDistance
- Cannot be set if guaranteedStop is true
stopLevel	number	NO	Price level when a stop loss will be triggered
stopDistance	number	NO	Distance between current and stop loss triggering price

Notes:
- Required parameter if trailingStop is true
stopAmount	number	NO	Loss amount when a stop loss will be triggered
profitLevel	number	NO	Price level when a take profit will be triggered
profitDistance	number	NO	Distance between current and take profit triggering price
profitAmount	number	NO	Profit amount when a take profit will be triggered
path Parameters
dealId
required
string
Example: {{dealId}}
Permanent deal reference for a confirmed trade

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request
404 Not Found

put
/api/v1/positions/{dealId}


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"guaranteedStop": true,
"stopDistance": 3,
"profitAmount": 2
}
Response samples
200400404
Content type
application/json

Copy
{
"dealReference": "p_006011e7-0001-54c4-0000-000080560068"
}
Close position
Close the position

path Parameters
dealId
required
string
Example: {{dealId}}
Permanent deal reference for a confirmed trade

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

delete
/api/v1/positions/{dealId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/positions/{{dealId}}", Method.Delete);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
{
"dealReference": "p_006011e7-0001-54c4-0000-000080560068"
}
Trading > Orders
All working orders
Returns all open working orders for the active account

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/workingorders


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/workingorders", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"workingOrders": [
{},
{}
]
}
Create working order
Create a limit or stop order

List of request body parameters:

Parameter	Format	Required?	Description
direction	string	YES	Order direction

Must be BUY or SELL
epic	string	YES	Instrument epic identifier
size	number	YES	Order size
level	number	YES	Order price
type	string	YES	Order type

Must be LIMIT or STOP
goodTillDate	string	NO	Order cancellation date in UTC time

Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-06-09T01:01:00)
guaranteedStop	boolean	NO	Must be true if a guaranteed stop is required

Notes:
- Default value: false
- If guaranteedStop equals true, then set stopLevel, stopDistance or stopAmount
- Cannot be set if trailingStop is true
- Cannot be set if hedgingMode is true
trailingStop	boolean	NO	Must be true if a trailing stop is required

Notes:
- Default value: false
- If trailingStop equals true, then set stopDistance
- Cannot be set if guaranteedStop is true
stopLevel	number	NO	Price level when a stop loss will be triggered
stopDistance	number	NO	Distance between current and stop loss triggering price

Notes:
- Required parameter if trailingStop is true
stopAmount	number	NO	Loss amount when a stop loss will be triggered
profitLevel	number	NO	Price level when a take profit will be triggered
profitDistance	number	NO	Distance between current and take profit triggering price
profitAmount	number	NO	Profit amount when a take profit will be triggered
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

post
/api/v1/workingorders


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"epic": "SILVER",
"direction": "BUY",
"size": 1,
"level": 20,
"type": "LIMIT"
}
Response samples
200400
Content type
application/json
Example

Success: Create limit order
Success: Create limit order

Copy
{
"dealReference": "o_307bb379-6dd8-4ea7-8935-faf725f0e0a3"
}
Update working order
Update a limit or stop order

List of request body parameters:

Parameter	Format	Required?	Description
level	number	NO	Order price
goodTillDate	string	NO	Order cancellation date in UTC time

Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-06-09T01:01:00)
guaranteedStop	boolean	NO	Must be true if a guaranteed stop is required

Notes:
- Default value: false
- If guaranteedStop equals true, then set stopLevel, stopDistance or stopAmount
- Cannot be set if trailingStop is true
- Cannot be set if hedgingMode is true
trailingStop	boolean	NO	Must be true if a trailing stop is required

Notes:
- Default value: false
- If trailingStop equals true, then set stopDistance
- Cannot be set if guaranteedStop is true
stopLevel	number	NO	Price level when a stop loss will be triggered
stopDistance	number	NO	Distance between current and stop loss triggering price

Notes:
- Required parameter if trailingStop is true
stopAmount	number	NO	Loss amount when a stop loss will be triggered
profitLevel	number	NO	Price level when a take profit will be triggered
profitDistance	number	NO	Distance between current and take profit triggering price
profitAmount	number	NO	Profit amount when a take profit will be triggered
path Parameters
dealId
required
string
Example: {{dealId}}
Permanent deal reference for an order

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
404 Not Found

put
/api/v1/workingorders/{dealId}


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"goodTillDate": "2022-06-09T01:01:00",
"guaranteedStop": true,
"stopDistance": 4,
"profitDistance": 4
}
Response samples
200404
Content type
application/json

Copy
{
"dealReference": "o_56e73aad-45fe-4058-a05b-569b1a6e8ba0"
}
Delete working order
Delete a limit or stop order

path Parameters
dealId
required
string
Example: {{dealId}}
Permanent deal reference for an order

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

delete
/api/v1/workingorders/{dealId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/workingorders/{{dealId}}", Method.Delete);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
{
"dealReference": "o_38323f0c-241a-43b3-8edf-a75d2ae989a5"
}
Markets Info > Markets
All top-level market categories
Returns all top-level nodes (market categories) in the market navigation hierarchy

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/marketnavigation


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/marketnavigation", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"nodes": [
{},
{},
{}
]
}
All category sub-nodes
Returns all sub-nodes (markets) of the given node (market category) in the market navigation hierarchy

path Parameters
nodeId
required
string
Example: {{nodeId}}
Identifier of the node to browse

query Parameters
limit	
integer
Example: limit=500
The maximum number of the markets in answer. Default = 500, max = 500

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
400 Bad Request

get
/api/v1/marketnavigation/{nodeId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/marketnavigation/{{nodeId}}?limit=500", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200400
Content type
application/json
Example

Success: List of category sub-nodes
Success: List of category sub-nodes

Copy
Expand allCollapse all
{
"nodes": [
{},
{},
{},
{},
{},
{},
{}
]
}
Markets details
Returns the details of all or specific markets

If query parameters are not specified in the request, the list of all available markets will be returned

Request can include one of the query parameters: searchTerm or epics

If both searchTerm or epics parameters are specified in the request, only searchTerm will be used (due to higher priority)

query Parameters
searchTerm	
string
Example: searchTerm=silver
The term to be used in the search. Has higher priority, than 'epics' parameter meaning that in case both searchTerm and epic are mentioned only searchTerm is taken into consideration.

epics	
string
Example: epics=SILVER,NATURALGAS
The epics of the market, separated by a comma. Max number of epics is limited to 50

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
400 Bad Request

get
/api/v1/markets


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/markets?searchTerm=silver&epics=SILVER,NATURALGAS", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200400
Content type
application/json
Example

Successful response: searchTerm
Successful response: searchTerm

Copy
Expand allCollapse all
{
"markets": [
{},
{}
]
}
Single market details
Returns the details of the given market

path Parameters
epic
required
string
Example: {{epic}}
The epic of the market

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/markets/{epic}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/markets/{{epic}}", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"instrument": {
"epic": "SILVER",
"symbol": "Silver",
"expiry": "-",
"name": "Silver",
"lotSize": 1,
"type": "COMMODITIES",
"guaranteedStopAllowed": true,
"streamingPricesAvailable": true,
"currency": "USD",
"marginFactor": 10,
"marginFactorUnit": "PERCENTAGE",
"openingHours": {},
"overnightFee": {}
},
"dealingRules": {
"minStepDistance": {},
"minDealSize": {},
"maxDealSize": {},
"minSizeIncrement": {},
"minGuaranteedStopDistance": {},
"minStopOrProfitDistance": {},
"maxStopOrProfitDistance": {},
"marketOrderPreference": "AVAILABLE_DEFAULT_ON",
"trailingStopsPreference": "NOT_AVAILABLE"
},
"snapshot": {
"marketStatus": "TRADEABLE",
"netChange": -0.627,
"percentageChange": -0.27,
"updateTime": "2022-04-06T11:23:00.955",
"delayTime": 0,
"bid": 22.041,
"offer": 22.061,
"high": 22.098,
"low": 21.926,
"decimalPlacesFactor": 3,
"scalingFactor": 1,
"marketModes": []
}
}
Markets Info > Prices
Historical prices
Returns historical prices for a particular instrument

All query parameters are optional for this request

By default returns the minute prices within the last 10 minutes

path Parameters
epic
required
string
Example: {{epic}}
Instrument epic

query Parameters
resolution	
string
Example: resolution=MINUTE
Defines the resolution of requested prices. Possible values are MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY, WEEK

max	
integer
Example: max=10
The maximum number of the values in answer. Default = 10, max = 1000

from	
string
Example: from=2022-02-24T00:00:00
Start date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on snapshotTimeUTC parameter

to	
string
Example: to=2022-02-24T01:00:00
End date. Date format: YYYY-MM-DDTHH:MM:SS (e.g. 2022-04-01T01:01:00). Filtration by date based on snapshotTimeUTC parameter

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
400 Bad Request

get
/api/v1/prices/{epic}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/prices/{{epic}}?resolution=MINUTE&max=10&from=2022-02-24T00:00:00&to=2022-02-24T01:00:00", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200400
Content type
application/json
Example

Success: Default response
Success: Default response

Copy
Expand allCollapse all
{
"prices": [
{},
{},
{},
{},
{},
{},
{},
{},
{},
{}
],
"instrumentType": "COMMODITIES"
}
Markets Info > Client Sentiment
Client sentiment for markets
Returns the client sentiment for the given market

query Parameters
marketIds	
string
Example: marketIds=SILVER,NATURALGAS
Comma separated list of market identifiers

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/clientsentiment


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/clientsentiment?marketIds=SILVER,NATURALGAS", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"clientSentiments": [
{},
{}
]
}
Client sentiment for market
Returns the client sentiment for the given market

path Parameters
marketId
required
string
Example: {{marketId}}
Market identifier

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/clientsentiment/{marketId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/clientsentiment/{{marketId}}", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
{
"marketId": "SILVER",
"longPositionPercentage": 91.85,
"shortPositionPercentage": 8.15
}
Watchlists
All watchlists
Returns all watchlists belonging to the current user

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK

get
/api/v1/watchlists


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/watchlists", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"watchlists": [
{},
{}
]
}
Create watchlist
Create a watchlist

List of request body parameters:

Parameter	Format	Required?	Description
name	string	YES	Watchlist name

Min length = 1
Max length = 20
epics	array[string]	NO	List of market epics to be associated with this new watchlist
header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
400 Bad Request

post
/api/v1/watchlists


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
Expand allCollapse all
{
"epics": [
"SILVER",
"NATURALGAS"
],
"name": "Lorem"
}
Response samples
200400
Content type
application/json
Example

Success: Watchlist created
Success: Watchlist created

Copy
{
"watchlistId": "123458",
"status": "SUCCESS"
}
Single watchlist
Returns a watchlist for the given watchlist identifier

path Parameters
watchlistId
required
string
Example: {{watchlistId}}
Identifier of the watchlist

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

get
/api/v1/watchlists/{watchlistId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/watchlists/{{watchlistId}}", Method.Get);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
Expand allCollapse all
{
"markets": [
{},
{}
]
}
Add market to watchlist
Add a market to the watchlist

List of request body parameters:

Parameter	Format	Required?	Description
epic	string	YES	Instrument epic identifier
path Parameters
watchlistId
required
string
Example: {{watchlistId}}
Identifier of the watchlist

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Request Body schema: application/json
object
Responses
200 OK
404 Not Found

put
/api/v1/watchlists/{watchlistId}


Request samples
PayloadC#cURLHTTPJavaJavaScriptNodeJSPHPPython
Content type
application/json

Copy
{
"epic": "SILVER"
}
Response samples
200404
Content type
application/json

Copy
{
"status": "SUCCESS"
}
Delete watchlist
Delete the watchlist

path Parameters
watchlistId
required
string
Example: {{watchlistId}}
Identifier of the watchlist

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

delete
/api/v1/watchlists/{watchlistId}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/watchlists/{{watchlistId}}", Method.Delete);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
{
"status": "SUCCESS"
}
Remove market from watchlist
Remove a market from the watchlist

path Parameters
watchlistId
required
string
Example: {{watchlistId}}
Identifier of the watchlist

epic
required
string
Example: {{epic}}
Instrument epic identifier

header Parameters
X-SECURITY-TOKEN	
string
Example: ENTER_OBTAINED_SECURITY_TOKEN
Account token identifying the client's current account

CST	
string
Example: ENTER_OBTAINED_CST_TOKEN
Access token identifying the client

Responses
200 OK
404 Not Found

delete
/api/v1/watchlists/{watchlistId}/{epic}


Request samples
C#cURLHTTPJavaJavaScriptNodeJSPHPPython

Copy
var options = new RestClientOptions("https://api-capital.backend-capital.com")
{
  MaxTimeout = -1,
};
var client = new RestClient(options);
var request = new RestRequest("/api/v1/watchlists/{{watchlistId}}/{{epic}}", Method.Delete);
request.AddHeader("X-SECURITY-TOKEN", "ENTER_OBTAINED_SECURITY_TOKEN");
request.AddHeader("CST", "ENTER_OBTAINED_CST_TOKEN");
RestResponse response = await client.ExecuteAsync(request);
Console.WriteLine(response.Content);
Response samples
200404
Content type
application/json

Copy
{
"status": "SUCCESS"
}
"

---
---

# asknews.app
Home
API Reference

Search documentation...
⌘K
AskNews Logo Dark

🏠
Getting Started
📰
News
📖
Stories
💬
Chat
🤿
DeepNews
🔮
Forecast
🕸
Graph
🔍
Web Search
🤖
Auto Filter
🚨
Alerts
👄
Reddit
📈
Analytics
🔎
Sources
🔗
LangChain
🚦
Pricing and Rate Limiting
#
Top use-cases

Metaculus Q3/Q4 AI forecasting bot winners took home over 30k dollars by building their bots with AskNews instead of Perplexity! Metaculus in-house bots changed their bots from using Perplexity to AskNews for the Q4 tournament 🚀 Read more here

UTexas is using AskNews to improve misinformation detection by 26% compared to the previous state-of-the-art 🔎 Read more here

ProMatchups.com is using AskNews' forecaster, Voir, to make high-accuracy sports predictions for millions of users 🏈

RileyRisk has 10 analysts using AskNews to work on humanitarian aid missions and global security risk analysis 🌍

#
Data Guarantee

We guarantee that our data is of the highest quality, and we will refund you if it is not. If you find a captcha, cookie, footer, or header in any of our data, we will refund you 100% of your subscription cost for that month.

#
Overview

The AskNews SDK allows you to access a variety of news related endpoints. This includes:

📰 News: Natural language, low-latency, prompt-optimized, endpoint. Ready to be the news-context link in your LLM chain.
📖 Stories: Get the hottest topics currently circulating in the news-sphere. Track sentiment, coverage, source origin, through time. Benefit from state-of-the-art clustering and custom written stories based on human-in-the-loop editorial.
💬 Chat: News infused assistant, interact with it like any other OpenAI model.
🤿 DeepNews: Our state-of-the-art Deep Research agent. Suitable for deep analytical tasks that require planning, reflection, and on-the-fly learning. The DeepNews agent leverages deep structures in the AskNews archive, Google, and more.
🔮 Forecast: Make any news-related forecast imaginable with our in-house model, Voir, based on rich temporal context and SOTA LLMs.
🕸 Graph: Explore the largest news knowledge graph on the planet using natural language queries combined with ultra-flexible filters.
🔍 Web search: Search the web and get relevant LLM distillations in return.
🤖 Auto Filter: Auto-build AskNews filter parameters for targeted news analyses.
👄 Reddit: Search Reddit live, get fully structured and GPT-summarized results - ready to contextualize your LLM.
📈 Analytics: AskNews analytics on financial assets and politics.
🔎 Sources: Review the distribution of sources underpinning AskNews for any given period of time.
🔗 LangChain: Use AskNews as a LangChain retriever or tool.
For endpoint specific pricing and rate-limits, please head to the pricing and rate limits page.

AskNews infuses any LLM with the latest news, using a single natural language query. Specifically, AskNews is enriching over 500k articles per day, indexing them into a hot vector database, and putting that vector database on an endpoint for you. When you query AskNews, you get back a prompt-optimized string that goes directly into your prompt. This means that you do not need to manage your own news RAG, and you do not need to worry about how to properly convey news information in a condensed way to your LLM.

Grab your API key at AskNews and boost the quality of yor LLM app today.

Python (sync)
Python (async)
TypeScript
PHP
1from asknews_sdk import AskNewsSDK
2
3ask = AskNewsSDK(
4    client_id="your_client_id",
5    client_secret="your_client_secret",
6    scopes=["news"]
7)
8query = "Effect of fed policy on tech sector"
9
10# prompt-optimized string ready to go for any LLM:
11news_context = ask.news.search_news(query).as_string
#
What is AskNews doing to keep data hot and high-quality?

Building and managing a high-quality real-time news Retrieval Augmented Generation (RAG) architecture includes:

🪣 Scraping 50k news websites every 5 minutes,
🧽 Cleaning, summarizing, translating, and enriching 300k articles per day,
🧮 Embedding the articles with dense and sparse vectors,
💾 Storing the documents in an ever-growing vector database,
🔬 Monitoring for quality and ensuring up-time reliability,
🏎 Ensuring low-latency interactions to avoid slowing down your LLM application,
🧑‍🔬️ Researching and developing state of the art (SOTA) methods for entity extraction. and quality/accuracy control,
🧭 Researching and improving methods for retrieval on dense and sparse vector indices,
🌍 Tracking news narratives through time with SOTA clustering/tracking methods.
When you use AskNews, you get all this with a single line of code.

#
Performance 🏎

A quantitative benchmark was run on AskNews vs JinaAI vs Tavily vs Exa, results indicate that AskNews is 1400% faster than JinaAI, and has 78% better context precision than all competitors. The full blog + Google Colab is available here. The summary of results is shown here:

Performance

#
Research 🧑🏽‍🔬️

We researched, developed, and deployed the best entity extraction model in the world, called GLiNER News. It is currently used to extract entities for all articles and stories in the AskNews database. It is also completely open-source, in-case you'd like to run the entity extraction yourself. You can find it on our HuggingFace repository.

Our research extends beyond GLiNER, we are actively improving quality and innovating on all aspects of our system. Our full list of scientific publications can be found here.

#
Quality Guarantee 👑

This level of dedication to quality and transparency sets us apart from all other News APIs. When you consume AskNews content, you are getting only the best quality data, guaranteed. We even have our own Quality Assurance and Quality Control that runs on every single article/story to ensure that you will not run into a single article with incorrect content, scraping, etc.

#
Transparency 🔬

Much of this quality comes from our dedication to high-quality foundational software. We also developed and open-sourced Flowdapt, which is a cluster orchestration software that enables highly reactive and adaptive artificial intelligence software. This software is what powers the AskNews backend, ensuring that we can keep up with the ever-changing news landscape, without missing a single article.

Beyond these points, we are dedicated to open-source, with the majority of our software completely free and open-source. We are fully transparent about our datasources as well, with a transparency dashboard available to track and monitor the data. We are commonly invited to present on our open-source methodologies at conferences, such as GenAI Zurich. You can find all our presentations here.

#
Support

If you need help with the AskNews SDK, please join our Discord, where you can ask questions, share your projects, and connect with other AskNews users. The Discord even has a channel that lets you talk directly to the AskNews endpoints, asking for Forecasts and talking to millions of news articles. Discord

If you would like to explore the data before using the SDK, we encourage you to visit the AskNews website at https://asknews.app.

#
Academic use

We love supporting academic use-cases. If you are interested in accessing AskNews data for an academic project, please reach out to us at contact@asknews.app with a description of your project as well as contact information. In most cases, academic access to AskNews is completely free under the Limited License.

#
Quickstart

#
Install

We are going to setup an example that infuses GPT3.5 with the latest news, but you could substitute GPT3.5 with any LLM you like. First, install the sdk:

Python
TypeScript
PHP
pip install asknews
#
Quick News context in your LLM

Next, import the AskNews and OpenAI SDKs:

Python (sync)
Python (async)
TypeScript
PHP
1from asknews_sdk import AskNewsSDK
2from openai import OpenAI
3
4ask = AskNewsSDK(
5    client_id="your_client_id",
6    client_secret="your_client_secret",
7    scopes=["chat", "news", "stories"]
8)
9# requires OpenAI SDK, install it via:
10# pip install openai
11oai_client = OpenAI(api_key="")
Your AskNews client_id and client_secret can be generated by going to the AskNews console and creating an account. You create your API credentials and set them in the AskNewsSDK constructor above. The scopes parameter list is designed to help you control access to different endpoints for different credentials.

Let's take an example of your LLM interacting with a user who is asking about the current political situation in Germany. If you had your own RAG setup, you would use that query to go search a database and retrieve documents, structure them into a prompt-ready format, and it inject into your prompt. With AskNews, you treat it as a one-stop RAG shop. Here's how you would do it:

Python (sync)
Python (async)
TypeScript
PHP
1def main():
2    # Your user asks a question about the current political situation in Germany
3    user = {
4        "role": "user",
5        "content": "What is the current political situation in Germany?"
6    }
7
8    # Grab a prompt-optimized string ready to go for your LLM:
9    response = ask.news.search_news(
10        query=user["content"], # any natural language query
11        n_articles=10, # control the number of articles to include in the context
12        return_type="string",  # you can also ask for "dicts" if you want more information
13        method="nl"  # use "nl" for natural language for your search, or "kw" for keyword search
14    )
15    # now you have a prompt optimized string:
16    news_articles = response.as_string
17
18    # simply infuse that string into the prompt:
19    system = {
20        "role": "system",
21        "content": "A chat between a curious user and an artificial intelligence Assistant. "
22        "The Assistant has access to the following news articles that "
23        f"may be useful for answering the User's questions: {news_articles}"
24    }
25    response = oai_client.chat.completions.create(
26        model="gpt-3.5-turbo",
27        messages=[system, user]
28    )
29
30    print(response.choices[0].message.content)
31
32main()
Now the response provides the latest updated information about the political situation in Germany:

Response from GPT3.5

The current political situation in Germany is dynamic and multifaceted.

Internal Security Concerns: There are doubts about Germany's internal security, with increasing threats from outside and vulnerabilities within the state structure, as highlighted in debates over strengthening the Federal Constitutional Court.

Fiscal Policy: The CDU's party leader, Friedrich Merz, has raised concerns about the financial feasibility of spending 40 billion euros on citizen's income in 2024, especially in the context of maintaining defense capabilities.

Political Shifts: The SPD has been criticized for moving away from its core voter base and reviving old Russia policies. This has sparked warnings about denying reality and concerns about Germany's foreign policy post-Merkel.

Youth Political Views: A survey found that a significant portion of first-time voters lean towards conservative views, some even trusting the far-right Alternative for Germany (AfD)...(LLM response truncated for brevity)

More details about filtering and sorting your news search can be found here.

#
Getting the hottest topics in the news-sphere

If you would like to obtain the hottest tech stories in North America, you can use SDK as follows:

Python (sync)
Python (async)
TypeScript
PHP
1def get_stories():
2    response = ask.stories.search_stories(
3        categories=["Technology", "Science"],
4        continent="North America",
5        sort_by="coverage",  # sort by coverage
6        sort_type="desc",  # highest to lowest coverage
7        reddit=3,  # include 3 reddit threads
8        expand_updates=True,  # get all the details for updates
9        max_updates=2,  # get the 2 most recent updates for each story
10        max_articles=10  # include 10 news articles associated with each update
11    )
12    print([story.updates[0].headline for story in response.stories])
13
14get_stories()
Which would return the hottest tech stories in North America, sorted by coverage, with the top 3 Reddit threads, and the 2 most recent updates for each story. Each story in the response is a custom AskNews-written story about a topic that is currently circulating in the news-sphere. The story includes a host of aggregated information such as sentiment, reddit opinion, clustered articles, coverage counts, origin diversity and much more.

More details about filtering and sorting your stories search can be found here.

#
Use the News-infused Chat endpoint

If you would like to use the chat endpoint to ask questions about the news, you can use the SDK as follows:

Python (sync)
Python (async)
TypeScript
PHP
1def chat_query():
2    response = ask.chat.get_chat_completions(
3        messages=[
4            {
5                "role": "user",
6                "content": "What is the top tech news?"
7            }
8        ],
9        stream=False
10    )
11
12    # response object maches the OpenAI SDK response object:
13    print(response.choices[0].message.content)
14
15chat_query()
Beyond news, there are other endpoints like stories, chat, analytics, and sources that you can explore.

#
Additional learning material

Check out our blog post explaining how to use the AskNews SDK to infuse news into your LLM.
Table of Contents
What is AskNews doing to keep data hot and high-quality?
Performance 🏎
Research 🧑🏽‍🔬️
Quality Guarantee 👑
Transparency 🔬
Support
Academic use
Quickstart
Install
Quick News context in your LLM
Getting the hottest topics in the news-sphere
Use the News-infused Chat endpoint
Additional learning material

---
sec-api.io
SEC API by D2V
Products
Filings
Pricing
Sandbox
Docs
Tutorials
Log in
Get Free API Key
API Documentation
Introduction
Filing Query API
Full-Text Search API
Stream API
Download & PDF Generator API
XBRL-to-JSON Converter 
Extractor API 
Form ADV API - Investment Advisers
Form 3/4/5 API - Insider Trading
Form 144 API - Restricted Sales
Form 13F API - Institut. Holdings
Form 13D/13G API - Activist Invst.
Form N-PORT API - Mutual Funds
Form N-CEN API - Annual Reports
Form N-PX API - Proxy Voting
Form S-1/424B4 API - IPOs, Notes
Form C API - Crowdfunding
Form D API - Private Sec. Offerings
Form 1-A/1-K/1-Z - Reg A Offerings
Form 8-K API - Item 4.01
Form 8-K API - Item 4.02
Form 8-K API - Item 5.02
Executive Compensation API
Directors & Board Members
Audit Fees API
Company Subsidiaries
Outstanding Shares & Public Float
SEC Enforcement Actions
SEC Litigation Releases
SEC Administrative Proceedings
AAER Database API
SRO Filings Database
CIK, CUSIP, Ticker Mapping API
EDGAR Entities Database
Financial Statements
Introduction
SEC Filings API is a platform that makes EDGAR filings and SEC data accessible and analyzable to everyone.

We offer many APIs to search, stream, parse, convert and download data and filings published by the SEC:

EDGAR Filing Search & Download
Filing Query API
Full-Text Search API
Filing Stream API
Filing Download & PDF Generator API
XBRL-to-JSON Converter API
10-K/10-Q/8-K Section Extractor API
Investment Advisers
Investment Adviser & Form ADV API
Insider Trading & Institutional Ownership
Form 3, 4, 5 - Insider Trading Data
Form 144 - Restricted Sales Notifications
Form 13F - Institutional Holdings & Cover Pages
Form N-PORT - Mutual Fund & Investment Company Holdings
Form 13D/13G - Activist & Passive Investor Ownership
Investment Companies
Form N-CEN - Annual Reports by Investment Companies
Form N-PX - Proxy Voting Records
Public & Private Offerings
Form S-1/424B4 - Registration Statements & Prospectuses for IPOs, Debt & Rights Offerings, etc.
Form C - Crowdfunding Offerings
Form D - Private Placements & Exempt Offerings
Form 1-A/1-K/1-Z - Regulation A Offering Statements
Structured Material Event Data from Form 8-K
Changes in Auditors & Accountants, and Reporting of Accounting Disagreements (Item 4.01)
Financial Restatements & Non-Reliance on Prior Financial Results (Item 4.02)
Changes in Directors, Officers and Compensation Plans (Item 5.02)
Public Company Data
Executive Compensation Data
Directors & Board Members
Audit Fees Data
Company Subsidiaries
Outstanding Shares & Public Float
Enforcement Actions & SRO Filings
SEC Enforcement Actions
SEC Litigation Releases
SEC Administrative Proceedings
Accounting & Auditing Enforcement Releases (AAERs)
SRO Filings
Other APIs
CIK, Ticker, CUSIP Mapping API
EDGAR Entities Database
We provide a petabyte-scale repository of all EDGAR filings and exhibits published by the SEC since 1993. Our platform includes over 800,000 EDGAR filers, 18 million filings, and more than 800 filing types, with new filings becoming available immediately upon release. All EDGAR filing entities are covered, including public companies, insiders, mutual funds, broker-dealers, asset-backed securities, business development companies, and more.

Filing Query API
The Query API allows you to search and filter all 18+ million filings and exhibits published on SEC EDGAR since 1993. The API accepts simple and complex filter expressions and returns filings in JSON format including all meta data, filer information, filing attachments, all URLs to the original SEC source, and many more. 13F holding information is also fully supported. The API supports over 20 search parameters, such as filer ticker symbols, CIKs, industries, filing types, SICs and many more.

Find more details in the documentation here.

Full-Text API
The Full-Text Search API is used to search the content of SEC filings and all filing attachments, such as exhibits. Single keyword search is supported as well as complex phrase search with boolean operators. The API returns filings and any other files including the search terms. The result is returned in JSON format.

Find more details in the documentation here.

Filing Stream API
The Stream API offers a live, real-time feed of newly published filings from the SEC EDGAR database, delivering these filings directly to your connected client the moment they are released.

This API utilizes push-based WebSocket technology for immediate data transmission. Upon establishing a connection, your client will start receiving updates on new filings in JSON format. The API is compatible with a wide range of programming languages and frameworks, including Python, Node.js, Java, C, C#, C++, Go, and React, among others that support WebSocket clients.

For additional information and tutorials, please refer to our documentation here.

10-K/10-Q/8-K Section Extractor API
The Extractor API returns any section item from 10-Q, 10-K and 8-K filings, in cleaned and standardized text or HTML. You can programmatically extract one or multiple items from any 10-Q, 10-K and 8-K filing. An item is returned as clear-text or standardized HTML.

The API supports all 10-K form types including old fashioned TXT versions filed prior to 2003. Supported types include: 10-K/A, 10-KT/A, 10KSB, 10KSB/A, 10KT405, 10KT405/A, 10KSB40, 10KSB40/A, 10-K405, 10-K405/A, 10KSB, 10KSB.

Find more details in the documentation here.

XBRL-to-JSON Converter API
The XBRL-to-JSON Converter API parses, converts and standardizes any 10-K and 10-Q XBRL data into JSON format. All financial statements and all US GAAP elements can be accessed:

Income statement (consolidated statement of operations)
Balance sheet (consolidated statement of balance sheets)
Cash flow statement (consolidated statement of cash flows)
And more.
Find more details in the documentation here.

Filing Download & Render API
Use the Filing Download & Render API to download any filing, exhibit or any other attached file such as graphics, XML, XSD or TXT. The API returns the original data of the requested file or generates a PDF version.

Find more details in the documentation here.

Form ADV Investment Adviser API
The Investment Adviser & Form ADV API provides access to all current and historical Form ADV filings published by SEC- and state-registered investment advisor firms, as well as individual and exempt reporting advisers. The database goes back to the year 2000, covers more than 400,000 advisors, and includes the main filing content as well as Schedule A, Schedule B, and Schedule D.

Find more details in the documentation here.

Form 3/4/5 Insider Trading API
Accessing and searching insider trades as reported on Form 3, Form 4 and Form 5 is possible with the Insider Trading API. The API enables searching and retrieving the complete history of Form 3/4/5 filings in standardized JSON format. All derivative and non-derivative transactions as well as footnotes are included and any form parameter is searchable.

Find more details in the documentation here.

Form 13F Institutional Ownership API
Portfolio holdings of institutional investment managers as disclosed in quarterly Form 13F filings are available through the 13F Institutional Ownership API. The API returns all portfolio holding information, such as the CUSIP, ticker, number of shares held, dollar value of each position in the portfolio, and more per fund, in standardized JSON format.

Find more details in the documentation here.

Form 13D/13G Ownership Reports API
Standardized JSON-formatted content of Form 13D and Form 13G filings is available through the Form 13D/13G Ownership Reports API. The API provides access to all beneficial ownership reports filed by institutional investors, hedge funds, and other major shareholders, including the name of the issuer, the type of security, the date of the event, the total amount of securities beneficially owned, and more.

Find more details in the documentation here.

Form C Crowdfunding API
The API provides access to crowdfunding offerings as disclosed in Form C filings. All Form C filings are made available in standardized JSON format, including the issuer's background, offering amounts, and financial metrics, and more.

Find more details in the documentation here.

Form D Private Security Offering API
The API provides access to private capital offerings as disclosed in Form D filings. All Form D filings are made available in standardized JSON format, including the issuer, the type of security offered, the date of first sale, the total offering amount, and more.

Find more details in the documentation here.

CIK/CUSIP/Ticker Mapping API
The CIK/CUSIP/Ticker Mapping API maps a given CIK, ticker or CUSIP to its corresponding entity, including its ticker, CUSIP, CIK and company name, and provides a list of all stocks (listed and delisted) traded on U.S. exchanges, such as NYSE, NASDAQ, and AMEX.

Find more details in the documentation here.

Footer
Products
EDGAR Filing Search API
Full-Text Search API
Real-Time Filing Stream API
Filing Download & PDF Generator API
XBRL-to-JSON Converter
10-K/10-Q/8-K Item Extractor
Investment Adviser & Form ADV API
Insider Trading Data - Form 3, 4, 5
Restricted Sales Notifications - Form 144
Institutional Holdings - Form 13F
Form N-PORT API - Investment Company Holdings
Form N-CEN API - Annual Reports by Investment Companies
Form N-PX API - Proxy Voting Records
Form 13D/13G API
Form S-1/424B4 - IPOs, Debt & Rights Offerings
Form C - Crowdfunding Offerings
Form D - Private Placements & Exempt Offerings
Regulation A Offering Statements API
Changes in Auditors & Accountants
Non-Reliance on Prior Financial Statements
Executive Compensation Data API
Audit Fees Data API
Directors & Board Members Data
Company Subsidiaries Database
Outstanding Shares & Public Float
SEC Enforcement Actions
Accounting & Auditing Enforcement Releases (AAERs)
SRO Filings
CIK, CUSIP, Ticker Mapping
General
Pricing
Features
Supported Filings
EDGAR Filing Statistics
Account
Sign Up - Start Free Trial
Log In
Forgot Password
Developers
API Sandbox
Documentation
Resources & Tutorials
Python API SDK
Node.js API SDK
Legal
Terms of Service
Privacy Policy

SEC API

© 2025 sec-api.io by Data2Value GmbH. All rights reserved.

SEC® and EDGAR® are registered trademarks of the U.S. Securities and Exchange Commission (SEC).

EDGAR is the Electronic Data Gathering, Analysis, and Retrieval system operated by the SEC.

sec-api.io and Data2Value GmbH are independent of, and not affiliated with, sponsored by, or endorsed by the U.S. Securities and Exchange Commission.

sec-api.io is classified under SIC code 7375 (Information Retrieval Services), providing on-demand access to structured data and online information services.

