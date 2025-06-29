# Banksia

Banksia is a collection of tools for fetching and analyzing weather data from Turkey's Meteorological Service (MGM). It includes a data collector, a FastAPI-based API server, Kafka utilities, and optional machine-learning components for fire risk prediction. The project is distributed under the **F.U.C.K. License** found in the `LICENSE` file.

## Features

- Fetch hourly weather data with retry logic (`data_collector.py`).
- Store data in SQLite, PostgreSQL/TimescaleDB, or InfluxDB.
- Serve data and statistics over a FastAPI API with optional WebSocket updates.
- Lightweight Vue dashboard under `/dashboard`.
- Prometheus metrics exposed via `/metrics`.
- Kafka streaming utilities for real-time pipelines.
- Kubernetes manifests and Dockerfile for containerized deployment.
- Utilities for training machine-learning models to predict fire risk.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests to verify the setup:
   ```bash
   pytest -q
   ```
3. Collect the latest weather data:
   ```bash
   python data_collector.py --output weather_data.json
   ```
4. Launch the API server:
   ```bash
   uvicorn fastapi_app:app --reload
   ```
5. Open `http://localhost:8000/dashboard` to see the basic dashboard.

Environment variables such as `WEATHER_DB`, `API_KEY`, and `MGM_API_URL` can be configured in a `.env` file. See `fastapi_app.py` and `collector/config.py` for defaults.

### Docker

Build and run the image locally:
```bash
docker build -t banksia .
docker run -p 8000:8000 banksia
```

### Kubernetes

The `k8s/` directory contains example manifests for deploying the application. Adjust the image and configuration values before applying them with `kubectl`.

## Contributing

Please ensure all tests pass and adhere to the licensing terms. Contributions should serve public good and respect user privacy.

