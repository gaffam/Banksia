# Banksia

**Türkçe**: Banksia, başta orman yangınları olmak üzere çevresel yangın risklerini hesaplamak, gözlemlemek ve haber vermek için bağımsız bir yazılımcı tarafından geliştirilen açık kaynaklı bir projedir. Amaç, en ücra yerleşim birimlerinde bile düşük sistem gereksinimleriyle çalışabilen sürdürülebilir bir altyapı sunmaktır. Proje halen geliştirme aşamasındadır ve katkılara açıktır. Lütfen etik ilkelere sadık kalınız. Lisans: "F.U.C.K. — Freedom Under Conditioned Knowledge".

**English**: Banksia is an independent open-source project developed to compute, monitor, and alert for environmental fire risks, particularly wildfires. It is designed to run with minimal hardware even in remote areas. The project is still evolving, and contributions are welcome as long as ethical guidelines and data privacy are respected. Licensed under **F.U.C.K. — Freedom Under Conditioned Knowledge**.

---

## Overview

Banksia collects meteorological data from the Turkish State Meteorological Service (MGM) API and stores it in a database. By default, it uses SQLite, but it can also be configured to use PostgreSQL/TimescaleDB for larger datasets. A FastAPI backend serves recent records and analytics, while a Vue-based frontend dashboard provides visualization.

It also supports integration with satellite fire observation sources such as:

* `fetch_modis_data` — NASA MODIS active fire data
* `fetch_viirs_data` — VIIRS high-resolution fire detections
* `fetch_sentinel2_data` — Sentinel‑2 burned area imagery
* `fetch_effis_data` — European Forest Fire Information System

These datasets can be merged with local weather data for ML-based fire risk prediction.

---

## Usage

**Collect Data:**

```bash
python data_collector.py --output weather_data --db-url postgres://user:pass@localhost/weather
```

**Optional Backup to S3:**

```bash
python data_collector.py --output weather.json --s3-bucket my-bucket --s3-key weather/latest.json
```

**Lightweight Mode:**

```bash
python weather_script.py
```

**Run the API Server:**

```bash
API_KEY=yourkey uvicorn fastapi_app:app --reload
```

**Connect WebSocket:**

```bash
websocat ws://localhost:8000/ws/weather -E
```

**Open the Dashboard:**
Navigate to `http://localhost:8000/dashboard/` after starting the server.

---

## Features

* **PostgreSQL and InfluxDB support** for persistent and metric storage
* **Advanced API endpoints** like `/data-range`, `/hourly-average`, `/risk-score`
* **Slack alert integration** with `SLACK_WEBHOOK`
* **API key security** using `X-API-Key` headers
* **S3 upload** support with CLI flags

The `risk_analyzer` module supports both rule-based and ML-based scoring. Trained models use `RandomForestRegressor` and include advanced features like `wind_dir` and `condition` fields.

**Visualize Risk vs Brightness:**

```python
visualize.plot_brightness_vs_risk()
```

---

## Async API

Set `ASYNC_DB=1` to activate async endpoints using `aiosqlite`. Indexing is auto-enabled on the `date` column.

---

## Kubernetes Deployment

Deployment manifests are available in `k8s/`. Apply in the following order:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

---

## Model Versioning

The ML training stage is tracked via `dvc.yaml`. Use:

```bash
dvc repro
```

to generate and save the model to `models/model.joblib`.

---

## Microservices

Start separate services as needed:

```bash
uvicorn services.collector_service:app --port 8001
uvicorn services.risk_service:app --port 8002
```

---

## Kafka Streaming

**Stream to Kafka:**

```bash
python -m streaming.kafka_streamer stream_to_kafka --topic weather
```

**Consume and Save:**

```bash
python -m streaming.kafka_streamer consume_to_db --db weather.db --topic weather
```

---

## Monitoring

Prometheus metrics available at `/metrics`.

**Prometheus Job Example:**

```yaml
scrape_configs:
  - job_name: weather-api
    static_configs:
      - targets: ['localhost:8000']
```

**Grafana Setup:**

```bash
docker run -p 3000:3000 grafana/grafana
```

Add Prometheus at `http://localhost:9090` as data source.

---

## Backup Strategy

Track key assets with Git LFS:

```bash
git lfs install
git lfs track "backups/*" "models/*.joblib"
```

Collect and upload to S3:

```bash
python data_collector.py --output backups/weather.json \
    --s3-bucket my-bucket --s3-key weather/latest.json
```

---

## Hyperparameter Tuning

Run with Optuna:

```bash
python train_model.py --tune --trials 30
```

---

## License

Licensed under **F.U.C.K. — Freedom Under Conditioned Knowledge**. See `LICENSE` for terms and obligations.
