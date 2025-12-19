import json
import os
import joblib
import psycopg2
from kafka import KafkaConsumer, KafkaProducer
import pandas as pd

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
CLEAN_TOPIC = os.getenv("CLEAN_TOPIC")
FRAUD_TOPIC = os.getenv("FRAUD_TOPIC")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)
conn.autocommit = True

model = joblib.load("models/model.joblib")


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

consumer = KafkaConsumer(
    CLEAN_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8")
)

print("[ML] Inference service started")

for msg in consumer:
    tx = msg.value
    user_id = msg.key

    features = pd.DataFrame([{
        "amount": tx["amount"],
        "amount_deviation": tx["amount_deviation"],
        "time_since_last_tx": tx["time_since_last_tx"] or 9999,
        "user_tx_count": tx["user_tx_count"],
        "location_changed": 1 if tx["location_changed"] else 0
    }])

    score = -model.decision_function(features)[0]  # higher = risk

    if score > 0.6:
        risk = "HIGH"
    elif score > 0.3:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    reasons = []
    if tx["amount_deviation"] > 20000:
        reasons.append("Unusual transaction amount")
    if tx["location_changed"]:
        reasons.append("Location change detected")
    if tx["time_since_last_tx"] and tx["time_since_last_tx"] < 30:
        reasons.append("High transaction velocity")

    alert = {
        "transaction_id": tx["transaction_id"],
        "user_id": user_id,
        "risk_score": round(score, 3),
        "risk_level": risk,
        "reasons": reasons
    }

    producer.send(FRAUD_TOPIC, key=user_id, value=alert)
    with conn.cursor() as cur:
    cur.execute(
        """
        INSERT INTO fraud_predictions
        (transaction_id, user_id, risk_score, risk_level, reasons)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
        """,
        (
            alert["transaction_id"],
            alert["user_id"],
            alert["risk_score"],
            alert["risk_level"],
            alert["reasons"],
        )
    )

    print(f"[ML] Scored tx {tx['transaction_id']} → {risk}")
