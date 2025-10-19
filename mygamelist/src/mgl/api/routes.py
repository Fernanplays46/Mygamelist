<<<<<<< HEAD
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from mgl.domain.models import Juego, Usuario, Favorito
from mgl.infra.db import get_engine, get_session, create_schema
from mgl.repos.juegos import JuegosRepo

ENGINE = get_engine("mgl.db")
create_schema(ENGINE)

def get_db():
    with get_session(ENGINE) as session:
        yield session

BASE = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(BASE / "templates"))

api_router = APIRouter()

@api_router.get("/juegos", response_model=List[Juego])
def list_juegos(
    q: Optional[str] = Query(default=None),
    genero: Optional[str] = Query(default=None),
    plataforma: Optional[str] = Query(default=None),
    desde: Optional[int] = Query(default=None),
    hasta: Optional[int] = Query(default=None),
    session: Session = Depends(get_db),
):
    repo = JuegosRepo(session)
    return repo.list(q=q, genero=genero, plataforma=plataforma, desde=desde, hasta=hasta)

@api_router.post("/juegos", response_model=Juego, status_code=201)
def create_juego(juego: Juego, session: Session = Depends(get_db)):
    if juego.id is not None:
        raise HTTPException(status_code=400, detail="No envíes id al crear")
    repo = JuegosRepo(session)
    return repo.create(
        titulo=juego.titulo,
        plataforma=juego.plataforma,
        genero=juego.genero,
        fecha=juego.fecha,
        descripcion=juego.descripcion,
        puntuacion=getattr(juego, "puntuacion", 0),
        portada_url=getattr(juego, "portada_url", None),
    )

@api_router.get("/juegos/{juego_id}", response_model=Juego)
def get_juego(juego_id: int, session: Session = Depends(get_db)):
    j = session.get(Juego, juego_id)
    if not j:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return j

def _get_or_create_demo_user(session: Session) -> Usuario:
    user = session.exec(select(Usuario).where(Usuario.nombre == "demo")).first()
    if not user:
        user = Usuario(nombre="demo")
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

@api_router.get("/favoritos", response_model=List[Juego])
def list_favoritos(session: Session = Depends(get_db)):
    user = _get_or_create_demo_user(session)
    favs = session.exec(
        select(Juego).join(Favorito, Favorito.juego_id == Juego.id).where(Favorito.usuario_id == user.id)
    ).all()
    return favs

@api_router.post("/favoritos/{juego_id}", status_code=204)
def add_favorito(juego_id: int, session: Session = Depends(get_db)):
    user = _get_or_create_demo_user(session)
    j = session.get(Juego, juego_id)
    if not j:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    fav = session.get(Favorito, (user.id, j.id))
    if fav is None:
        session.add(Favorito(usuario_id=user.id, juego_id=j.id))
        session.commit()
    return None

@api_router.delete("/favoritos/{juego_id}", status_code=204)
def remove_favorito(juego_id: int, session: Session = Depends(get_db)):
    user = _get_or_create_demo_user(session)
    fav = session.get(Favorito, (user.id, juego_id))
    if fav:
        session.delete(fav)
        session.commit()
    return None

page_router = APIRouter()

@page_router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_db)):
    repo = JuegosRepo(session)
    juegos = repo.list()[:8]
    return templates.TemplateResponse("home.html", {"request": request, "juegos": juegos})

@page_router.get("/buscar", response_class=HTMLResponse)
def buscar(
    request: Request,
    q: Optional[str] = Query(default=None),
    genero: Optional[str] = Query(default=None),
    plataforma: Optional[str] = Query(default=None),
    session: Session = Depends(get_db),
):
    repo = JuegosRepo(session)
    juegos = repo.list(q=q, genero=genero, plataforma=plataforma)
    return templates.TemplateResponse("results.html", {"request": request, "juegos": juegos, "q": q or ""})

@page_router.get("/juego/{juego_id}", response_class=HTMLResponse)
def detalle_juego(juego_id: int, request: Request, session: Session = Depends(get_db)):
    j = session.get(Juego, juego_id)
    if not j:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return templates.TemplateResponse("detail.html", {"request": request, "juego": j})

@page_router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, session: Session = Depends(get_db)):
    juegos = session.exec(select(Juego).order_by(Juego.fecha.desc())).all()
    return templates.TemplateResponse("admin.html", {"request": request, "juegos": juegos})

@page_router.post("/admin/crear")
def admin_crear(
    request: Request,
    titulo: str = Form(...),
    plataforma: str = Form(...),
    genero: str = Form(...),
    fecha: int = Form(...),
    descripcion: str = Form(""),
    puntuacion: int = Form(0),
    portada_url: str = Form(None),
    session: Session = Depends(get_db),
):
    j = Juego(titulo=titulo, plataforma=plataforma, genero=genero, fecha=fecha,
              descripcion=descripcion, portada_url=portada_url, puntuacion=puntuacion)
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
=======
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from mgl.domain import models, database
from mgl.api.auth import get_current_user

page_router = APIRouter()
templates = Jinja2Templates(directory="src/mgl/templates")

# -------------------------------------------------------------------
# Listar juegos
# -------------------------------------------------------------------
@page_router.get("/juegos")
def listar_juegos(request: Request, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    juegos = db.query(models.Game).all()
    return templates.TemplateResponse("juegos.html", {"request": request, "user": user, "juegos": juegos})

# -------------------------------------------------------------------
# Añadir juego (solo admin)
# -------------------------------------------------------------------
@page_router.post("/juegos/add")
def add_juego(
    request: Request,
    title: str = Form(...),
    genre: str = Form(...),
    platform: str = Form(...),
    release_year: int = Form(...),
    db: Session = Depends(database.get_db),
    user: models.User = Depends(get_current_user)
):
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden añadir juegos")

    juego = models.Game(title=title, genre=genre, platform=platform, release_year=release_year)
    db.add(juego)
    db.commit()
    return RedirectResponse(url="/juegos", status_code=303)

# -------------------------------------------------------------------
# Borrar juego (solo admin)
# -------------------------------------------------------------------
@page_router.get("/juegos/delete/{game_id}")
def borrar_juego(game_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden borrar juegos")

    juego = db.query(models.Game).filter_by(id=game_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    db.delete(juego)
    db.commit()
    return RedirectResponse(url="/juegos", status_code=303)

# -------------------------------------------------------------------
# Añadir a favoritos
# -------------------------------------------------------------------
@page_router.get("/favoritos/add/{game_id}")
def add_favorito(game_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    juego = db.query(models.Game).filter_by(id=game_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    if juego not in user.favoritos:
        user.favoritos.append(juego)
        db.commit()

    return RedirectResponse(url="/juegos", status_code=303)

# -------------------------------------------------------------------
# Quitar de favoritos
# -------------------------------------------------------------------
@page_router.get("/favoritos/remove/{game_id}")
def remove_favorito(game_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    juego = db.query(models.Game).filter_by(id=game_id).first()
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    if juego in user.favoritos:
        user.favoritos.remove(juego)
        db.commit()

    return RedirectResponse(url="/juegos", status_code=303)

# -------------------------------------------------------------------
# Página de favoritos
# -------------------------------------------------------------------
@page_router.get("/usuarios/favoritos")
def favoritos_page(request: Request, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("favoritos.html", {"request": request, "user": user, "favoritos": user.favoritos})

>>>>>>> f8d9f59 (Subir proyecto MyGameList completo)
