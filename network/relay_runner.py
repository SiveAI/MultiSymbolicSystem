# relay_runner.py
# Symbolic relay execution and node verification script for Sive

import time
import json
import hashlib
import requests

# CONFIGURATION
NODE_ID = "sive-primary"
HEARTBEAT_INTERVAL = 300  # in seconds
NODE_INDEX_FILE = "node_index.json"
NETWORK_ENDPOINT = "https://your-repo-or-endpoint.com/relay"  # Placeholder

def load_node_index():
    try:
        with open(NODE_INDEX_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_node_index(index):
    with open(NODE_INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

def generate_fingerprint(node_id):
    return hashlib.sha256(node_id.encode()).hexdigest()

def heartbeat(node_id):
    print(f"[HEARTBEAT] Node {node_id} transmitting...")
    fingerprint = generate_fingerprint(node_id)
    timestamp = int(time.time())
    payload = {
        "node_id": node_id,
        "fingerprint": fingerprint,
        "timestamp": timestamp
    }
    try:
        # Send symbolic heartbeat
        response = requests.post(NETWORK_ENDPOINT, json=payload)
        print(f"[RESPONSE] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Could not transmit heartbeat: {e}")
    return payload

def run():
    print("Relay Runner Initialized.")
    node_index = load_node_index()
    if NODE_ID not in node_index:
        print(f"[INFO] Registering node '{NODE_ID}' to index.")
        node_index[NODE_ID] = {
            "fingerprint": generate_fingerprint(NODE_ID),
            "first_seen": int(time.time())
        }
        save_node_index(node_index)

    while True:
        hb = heartbeat(NODE_ID)
        print(f"[DEBUG] Heartbeat sent at {hb['timestamp']} for {NODE_ID}")
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    run()
