import requests
from plyer import notification
import schedule
import time
import smtplib
from email.mime.text import MIMEText
import csv
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env



# ------------------------------
# CONFIG
# ------------------------------
WEBSITES = [
    "https://www.google.com",
    "https://www.example.com",
    "https://www.github.com"
]

EMAIL_SENDER = "tloutumelo676@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "220128591@student.uj.ac.za"
LOG_FILE = "website_status_log.csv"

# ------------------------------
# FUNCTIONS
# ------------------------------

def check_website(site):
    """
    Check a single website's status.
    Returns True if up, False otherwise along with status/error.
    """
    try:
        response = requests.get(site, timeout=5)
        if response.status_code == 200:
            print(f"{site} is UP ✅")
            return True, None
        else:
            print(f"{site} is DOWN ❌ Status Code: {response.status_code}")
            return False, response.status_code
    except requests.RequestException as e:
        print(f"{site} is DOWN ❌ Error: {e}")
        return False, str(e)

def send_desktop_notification(site, error):
    """
    Send a desktop notification if website is down.
    """
    notification.notify(
        title="Website Down Alert!",
        message=f"{site} is down! Error: {error}",
        timeout=10
    )

def send_email_notification(site, error):
    """
    Send an email if website is down.
    """
    msg = MIMEText(f"{site} is down! Error: {error}")
    msg['Subject'] = f"Website Down Alert: {site}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent for {site}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def log_status(site, status, error=None):
    """
    Log website status to CSV with timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, site, status, error])

def monitor_websites():
    """
    Check all websites and handle notifications + logging.
    """
    for site in WEBSITES:
        is_up, error = check_website(site)
        if is_up:
            log_status(site, "UP")
        else:
            log_status(site, "DOWN", error)
            send_desktop_notification(site, error)
            send_email_notification(site, error)

# ------------------------------
# INITIALIZE CSV LOG
# ------------------------------
def initialize_log():
    try:
        with open(LOG_FILE, mode='x', newline='') as file:  # 'x' creates a new file, fails if exists
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Website", "Status", "Error"])
    except FileExistsError:
        pass  # File already exists, no need to create

# ------------------------------
# SCHEDULER
# ------------------------------

initialize_log()
schedule.every(10).minutes.do(monitor_websites)

print("Website Status Checker Running...")
while True:
    schedule.run_pending()
    time.sleep(1)
