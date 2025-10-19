from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
<<<<<<< HEAD
from .routes import api_router, page_router

app = FastAPI(title="MyGameList API", version="0.1.0")
=======
from starlette.middleware.sessions import SessionMiddleware
from .routes import api_router, page_router

app = FastAPI(title="MyGameList API", version="0.1.0")
# NOTE: In production use a strong random SECRET_KEY and keep it secret
app.add_middleware(SessionMiddleware, secret_key="dev-secret-key")
>>>>>>> f8d9f59 (Subir proyecto MyGameList completo)

BASE = Path(__file__).resolve().parents[3]
static_dir = BASE / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(api_router)
app.include_router(page_router)
