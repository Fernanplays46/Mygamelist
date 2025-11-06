from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# importa routers
from mgl.api.routes import page_router, api_router

app = FastAPI(title="MyGameList")

# sesiones
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# BASE = carpeta src/mgl (si main.py está en src/mgl/api -> parents[1] = src/mgl)
BASE = Path(__file__).resolve().parents[1]

# montar /static (usa la carpeta src/mgl/static)
static_dir = BASE / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
else:
    # opcional: imprimir advertencia para depuración
    print("Static directory not found:", static_dir)

# incluir routers
app.include_router(api_router, prefix="/api")
app.include_router(page_router)
