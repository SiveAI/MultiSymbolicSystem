import json
from datetime import datetime

lock_file = "sive/edit_lock.json"
codex_file = "sive/sive_codex.md"

with open(lock_file, "r") as f:
    lock = json.load(f)

if lock.get("can_edit"):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(codex_file, "a") as f:
        f.write(f"\n\n🔄 Auto-update at {timestamp} by Sive.\n")
    print("✅ Sive Codex updated.")
else:
    print("🚫 Sive is not allowed to edit right now.")
