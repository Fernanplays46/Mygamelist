from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import api_router, page_router

app = FastAPI(title="MyGameList API", version="0.1.0")

BASE = Path(__file__).resolve().parents[3]
static_dir = BASE / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(api_router)
app.include_router(page_router)
