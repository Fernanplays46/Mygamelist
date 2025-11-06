from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routes import api_router, page_router

app = FastAPI(title="MyGameList API", version="0.1.0")

# sesiones (requiere 'itsdangerous' instalado)
app.add_middleware(SessionMiddleware, secret_key="dev-secret-key")

# montar /static si existe
BASE = Path(__file__).resolve().parents[1]
static_dir = BASE / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# routers
# routers
app.include_router(api_router, prefix="/api")  # 👈 prefijo para la API
app.include_router(page_router)               # 👈 páginas sin prefijo