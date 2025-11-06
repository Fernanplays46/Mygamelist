from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from mgl.infra.db import get_session
from mgl.domain.models import Juego
from mgl.repos.juegos import JuegosRepo
from mgl.web.shared import template

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    repo = JuegosRepo(session)
    juegos = repo.list()[:8]
    return template(request, "home.html", {"juegos": juegos})

@router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, session: Session = Depends(get_session)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=302)

    juegos = session.exec(select(Juego).order_by(Juego.fecha.desc())).all()
    return template(request, "admin.html", {"juegos": juegos})

@router.post("/admin/crear")
def admin_crear(
    request: Request,
    titulo: str = Form(...), plataforma: str = Form(...),
    genero: str = Form(...), fecha: int = Form(...),
    descripcion: str = Form(""), puntuacion: int = Form(0),
    portada_url: str = Form(""),
    session: Session = Depends(get_session)
):
    portada_url = (portada_url or "").strip() or None

    j = Juego(
        titulo=titulo, plataforma=plataforma, genero=genero,
        fecha=fecha, descripcion=descripcion, puntuacion=puntuacion, 
        portada_url=portada_url
    )
    session.add(j)
    session.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/admin/borrar")
def admin_borrar(juego_id: int = Form(...), session: Session = Depends(get_session)):
    j = session.get(Juego, juego_id)
    if j:
        session.delete(j)
        session.commit()
    return RedirectResponse(url="/admin", status_code=303)
