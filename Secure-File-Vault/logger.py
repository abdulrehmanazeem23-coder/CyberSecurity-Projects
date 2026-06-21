from datetime import datetime
from config import LOG_FILE

def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")
