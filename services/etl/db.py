import psycopg2
import os
import json
import time

_conn = None

def get_connection(retries=10, delay=2):
    global _conn

    if _conn is not None:
        return _conn

    for attempt in range(1, retries + 1):
        try:
            _conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
            )
            _conn.autocommit = True
            print("[DB] Connected to Postgres")
            return _conn
        except psycopg2.OperationalError as e:
            print(f"[DB] Connection failed (attempt {attempt}/{retries})")
            time.sleep(delay)

    raise Exception("Could not connect to Postgres after retries")


def insert_transaction(tx):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO transactions_raw (payload)
            VALUES (%s);
            """,
            (json.dumps(tx),)
        )

def insert_enriched_transaction(tx):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO transactions_enriched (
                transaction_id, user_id, device_id, amount, currency,
                transaction_type, payment_channel, merchant_id,
                merchant_category, country, city, timestamp,
                time_since_last_tx, user_tx_count, user_avg_amount,
                location_changed, amount_deviation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING;
            """,
            (
                tx["transaction_id"],
                tx["user_id"],
                tx["device_id"],
                tx["amount"],
                tx["currency"],
                tx["transaction_type"],
                tx["payment_channel"],
                tx["merchant_id"],
                tx["merchant_category"],
                tx["country"],
                tx["city"],
                tx["timestamp"],
                tx["time_since_last_tx"],
                tx["user_tx_count"],
                tx["user_avg_amount"],
                tx["location_changed"],
                tx["amount_deviation"],
            )
        )
