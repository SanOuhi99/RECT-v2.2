# scripts/health_check_with_alerts.py
import requests
import smtplib
from email.mime.text import MIMEText
import os
import sys

def send_alert(subject, message):
    """Send email alert"""
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = os.getenv('ALERT_FROM_EMAIL')
        msg['To'] = os.getenv('ALERT_TO_EMAIL')
        
        server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)
        server.quit()
        
        print("📧 Alert sent successfully")
        
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def check_service_with_alert(name, url):
    """Check service and send alert if down"""
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {name} is healthy")
            return True
        else:
            error_msg = f"{name} returned status {response.status_code}"
            print(f"❌ {error_msg}")
            send_alert(f"🚨 {name} Service Alert", error_msg)
            return False
            
    except Exception as e:
        error_msg = f"{name} is unreachable: {str(e)}"
        print(f"❌ {error_msg}")
        send_alert(f"🚨 {name} Service Down", error_msg)
        return False

def main():
    """Run health checks with alerting"""
    services = [
        ("Backend", "https://your-backend.up.railway.app/health"),
        ("Frontend", "https://your-frontend.up.railway.app"),
    ]
    
    all_healthy = True
    
    for name, url in services:
        if not check_service_with_alert(name, url):
            all_healthy = False
    
    if not all_healthy:
        sys.exit(1)

if __name__ == "__main__":
    main()