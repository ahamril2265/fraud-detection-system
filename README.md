# Real-Time Financial Fraud Detection Platform

## Overview
A Kafka-based, real-time fraud detection system that ingests financial transactions, performs streaming ETL with data quality checks, applies unsupervised ML for risk scoring, and provides explainable fraud alerts with live monitoring.

## Architecture
- Kafka for event streaming
- Python microservices (Producer, ETL, ML Inference)
- PostgreSQL for audit & analytics
- Isolation Forest for fraud detection
- Streamlit dashboard for monitoring
- Docker Compose for orchestration

## Key Features
- Event-driven ingestion
- Stateful streaming ETL
- Dead Letter Queue (DLQ)
- Unsupervised fraud detection
- Explainable risk scoring
- Persistent fraud intelligence
- Live monitoring dashboard

## Tech Stack
Kafka, Python, PostgreSQL, scikit-learn, Streamlit, Docker

## Status
Production-designed prototype
