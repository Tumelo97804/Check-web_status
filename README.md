# Website Status Checker

A Python script that monitors the uptime of websites and notifies you if any go down. It logs status to a CSV file, sends desktop notifications, and emails alerts when a website is unavailable.

---

## Features

- Monitor multiple websites.
- Send **desktop notifications** when a website is down.
- Send **email notifications** using Gmail.
- Log website status and errors to a CSV file.
- Configurable monitoring interval with the `schedule` library.

---

## Requirements

- Python 3.7+
- Libraries:
  ```bash
  pip install requests plyer schedule python-dotenv
