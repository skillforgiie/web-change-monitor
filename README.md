# Web Change Monitor

A lightweight Python tool that monitors any website for content changes
and sends an email alert the moment something shifts.

## Why this exists

Manually checking websites for updates is wasted time.
This script automates the watch — you only look when something actually changes.

## How it works

1. Fetches the target page and stores an MD5 hash of its content
2. Re-fetches on a set interval (default: every 5 minutes)
3. Compares the new hash against the stored one
4. If they differ → sends an email alert with the URL, timestamp, and hash diff
5. Updates the baseline and continues monitoring

## Setup
```bash
pip install requests
```

Edit the CONFIG block at the top of `monitor.py`:

| Variable | What it is |
|----------|------------|
| `TARGET_URL` | The page you want to monitor |
| `CHECK_INTERVAL` | Seconds between checks (300 = 5 min) |
| `ALERT_EMAIL` | Where alerts get sent |
| `SENDER_EMAIL` | Your Gmail address |
| `SENDER_PASSWORD` | Your Gmail App Password |

> For Gmail: enable 2FA → go to Google Account → Security → App Passwords → generate one for "Mail"

## Run it
```bash
python monitor.py
```

## What I learned building this

- HTTP request handling and error management with `requests`
- Hashing page content as a change detection mechanism
- Automating email alerts with `smtplib` and SMTP_SSL
- Designing a clean monitoring loop with graceful error handling

## Tech

Python · requests · hashlib · smtplib · datetime
```

---

**Step 4 — Add a `requirements.txt` file**

Create one more file in the repo called `requirements.txt` with just:
```
requests
