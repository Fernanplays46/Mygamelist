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

def _engine(db_path: str):
    eng = get_engine(db_path)
    create_schema(eng)
    return eng

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
def export_json(
    out: Path = typer.Option(Path("data/out/games.json"), "--out", help="Ruta del JSON de salida"),
    db: str = typer.Option("mgl.db", "--db", help="Ruta a la base de datos SQLite"),
):
    """Exporta el catálogo a JSON."""
    out.parent.mkdir(parents=True, exist_ok=True)
    engine = _engine(db)
    with get_session(engine) as session:
        items = session.exec(select(Juego)).all()
        payload = [i.model_dump() for i in items]  # SQLModel → dict
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"Export JSON → {out}")

@app.command()
def export_csv(
    out: Path = typer.Option(Path("data/out/games.csv"), "--out", help="Ruta del CSV de salida"),
    db: str = typer.Option("mgl.db", "--db", help="Ruta a la base de datos SQLite"),
):
    """Exporta el catálogo a CSV."""
    out.parent.mkdir(parents=True, exist_ok=True)
    engine = _engine(db)
    with get_session(engine) as session, open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","titulo","plataforma","genero","fecha","descripcion","puntuacion","portada_url"])
        for j in session.exec(select(Juego)).all():
            w.writerow([j.id, j.titulo, j.plataforma, j.genero, j.fecha, j.descripcion, getattr(j, "puntuacion", 0), getattr(j, "portada_url", None)])
    typer.echo(f"Export CSV → {out}")

@app.command()
def import_json(
    src: Path = typer.Argument(..., exists=True, readable=True, help="Ruta del JSON con lista de juegos"),
    db: str = typer.Option("mgl.db", "--db", help="Ruta a la base de datos SQLite"),
):
    """Importa juegos desde un JSON con una lista de objetos Juego."""
    engine = _engine(db)
    data = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        typer.echo("El JSON debe ser una lista de juegos.")
        raise typer.Exit(code=1)
    inserted = 0
    with get_session(engine) as session:
        for row in data:
            # campos mínimos
            try:
                j = Juego(
                    titulo=row["titulo"],
                    plataforma=row["plataforma"],
                    genero=row["genero"],
                    fecha=int(row["fecha"]),
                    descripcion=row.get("descripcion", ""),
                    puntuacion=int(row.get("puntuacion", 0)) if row.get("puntuacion") else 0,
                    portada_url=row.get("portada_url") or None,
                )
            except KeyError as e:
                typer.echo(f"Fila inválida (falta campo): {e}")
                continue
            session.add(j)
            inserted += 1
        session.commit()
    typer.echo(f"Importados {inserted} juegos desde {src} a {db}")

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

def main():
    app()

if __name__ == "__main__":
    main()
