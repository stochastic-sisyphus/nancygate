
# Congressional Trading Intelligence System Setup Guide

## Overview
This system provides real-time insights into congressional trading activities, complete with automated reporting, email marketing, and social media content generation.

## Setup Instructions
1. **API Key Configuration**: Replace 'YOUR_API_KEY_HERE' in `config.json` with your actual QuiverQuant API key.
2. **Stripe Configuration**: Replace 'YOUR_STRIPE_API_KEY_HERE' in `config.json` with your actual Stripe API key.
3. **Email Settings**: Configure the email settings in `config.json` with your SMTP server details.
4. **Install Dependencies**: Run `pip install -r requirements.txt` to install all necessary packages.
5. **Run the System**: Execute `congressional_trading_system.py` to start the system.

## Features
- **Real-Time Data Fetching**: Automatically fetches and processes congressional trading data.
- **Automated Reporting**: Generates detailed PDF reports and sends them via email.
- **Social Media Automation**: Creates and logs content for social media platforms.
- **Revenue Tracking**: Integrates with Stripe for subscription management and revenue tracking.
- **Data Backup**: Regularly backs up data to ensure recovery in case of failures.

## Deployment
Ensure the system is deployed on a server with internet access and the ability to run Python scripts. Schedule the script to run at regular intervals using a task scheduler or cron job.

## Support
For support, please contact [support@example.com].
