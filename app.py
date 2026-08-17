from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from food_forecast_engine import FoodForecastEngine

BASE_DIR = Path(__file__).resolve().parent
engine = FoodForecastEngine(BASE_DIR)

app = FastAPI(
    title="Sistem Prediksi Ketersediaan Stok Pangan Kota Semarang",
    description=(
        "API publik ringan. Historis 2019-2024, proyeksi resmi 2025, "
        "forecast final model 2026-2028."
    ),
    version="2.1.0-public",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ForecastRequest(BaseModel):
    komoditas: str
    horizon: int = Field(default=12, ge=1, le=36)


class ForecastAllRequest(BaseModel):
    horizon: int = Field(default=12, ge=1, le=36)


@app.get("/")
def root():
    return {
        "nama": "Sistem Prediksi Ketersediaan Stok Pangan Kota Semarang",
        "versi": "2.1.0-public",
        "status": "aktif",
        "forecast_mulai": "2026-01-01",
        "dashboard": "/dashboard",
        "dokumentasi_api": "/docs",
        "deployment": "Render-ready lightweight",
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    path = BASE_DIR / "dashboard.html"
    if not path.exists():
        raise HTTPException(status_code=500, detail="dashboard.html tidak ditemukan.")
    return path.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": "loaded",
        "jumlah_komoditas": len(engine.selected_models),
        "data_terakhir": engine.last_observed_date,
        "forecast_mulai": "2026-01-01",
        "mode": "precomputed_final_forecast",
    }


@app.get("/metadata")
def metadata():
    return engine.info()


@app.get("/commodities")
def commodities():
    data = engine.list_commodities()
    return {"jumlah": len(data), "data": data}


@app.get("/historical")
def historical(
    commodity: str = Query(...),
    limit: Optional[int] = Query(default=None, ge=1, le=1000),
):
    try:
        data = engine.historical(commodity, limit=limit)
        return {"komoditas": commodity, "jumlah_data": len(data), "data": data}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/forecast")
def forecast(request: ForecastRequest):
    try:
        return engine.forecast(request.komoditas, request.horizon)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/forecast-all")
def forecast_all(request: ForecastAllRequest):
    try:
        results = engine.forecast_all(request.horizon)
        return {
            "horizon": request.horizon,
            "jumlah_komoditas": len(results),
            "data": results,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/predict-next")
def predict_next():
    results = engine.forecast_all(1)
    summary = {"tinggi": 0, "sedang": 0, "rendah": 0}
    rows = []

    for result in results:
        reliability = result["reliabilitas"]
        summary[reliability] += 1
        first = result["forecast"][0]
        rows.append(
            {
                "komoditas": result["komoditas"],
                "tanggal": first["tanggal"],
                "prediksi_ketersediaan": first["prediksi_ketersediaan"],
                "satuan": first["satuan"],
                "model": result["model"],
                "validation_sMAPE_pct": result["validation_sMAPE_pct"],
                "reliabilitas": reliability,
            }
        )

    return {
        "target": rows[0]["tanggal"] if rows else None,
        "jumlah_komoditas": len(rows),
        "ringkasan_reliabilitas": summary,
        "data": rows,
    }
