# Real-Time Financial Fraud Detection Platform

A production-inspired event-driven fraud detection platform that ingests financial transactions, performs streaming ETL, enriches behavioral features, applies machine learning risk scoring, and provides real-time fraud monitoring.

---

## Overview

Financial institutions process millions of transactions daily and require systems capable of detecting suspicious activity in real time.

This project simulates a modern fraud detection architecture using:

- Apache Kafka event streaming
- Stateful stream processing
- Transaction validation
- Feature enrichment
- Isolation Forest anomaly detection
- PostgreSQL persistence
- Streamlit monitoring dashboard

---

## Architecture

```text
                    ┌─────────────────────┐
                    │ Transaction Producer│
                    └──────────┬──────────┘
                               │
                               ▼
                     Kafka RAW Topic
                               │
                               ▼
               ┌─────────────────────────┐
               │ Streaming ETL Service   │
               │                         │
               │ • Validation            │
               │ • DLQ Routing           │
               │ • State Tracking        │
               │ • Feature Engineering   │
               └──────────┬──────────────┘
                          │
                          ▼
                    Kafka CLEAN Topic
                          │
                          ▼
              ┌─────────────────────────┐
              │ ML Inference Service    │
              │ Isolation Forest        │
              └──────────┬──────────────┘
                         │
                         ▼
                   Fraud Alerts
                         │
                         ▼
                    PostgreSQL
                         │
                         ▼
                Streamlit Dashboard
```

---

## Key Features

### Event Streaming

- Kafka-based transaction ingestion
- Real-time processing
- Event-driven architecture

### Streaming ETL

- Transaction validation
- Dead Letter Queue handling
- Stateful processing
- Feature enrichment

### Fraud Analytics

Derived behavioral features:

- Amount deviation
- Transaction frequency
- Time since last transaction
- Location change detection

### Machine Learning

- Isolation Forest anomaly detection
- Continuous fraud scoring
- Risk classification:
  - LOW
  - MEDIUM
  - HIGH

### Persistence Layer

- PostgreSQL storage
- Historical fraud intelligence
- Auditability

### Monitoring

- Risk distribution dashboard
- High-risk user tracking
- Real-time fraud alerts

---

## Tech Stack

| Category | Technology |
|-----------|-----------|
| Language | Python |
| Streaming | Apache Kafka |
| Database | PostgreSQL |
| Machine Learning | Scikit-Learn |
| Dashboard | Streamlit |
| Containerization | Docker |
| Orchestration | Docker Compose |

---

## Microservices

### Producer

Generates synthetic financial transactions and publishes them to Kafka.

### ETL Service

Performs:

- Validation
- DLQ routing
- Stateful processing
- Feature enrichment

### ML Inference Service

Scores transactions using Isolation Forest and generates fraud alerts.

### Dashboard Service

Visualizes fraud metrics and alerts in real time.

---

## Running the Platform

```bash
docker-compose up --build
```

Access:

- Kafka: localhost:9092
- PostgreSQL: localhost:5432
- Dashboard: localhost:8501

---

## Engineering Concepts Demonstrated

- Event-Driven Architecture
- Streaming ETL
- Kafka Messaging
- Stateful Processing
- Feature Engineering
- Anomaly Detection
- Microservices
- Dockerized Infrastructure
- Fraud Analytics

---

## Future Enhancements

- Kafka Streams / Flink
- Redis State Store
- Prometheus Monitoring
- Grafana Dashboards
- Model Retraining Pipeline
- Kubernetes Deployment
- Real Banking Transaction Feeds

---

## Author

Ahamed Rilwan

GitHub: https://github.com/ahamril2265

LinkedIn: https://linkedin.com/in/ahamedrilwan
