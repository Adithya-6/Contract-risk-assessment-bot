
import json
from datetime import datetime

def save_audit_log(data):
    log_entry = {
        "timestamp": str(datetime.now()),
        "data": data
    }
    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
