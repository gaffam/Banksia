# Banksia

Banksia, ilçe bazlı yangın riskini hava durumu + uydu sıcak nokta verisiyle izlemek için tasarlanmış bir FastAPI servisidir.

## Ne işe yarar?
- İlçe bazlı son ölçümleri döner.
- Tarih aralığında geçmiş veriyi filtreler.
- Basit risk skoru üretir.
- Canlı panel ve websocket üzerinden en güncel veriyi yayınlar.

## Neye iyi değil?
- Üretim-grade FWI implementasyonu henüz yok.
- MGM/FIRMS kaynakları adapter + fallback yapısına tam geçirilmedi.
- PostgreSQL/PostGIS varsayılan değil (geçiş planı gerekiyor).

## 3 komutta çalıştır
```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

Ardından:
- API docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8000/dashboard`

## API Özeti
- `GET /api/weather/latest`
- `GET /api/weather/range`
- `GET /api/weather/risk`
- `GET /api/weather/statistics`
- `GET /ws/weather`

Header auth için:
- `x-api-key: <API_KEYS içindeki key>`
