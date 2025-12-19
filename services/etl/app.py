import json
import os
from kafka import KafkaConsumer, KafkaProducer

from validator import validate_transaction
from state import update_state
from enricher import enrich_transaction
from db import insert_transaction, insert_enriched_transaction

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
RAW_TOPIC = os.getenv("RAW_TOPIC")
CLEAN_TOPIC = os.getenv("CLEAN_TOPIC")
DLQ_TOPIC = os.getenv("DLQ_TOPIC")

consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8"),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8")
)

print("[ETL] Streaming ETL started")

for msg in consumer:
    tx = msg.value
    user_id = msg.key

    valid, reason = validate_transaction(tx)

    if not valid:
        tx["dlq_reason"] = reason
        producer.send(DLQ_TOPIC, key=user_id, value=tx)
        print(f"[ETL] Routed to DLQ: {reason}")
        continue

    state_features = update_state(user_id, tx)
    enriched_tx = enrich_transaction(tx, state_features)

    producer.send(CLEAN_TOPIC, key=user_id, value=enriched_tx)
    insert_transaction(enriched_tx)
    insert_enriched_transaction(enriched_tx)

    print(f"[ETL] Processed tx {tx['transaction_id']}")
