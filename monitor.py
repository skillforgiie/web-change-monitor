import hashlib
import time
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText

# ── CONFIG ──────────────────────────────────────────────
TARGET_URL     = "https://example.com"   # URL to monitor
CHECK_INTERVAL = 300                     # seconds between checks (300 = 5 min)
ALERT_EMAIL    = "you@gmail.com"         # where to send alerts
SENDER_EMAIL   = "you@gmail.com"         # Gmail sender
SENDER_PASSWORD = "your-app-password"   # Gmail App Password (not your real password)
# ────────────────────────────────────────────────────────


def fetch_page(url):
    """Fetch page content and return it as a string."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[{timestamp()}] ERROR fetching page: {e}")
        return None


def hash_content(content):
    """Return an MD5 hash of the page content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def send_alert(url, previous_hash, new_hash):
    """Send an email alert when a change is detected."""
    subject = f"[Monitor Alert] Change detected: {url}"
    body = (
        f"A change was detected on the monitored page.\n\n"
        f"URL: {url}\n"
        f"Time: {timestamp()}\n\n"
        f"Previous hash: {previous_hash}\n"
        f"New hash:      {new_hash}\n\n"
        f"Visit the page to review the change."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = ALERT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, ALERT_EMAIL, msg.as_string())
        print(f"[{timestamp()}] Alert sent to {ALERT_EMAIL}")
    except Exception as e:
        print(f"[{timestamp()}] ERROR sending alert: {e}")


def timestamp():
    """Return current time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run():
    """Main monitoring loop."""
    print(f"[{timestamp()}] Starting monitor for: {TARGET_URL}")
    print(f"[{timestamp()}] Check interval: {CHECK_INTERVAL}s\n")

    content = fetch_page(TARGET_URL)
    if not content:
        print("Could not reach target URL. Check the URL and your connection.")
        return

    current_hash = hash_content(content)
    print(f"[{timestamp()}] Baseline captured. Hash: {current_hash}\n")

    while True:
        time.sleep(CHECK_INTERVAL)
        print(f"[{timestamp()}] Checking...")

        new_content = fetch_page(TARGET_URL)
        if not new_content:
            continue

        new_hash = hash_content(new_content)

        if new_hash != current_hash:
            print(f"[{timestamp()}] CHANGE DETECTED")
            send_alert(TARGET_URL, current_hash, new_hash)
            current_hash = new_hash
        else:
            print(f"[{timestamp()}] No change. Hash: {new_hash}")


if __name__ == "__main__":
    run()
