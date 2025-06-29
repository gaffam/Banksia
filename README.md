# Banksia

Banksia is an open-source toolkit for gathering meteorological data and estimating wildfire risk. The project fetches hourly weather observations from Turkey's State Meteorological Service (MGM) and stores them in a local or remote database. A FastAPI backend exposes recent records and statistics, while an optional Vue dashboard visualizes the data.

## Features

- **Data Collection** from the MGM API with retry logic
- **Storage Options:** SQLite by default, with optional PostgreSQL/TimescaleDB and InfluxDB support
- **API Service** providing JSON endpoints, WebSocket streaming, and Prometheus metrics
- **Frontend Dashboard** built with Vue and Chart.js
- **Kafka Streaming** utilities for real-time pipelines
- **Risk Analysis** helpers and machine-learning model training via `risk_analyzer.py`
- **Docker** image and Kubernetes manifests for deployment

## Quick Start

1. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. Collect data:
   ```bash
   python data_collector.py --output weather_data.json
   ```
3. Run the API server:
   ```bash
   uvicorn fastapi_app:app --reload
   ```
4. Open `http://localhost:8000/dashboard/` to view the dashboard.

## Tests

Run the full test suite with:
```bash
pytest -q
```

## Docker

Build and start the service using Docker:
```bash
docker build -t banksia .
docker run -p 8000:8000 banksia
```

## Kubernetes

Deployment manifests reside in `k8s/`. Apply them in order:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

## License

This project is released under the terms of the F.U.C.K. License. See the [LICENSE](LICENSE) file for details.
