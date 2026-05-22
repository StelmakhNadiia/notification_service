# Notification Service

Notification Service for a microservice-based E-Learning platform. This service operates as a reactive consumer within the platform's message broker, handling transactional email dispatches and push alerts based on domain events.

## Features

* **FastAPI REST API** with asynchronous request handling.
* **PostgreSQL persistence** via SQLAlchemy 2.0 (AsyncPG) for secure audit logging and notification history.
* **RabbitMQ consumer** using `aiormq` to handle reactive e-learning events (`UserRegistered`, `PaymentSucceeded`, `CourseCompleted`).
* **Dynamic HTML/Text parsing** using Jinja2 template rendering engine.
* **Fault Tolerance & Reliability** via an automated transport delivery retry mechanism with exponential back-off (NFR-R5).
* **Distributed Tracing** with end-to-end `trace_id` tracking injected into structured JSON logs (NFR-O2/O4).
* **Data Masking** for financial and sensitive attributes to protect privacy in application logs (NFR-S4).

## Architecture

The microservice strictly follows a decoupled **Layered Architecture** pattern to guarantee high maintainability (NFR-M1):
* **Controllers / Inbound Interfaces:** `app/controllers/http_routes.py` (FastAPI router) and `app/controllers/broker_consumer.py` (RabbitMQ event listener).
* **Core Business Logic (Services):** `app/services/notification_manager.py` (Jinja2 compiler and dispatch retry orchestrator) and `app/services/logger.py` (Structured logging context).
* **Data Access Layer (Repositories):** `app/repositories/notification_repo.py` (SQLAlchemy 2.0 async database interactions).

## API & Event Endpoints

* **Sync Health Check Endpoint:** `GET /health` (Exposes lightweight live status of application, database pool, and broker connectivity).
* **OpenAPI spec:** `api-docs/openapi.yaml`
* **AsyncAPI spec:** `api-docs/asyncapi.yaml`

## Run with Docker Compose

Spin up the entire localized infrastructure (Microservice + Database + Broker) with absolute isolation using a single command:

## Run with Docker Compose

```bash
docker-compose up --build
```

Infrastructure Services Summary:

- Notification App Core: http://localhost:8000 (Health Check at http://localhost:8000/health)
- PostgreSQL Database: localhost:5432 (Database name: notification_db)
- RabbitMQ Message Broker: localhost:5672 (Management Dashboard UI available at http://localhost:15672 via credentials guest/guest)

## Run tests

```bash
pip install -r requirements.txt
pytest
```

