"""Helpers de base de datos (SQLite + SQLModel)."""
from __future__ import annotations

from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine

def get_engine(db_path: Path | str = "mgl.db"):
    url = f"sqlite:///{db_path}"
    return create_engine(url, echo=False)

def create_schema(engine):
    from mgl.domain.models import Juego, Usuario, Favorito  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session(engine):
    return Session(engine)
