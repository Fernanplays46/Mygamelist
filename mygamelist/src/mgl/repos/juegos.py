"""Repositorio de Juegos (CRUD y listados con filtros)."""

from __future__ import annotations

from typing import List, Optional
from sqlmodel import select
from sqlmodel import SQLModel
from mgl.domain.models import Juego
from sqlmodel import Session

class JuegosRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **data) -> Juego:
        juego = Juego(**data)
        self.session.add(juego)
        self.session.commit()
        self.session.refresh(juego)
        return juego

    def get(self, juego_id: int) -> Optional[Juego]:
        return self.session.get(Juego, juego_id)

    def list(
        self,
        q: str | None = None,
        genero: str | None = None,
        plataforma: str | None = None,
        desde: int | None = None,
        hasta: int | None = None,
    ) -> List[Juego]:
        stmt = select(Juego)
        if q:
            like = f"%{q.lower()}%"
            from sqlalchemy import func
            stmt = stmt.where(func.lower(Juego.titulo).like(like))
        if genero:
            stmt = stmt.where(Juego.genero == genero)
        if plataforma:
            stmt = stmt.where(Juego.plataforma == plataforma)
        if desde is not None:
            stmt = stmt.where(Juego.fecha >= desde)
        if hasta is not None:
            stmt = stmt.where(Juego.fecha <= hasta)
        stmt = stmt.order_by(Juego.fecha.desc())
        return list(self.session.exec(stmt))
