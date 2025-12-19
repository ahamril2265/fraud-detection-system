import uuid
import random
from datetime import datetime, timedelta

USERS = [f"user_{i}" for i in range(1, 101)]
DEVICES = [f"device_{i}" for i in range(1, 120)]
MERCHANTS = ["amazon", "flipkart", "netflix", "zomato", "atm"]
CATEGORIES = ["ecommerce", "food", "entertainment", "cash"]
COUNTRIES = ["IN", "US", "SG"]
CITIES = {
    "IN": ["Chennai", "Bangalore", "Delhi"],
    "US": ["New York", "Chicago"],
    "SG": ["Singapore"]
}

def generate_transaction(fraud=False):
    user_id = random.choice(USERS)

    if fraud:
        amount = random.uniform(50000, 200000)
        device_id = f"unknown_{uuid.uuid4().hex[:6]}"
        country = random.choice(["US", "SG"])
    else:
        amount = random.uniform(50, 5000)
        device_id = random.choice(DEVICES)
        country = "IN"

    city = random.choice(CITIES[country])

    return {
        "transaction_id": str(uuid.uuid4()),
        "schema_version": "1.0",
        "user_id": user_id,
        "device_id": device_id,
        "amount": round(amount, 2),
        "currency": "INR",
        "transaction_type": random.choice(["purchase", "transfer", "withdrawal"]),
        "payment_channel": random.choice(["card", "upi", "netbanking"]),
        "merchant_id": random.choice(MERCHANTS),
        "merchant_category": random.choice(CATEGORIES),
        "country": country,
        "city": city,
        "timestamp": datetime.utcnow().isoformat(),
        "is_fraud_simulated": fraud
    }
