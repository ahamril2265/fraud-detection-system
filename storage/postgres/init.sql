CREATE TABLE IF NOT EXISTS transactions_raw (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud_predictions (
    id SERIAL PRIMARY KEY,
    transaction_id TEXT,
    risk_score FLOAT,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions_enriched (
    transaction_id TEXT PRIMARY KEY,
    user_id TEXT,
    device_id TEXT,
    amount NUMERIC,
    currency TEXT,
    transaction_type TEXT,
    payment_channel TEXT,
    merchant_id TEXT,
    merchant_category TEXT,
    country TEXT,
    city TEXT,
    timestamp TIMESTAMP,

    -- features
    time_since_last_tx NUMERIC,
    user_tx_count INTEGER,
    user_avg_amount NUMERIC,
    location_changed BOOLEAN,
    amount_deviation NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_daily_stats (
    user_id TEXT,
    date DATE,
    tx_count INTEGER,
    avg_amount NUMERIC,
    max_amount NUMERIC,
    country_changes INTEGER,

    PRIMARY KEY (user_id, date)
);

CREATE INDEX IF NOT EXISTS idx_enriched_user_time
ON transactions_enriched (user_id, timestamp);

CREATE INDEX IF NOT EXISTS idx_enriched_amount
ON transactions_enriched (amount);

CREATE INDEX IF NOT EXISTS idx_enriched_country
ON transactions_enriched (country);

