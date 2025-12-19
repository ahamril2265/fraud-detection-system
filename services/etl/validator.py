REQUIRED_FIELDS = {
    "transaction_id": str,
    "schema_version": str,
    "user_id": str,
    "device_id": str,
    "amount": (int, float),
    "currency": str,
    "transaction_type": str,
    "payment_channel": str,
    "merchant_id": str,
    "merchant_category": str,
    "country": str,
    "city": str,
    "timestamp": str,
}

ALLOWED_CURRENCIES = {"INR"}
ALLOWED_CHANNELS = {"card", "upi", "netbanking"}

def validate_transaction(tx: dict):
    for field, dtype in REQUIRED_FIELDS.items():
        if field not in tx:
            return False, f"Missing field: {field}"
        if not isinstance(tx[field], dtype):
            return False, f"Invalid type for {field}"

    if tx["amount"] <= 0:
        return False, "Amount must be positive"

    if tx["currency"] not in ALLOWED_CURRENCIES:
        return False, "Unsupported currency"

    if tx["payment_channel"] not in ALLOWED_CHANNELS:
        return False, "Invalid payment channel"

    return True, "OK"
