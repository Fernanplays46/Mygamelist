from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import Request

BASE = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(BASE / "templates"))

def template(request: Request, name: str, context: dict = None):
    user = request.session.get("user")
    context = context or {}
    context["request"] = request
    context["user"] = user
    return templates.TemplateResponse(name, context)
