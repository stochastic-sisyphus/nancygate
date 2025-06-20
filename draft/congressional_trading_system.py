
import requests
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import logging
from ratelimit import limits, sleep_and_retry
import stripe

# Setup logging
logging.basicConfig(filename='/home/user/output/system.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration
CONFIG_PATH = '/home/user/config/config.json'
def load_config():
    with open(CONFIG_PATH, 'r') as config_file:
        return json.load(config_file)

config = load_config()

class CongressionalTradingIntelligenceSystem:
    def __init__(self, api_key, stripe_api_key):
        self.api_key = api_key
        self.stripe_api_key = stripe_api_key
        self.base_url = "https://api.quiverquant.com/beta/congress"
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        stripe.api_key = self.stripe_api_key

    @sleep_and_retry
    @limits(calls=60, period=60)  # Rate limiting: 60 calls per minute
    def fetch_congressional_trading_data(self):
        url = f"{self.base_url}?apiKey={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    def validate_and_clean_data(self, df):
        if df.empty:
            logging.warning("No data to validate and clean.")
            return df
        df.dropna(inplace=True)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df = df[df['amount'] > 0]
        return df

    def generate_intelligence_report(self, df):
        if df.empty:
            logging.warning("No data available for report generation.")
            return
        report = f"Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}
"
        report += f"Total Transactions: {len(df)}
"
        report += f"Top Traders: {df['representative'].value_counts().head(5)}
"
        logging.info(report)

    def calculate_performance(self, df):
        if df.empty:
            logging.warning("No data available for performance calculation.")
            return
        sp500_data = pd.DataFrame({'date': pd.date_range(start='2023-01-01', periods=100), 'value': range(100)})
        df['performance'] = df['amount'] / sp500_data['value'].mean()
        return df

    def alert_significant_trades(self, df):
        if df.empty:
            logging.warning("No data available for alerts.")
            return
        significant_trades = df[df['amount'] > 100000]
        if not significant_trades.empty:
            logging.info(f"Significant trades detected: {significant_trades}")

    def generate_pdf_report(self, df):
        if df.empty:
            logging.warning("No data available for PDF report generation.")
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Congressional Trading Report", ln=True, align='C')
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['representative']} - {row['amount']}", ln=True)
        pdf.output("/home/user/output/congressional_trading_report.pdf")
        logging.info("PDF report generated.")

    def send_email_report(self):
        sender_email = config['email']['sender']
        receiver_email = config['email']['receiver']
        subject = "Congressional Trading Insights"
        body = "Here are the latest insights from congressional trading data."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(config['email']['smtp_server'], config['email']['smtp_port']) as server:
                server.starttls()
                server.login(sender_email, config['email']['password'])
                server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

    def generate_social_media_content(self, df):
        if df.empty:
            logging.warning("No data available for social media content generation.")
            return
        content = f"Top Congressional Traders: {df['representative'].value_counts().head(3)}"
        logging.info(f"Social Media Content: {content}")

    def display_dashboard(self, df):
        if df.empty:
            logging.warning("No data available for dashboard display.")
            return
        plt.figure(figsize=(10, 6))
        df['representative'].value_counts().head(10).plot(kind='bar')
        plt.title('Top 10 Congressional Traders')
        plt.xlabel('Representative')
        plt.ylabel('Number of Trades')
        plt.show()

    def backup_data(self, df):
        if df.empty:
            logging.warning("No data available for backup.")
            return
        backup_path = '/home/user/output/congressional_trading_backup.csv'
        df.to_csv(backup_path, index=False)
        logging.info(f"Data backed up to {backup_path}")

    def setup_scheduler(self):
        self.scheduler.add_job(self.fetch_congressional_trading_data, 'interval', hours=1)
        self.scheduler.add_job(self.send_email_report, 'interval', days=1)

    def setup_payment_processing(self):
        # Example setup for Stripe payment processing
        try:
            product = stripe.Product.create(name="Congressional Trading Intelligence Subscription")
            for tier in config['pricing_tiers']:
                stripe.Price.create(product=product.id, **tier)
            logging.info(f"Stripe product and price tiers created: {product.id}")
        except Exception as e:
            logging.error(f"Error setting up payment processing: {e}")

    def run(self):
        data = self.fetch_congressional_trading_data()
        clean_data = self.validate_and_clean_data(data)
        self.generate_intelligence_report(clean_data)
        performance_data = self.calculate_performance(clean_data)
        self.alert_significant_trades(clean_data)
        self.generate_pdf_report(clean_data)
        self.generate_social_media_content(clean_data)
        self.display_dashboard(clean_data)
        self.backup_data(clean_data)

# Setup and deployment
def setup():
    print("Setup Instructions:")
    print("1. Replace 'YOUR_API_KEY_HERE' with your actual QuiverQuant API key in the config.json file.")
    print("2. Replace 'YOUR_STRIPE_API_KEY_HERE' with your actual Stripe API key in the config.json file.")
    print("3. Configure email settings in the config.json file.")
    print("4. Ensure all necessary packages are installed.")
    print("5. Run this script to start the congressional trading intelligence system.")

# Main execution
setup()
system = CongressionalTradingIntelligenceSystem(api_key=config['api_key'], stripe_api_key=config['stripe_api_key'])
system.setup_scheduler()
system.setup_payment_processing()
system.run()
