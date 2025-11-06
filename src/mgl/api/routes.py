from __future__ import annotations
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from mgl.domain.models import Juego, Favorito
from mgl.infra.db import get_engine, get_session, create_schema
from mgl.repos.juegos import JuegosRepo
from mgl.repos.usuarios import create_user, get_user, verify_password

# --- DB ---
#ENGINE = get_engine("../mgl.db")
ENGINE = get_engine()
create_schema(ENGINE)

def get_db():
    with get_session(ENGINE) as session:
        yield session

# --- Templates ---
BASE = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE / "mgl" / "templates"))

# ✅ Helper para templates con usuario en contexto
def template(request: Request, name: str, context: dict = None):
    user = request.session.get("user")
    context = context or {}
    context["request"] = request
    context["user"] = user
    return templates.TemplateResponse(name, context)

# ----------------------------------------------------
# API JSON
# ----------------------------------------------------
api_router = APIRouter()

@api_router.get("/juegos", response_model=List[Juego])
def list_juegos(
    q: Optional[str] = Query(default=None),
    genero: Optional[str] = Query(default=None),
    plataforma: Optional[str] = Query(default=None),
    desde: Optional[int] = Query(default=None),
    hasta: Optional[int] = Query(default=None),
    session: Session = Depends(get_db)
):
    repo = JuegosRepo(session)
    return repo.list(q=q, genero=genero, plataforma=plataforma, desde=desde, hasta=hasta)

@api_router.get("/juegos/{juego_id}", response_model=Juego)
def get_juego(juego_id: int, session: Session = Depends(get_db)):
    j = session.get(Juego, juego_id)
    if not j:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return j

# ----------------------------------------------------
# Páginas (Jinja2)
# ----------------------------------------------------
page_router = APIRouter()

@page_router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_db)):
    juegos = JuegosRepo(session).list()[:8]
    return template(request, "home.html", {"juegos": juegos})

# 🔍 NUEVA RUTA: buscador de juegos
@page_router.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = Query(default=None), session: Session = Depends(get_db)):
    repo = JuegosRepo(session)
    juegos = repo.list()

    if q:
        q_lower = q.lower()
        juegos = [j for j in juegos if q_lower in j.titulo.lower()]

    return template(request, "home.html", {"juegos": juegos, "q": q})

# ----------------------------------------------------
# Panel de administración
# ----------------------------------------------------
@page_router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, session: Session = Depends(get_db)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=302)

    juegos = session.exec(select(Juego).order_by(Juego.fecha.desc())).all()
    return template(request, "admin.html", {"juegos": juegos})

@page_router.post("/admin/crear")
async def admin_crear(
    request: Request,
    titulo: str = Form(...), plataforma: str = Form(...),
    genero: str = Form(...), fecha: int = Form(...),
    descripcion: str = Form(""), puntuacion: int = Form(0),
    portada_url: Optional[str] = Form(None), session: Session = Depends(get_db)
):
    portada_url = (portada_url or "").strip() or None
    j = Juego(
        titulo=titulo, plataforma=plataforma, genero=genero,
        fecha=fecha, descripcion=descripcion, puntuacion=puntuacion, portada_url=portada_url
    )
    session.add(j)
    session.commit()
    return RedirectResponse(url="/admin", status_code=303)

@page_router.post("/admin/borrar")
def admin_borrar(juego_id: int = Form(...), session: Session = Depends(get_db)):
    j = session.get(Juego, juego_id)
    if j:
        session.delete(j)
        session.commit()
    return RedirectResponse(url="/admin", status_code=303)

# ----------------------------------------------------
# Registro y login
# ----------------------------------------------------
@page_router.get("/register")
def register_form(request: Request):
    return template(request, "register.html")

@page_router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_db)
):
    user = get_user(session, username)
    if user:
        return template(request, "register.html", {"error": "El usuario ya existe"})

    create_user(session, username, password)
    return RedirectResponse(url="/login", status_code=302)

@page_router.get("/login")
def login_form(request: Request):
    return template(request, "login.html")

@page_router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_db)
):
    user = get_user(session, username)

    if not user or not verify_password(password, user.password_hash):
        return template(request, "login.html", {"error": "Credenciales incorrectas"})

    request.session["user"] = user.username
    return RedirectResponse(url="/", status_code=302)

@page_router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

# ----------------------------------------------------
# Detalle de juego
# ----------------------------------------------------
@page_router.get("/juego/{juego_id}", response_class=HTMLResponse)
def juego_detalle(request: Request, juego_id: int, session: Session = Depends(get_db)):
    juego = session.get(Juego, juego_id)
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return template(request, "juego_detalle.html", {"juego": juego})
