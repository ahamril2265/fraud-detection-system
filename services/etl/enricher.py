def enrich_transaction(tx, state_features):
    enriched = tx.copy()

    enriched.update({
        "time_since_last_tx": state_features["time_since_last_tx"],
        "user_tx_count": state_features["user_tx_count"],
        "user_avg_amount": state_features["user_avg_amount"],
        "location_changed": state_features["location_changed"],
        "amount_deviation":
            round(tx["amount"] - state_features["user_avg_amount"], 2)
    })

    return enriched
