from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from mgl.infra.db import get_session
from mgl.repos.usuarios import create_user, get_user, verify_password
from mgl.web.shared import template
from sqlmodel import Session

router = APIRouter()

# --- Registro ---
@router.get("/register")
def register_form(request: Request):
    return template(request, "register.html")

@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = get_user(session, username)
    if user:
        return template(request, "register.html", {"error": "El usuario ya existe"})

    create_user(session, username, password)
    return RedirectResponse(url="/login", status_code=302)


# --- Login ---
@router.get("/login")
def login_form(request: Request):
    return template(request, "login.html")

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = get_user(session, username)

    if not user or not verify_password(password, user.password_hash):
        return template(request, "login.html", {"error": "Credenciales incorrectas"})

    request.session["user"] = user.username
    return RedirectResponse(url="/", status_code=302)


# --- Logout ---
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)
