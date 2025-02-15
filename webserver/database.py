import time

# Change this to a database connection
log_data = []

def log_event(event):
    log_data.append({
        "timestamp": time.time(),
        "event": event.get("event"),
        "text": event.get("text"),
        "data": event.get("data")
    })
    print(f"LOGGED EVENT: {event}")  # Print to console for debugging