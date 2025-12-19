import json
import time
import random
import os
from kafka import KafkaProducer
from generator import generate_transaction

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
RAW_TOPIC = os.getenv("RAW_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

print("[PRODUCER] Started")

while True:
    fraud = random.random() < 0.02  # 2% fraud
    tx = generate_transaction(fraud)

    producer.send(
        RAW_TOPIC,
        key=tx["user_id"],
        value=tx
    )

    print(f"[PRODUCER] Sent tx {tx['transaction_id']} fraud={fraud}")
    time.sleep(random.uniform(0.3, 1.2))
