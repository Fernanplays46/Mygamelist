from __future__ import annotations

import csv
from pathlib import Path
import subprocess
import sys
import time

import typer
from sqlmodel import Session

from mgl.infra.db import get_engine, create_schema, get_session
from mgl.domain.models import Juego

app = typer.Typer(help="MyGameList CLI")

@app.command()
def seed(csv_path: Path = typer.Argument(..., exists=True, readable=True)):
    """Carga juegos desde CSV (cabeceras: titulo,plataforma,genero,fecha,descripcion)."""
    engine = get_engine("mgl.db")
    create_schema(engine)
    inserted = 0
    with get_session(engine) as session, open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            j = Juego(
                titulo=row["titulo"],
                plataforma=row["plataforma"],
                genero=row["genero"],
                fecha=int(row["fecha"]),
                descripcion=row.get("descripcion", ""),
            )
            session.add(j)
            inserted += 1
        session.commit()
    typer.echo(f"Insertados {inserted} juegos en mgl.db")

@app.command()
def demo():
    """Lanza una demo mínima (prepara DB y muestra 3 llamadas ejemplo)."""
    if not Path("mgl.db").exists():
        typer.echo("No existe mgl.db, ejecuta primero: python -m mgl.cli seed data/seed/games.csv")
        raise typer.Exit(code=1)
    typer.echo("Iniciando API en http://127.0.0.1:8000 ... (Ctrl+C para parar)")
    typer.echo('Ejemplos:')
    typer.echo('  1) Listado con búsqueda: curl "http://127.0.0.1:8000/juegos?q=zelda"')
    typer.echo('  2) Crear juego: curl -X POST http://127.0.0.1:8000/juegos -H "Content-Type: application/json" -d "{\"titulo\":\"Celeste\",\"plataforma\":\"PC\",\"genero\":\"Plataformas\",\"fecha\":2018,\"descripcion\":\"Indie top\"}"')
    typer.echo('  3) Favorito: curl -X POST http://127.0.0.1:8000/favoritos/1 && curl http://127.0.0.1:8000/favoritos')
    # Ejecuta uvicorn inline
    subprocess.run([sys.executable, "-m", "uvicorn", "mgl.api:app", "--reload"])

if __name__ == "__main__":
    app()
