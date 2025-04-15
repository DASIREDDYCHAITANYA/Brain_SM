from alerts import summarize_alerts
from textblob import TextBlob
import praw
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
x=summarize_alerts()
def send_email_report(report_text, receiver_email, sender_email, app_password):
    msg = MIMEText(report_text)
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "🧠 Reddit Sentiment Mission Report"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- Run it ---


    # Fill these in
sender_email = "cherrychaitu054@gmail.com"
receiver_email = "cherrychaitu054@gmail.com"
app_password = "eksd qakt tkvm xarn"

send_email_report(x, receiver_email, sender_email, app_password)