from __future__ import annotations
from typing import Optional
from sqlmodel import Field, SQLModel


class Juego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    plataforma: str
    genero: str
    fecha: int
    descripcion: str


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Favorito(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    juego_id: int = Field(foreign_key="juego.id", primary_key=True)
