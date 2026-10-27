"""Local JSON storage for desynth log entries."""

import json
import os
import time

DEFAULT_STORAGE_PATH = os.path.join(os.getcwd(), "desynth_entries.json")


class Storage:
    def __init__(self, path=DEFAULT_STORAGE_PATH):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return []
        if isinstance(data, dict) and "entries" in data:
            return list(data["entries"])
        if isinstance(data, list):
            return list(data)
        return []

    def save(self, entries):
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump({"entries": entries}, fh, indent=2)

    def add_entry(self, entry):
        entries = self.load()
        entry_id = max([e.get("id", 0) for e in entries], default=0) + 1
        entry = dict(entry)
        entry["id"] = entry_id
        entry.setdefault("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        entries.append(entry)
        self.save(entries)
        return entry
