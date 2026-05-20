from pathlib import Path
import os
from typing import List
import asyncio

from fastapi import Depends, FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import structlog

from collector import sqlite_storage as storage
from collector.logging_config import setup_logging
from collector.middlewares import RateLimitMiddleware
from risk_analyzer import add_risk_column

DB_PATH = Path(os.getenv("WEATHER_DB", "weather.db"))
API_KEYS = {k.strip() for k in os.getenv("API_KEYS", os.getenv("API_KEY", "")).split(",") if k.strip()}


def _validate_api_key(raw_key: str) -> bool:
    return (not API_KEYS) or (raw_key in API_KEYS)


async def require_api_key(x_api_key: str = Header(default="")):
    if not _validate_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")


setup_logging()
logger = structlog.get_logger(__name__)


async def lifespan(app: FastAPI):
    await asyncio.to_thread(storage.init_db, DB_PATH)
    yield


app = FastAPI(title="Banksia API", lifespan=lifespan)
redis_url = os.getenv("REDIS_URL")
app.add_middleware(RateLimitMiddleware, max_requests=100, window=60, redis_url=redis_url)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Instrumentator().instrument(app).expose(app)
app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="dashboard")


class WeatherRecord(BaseModel):
    district: str
    date: str
    temp: float
    humidity: float
    wind_speed: float


class Stats(BaseModel):
    avg_temp: float | None
    avg_humidity: float | None
    avg_wind_speed: float | None
    max_temp: float | None
    min_temp: float | None
    max_humidity: float | None
    min_humidity: float | None
    max_wind_speed: float | None
    min_wind_speed: float | None


@app.get("/api/weather/latest", response_model=List[WeatherRecord])
async def latest_data(limit: int = 100, _=Depends(require_api_key)):
    df = await asyncio.to_thread(storage.query_latest, DB_PATH, limit)
    return df.to_dict(orient="records")


@app.get("/api/weather/range", response_model=List[WeatherRecord])
async def data_range(start: str | None = None, end: str | None = None, district: str | None = None, limit: int | None = None, _=Depends(require_api_key)):
    districts = [district] if district else None
    df = await asyncio.to_thread(storage.query_range, DB_PATH, start, end, districts, limit)
    return df.to_dict(orient="records")


@app.get("/api/weather/risk")
async def risk_score_endpoint(limit: int = 100, _=Depends(require_api_key)):
    df = await asyncio.to_thread(storage.query_latest, DB_PATH, limit)
    df = add_risk_column(df)
    return df.to_dict(orient="records")


@app.get("/api/weather/statistics", response_model=Stats)
async def statistics(_=Depends(require_api_key)):
    return await asyncio.to_thread(storage.get_statistics, DB_PATH)


class ConnectionManager:
    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for ws in list(self.active):
            try:
                await ws.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(ws)


manager = ConnectionManager()


@app.websocket("/ws/weather")
async def websocket_weather(ws: WebSocket, x_api_key: str = Header(default="")):
    if not _validate_api_key(x_api_key):
        await ws.close(code=1008)
        return
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
            df = await asyncio.to_thread(storage.query_latest, DB_PATH, 1)
            await manager.broadcast(df.to_json(orient="records"))
    except WebSocketDisconnect:
        manager.disconnect(ws)
