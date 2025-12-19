import streamlit as st
import psycopg2
import pandas as pd
import os

st.set_page_config(page_title="Fraud Monitoring Dashboard", layout="wide")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)

st.title("🚨 Fraud Detection Monitoring")

# --- Risk Summary ---
risk_df = pd.read_sql("""
    SELECT risk_level, COUNT(*) AS count
    FROM fraud_predictions
    WHERE created_at >= NOW() - INTERVAL '24 hours'
    GROUP BY risk_level;
""", conn)

st.subheader("Risk Level Distribution (Last 24h)")
st.bar_chart(risk_df.set_index("risk_level"))

# --- Top Risky Users ---
top_users = pd.read_sql("""
    SELECT user_id, COUNT(*) AS high_risk_count
    FROM fraud_predictions
    WHERE risk_level = 'HIGH'
    GROUP BY user_id
    ORDER BY high_risk_count DESC
    LIMIT 10;
""", conn)

st.subheader("Top Risky Users")
st.dataframe(top_users)

# --- Recent Alerts ---
recent_alerts = pd.read_sql("""
    SELECT transaction_id, user_id, risk_score, risk_level, reasons, created_at
    FROM fraud_predictions
    ORDER BY created_at DESC
    LIMIT 20;
""", conn)

st.subheader("Recent Fraud Alerts")
st.dataframe(recent_alerts)
