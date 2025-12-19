from collections import defaultdict
from datetime import datetime

class UserState:
    def __init__(self):
        self.last_tx_time = None
        self.tx_count = 0
        self.total_amount = 0.0
        self.last_country = None

STATE = defaultdict(UserState)

def update_state(user_id, tx):
    state = STATE[user_id]
    now = datetime.fromisoformat(tx["timestamp"])

    time_since_last = None
    if state.last_tx_time:
        time_since_last = (now - state.last_tx_time).total_seconds()

    state.last_tx_time = now
    state.tx_count += 1
    state.total_amount += tx["amount"]

    location_changed = (
        state.last_country is not None and
        state.last_country != tx["country"]
    )
    state.last_country = tx["country"]

    avg_amount = state.total_amount / state.tx_count

    return {
        "time_since_last_tx": time_since_last,
        "user_tx_count": state.tx_count,
        "user_avg_amount": round(avg_amount, 2),
        "location_changed": location_changed
    }
