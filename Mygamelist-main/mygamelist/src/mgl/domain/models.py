from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field

class Juego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    plataforma: str
    genero: str
    fecha: int
    puntuacion: int = 0
    portada_url: Optional[str] = None
    descripcion: str = ""

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class Favorito(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    juego_id: int = Field(foreign_key="juego.id", primary_key=True)

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from mgl.domain.database import Base

# Tabla intermedia: relación muchos a muchos (usuarios <-> juegos)
favoritos_table = Table(
    "favoritos",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("game_id", Integer, ForeignKey("games.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    role = Column(String, default="user")  # Nuevo campo para roles

    favoritos = relationship("Game", secondary=favoritos_table, back_populates="usuarios_favoritos")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    release_year = Column(Integer)

    usuarios_favoritos = relationship("User", secondary=favoritos_table, back_populates="favoritos")

