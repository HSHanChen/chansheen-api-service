import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def get_users():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
