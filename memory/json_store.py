import json
import os
from threading import Lock
from datetime import datetime, timezone

class JSONSummaryStore:
    def __init__(self, path="memory.json"):
        self.path = path
        self.lock = Lock()

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"sessions": {}}, f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def update_summary(self, session_id, summary, turns):
        with self.lock:
            data = self.load()

            data["sessions"][session_id] = {
                "summary": summary,
                "turns": turns,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }

            self.save(data)

    def get_summary(self, session_id):
        data = self.load()
        return data["sessions"].get(session_id)