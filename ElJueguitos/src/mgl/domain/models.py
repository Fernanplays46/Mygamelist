from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field

# === Tabla Juegos ===
class Juego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    plataforma: str
    genero: str
    fecha: int
    puntuacion: int = 0
    portada_url: Optional[str] = None
    descripcion: str = ""

# === Tabla Usuarios para login ===
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

# === Tabla Favoritos (usuario -> juego) ===
class Favorito(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="user.id", primary_key=True)
    juego_id: int = Field(foreign_key="juego.id", primary_key=True)
