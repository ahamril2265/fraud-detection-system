import psycopg2
import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)

query = """
SELECT
    amount,
    amount_deviation,
    COALESCE(time_since_last_tx, 9999) AS time_since_last_tx,
    user_tx_count,
    CASE WHEN location_changed THEN 1 ELSE 0 END AS location_changed
FROM transactions_enriched;
"""

df = pd.read_sql(query, conn)

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

model.fit(df)

joblib.dump(model, "models/model.joblib")

print("[ML] Model trained and saved")
