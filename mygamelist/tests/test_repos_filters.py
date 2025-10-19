<<<<<<< HEAD
from pathlib import Path
from mgl.infra.db import get_engine, create_schema, get_session
from mgl.repos.juegos import JuegosRepo


def _seed(session):
    repo = JuegosRepo(session)
    repo.create(titulo="Halo", plataforma="Xbox", genero="FPS", fecha=2001, descripcion="")
    repo.create(titulo="Hollow Knight", plataforma="PC", genero="Metroidvania", fecha=2017, descripcion="")
    repo.create(titulo="Celeste", plataforma="PC", genero="Plataformas", fecha=2018, descripcion="")
    repo.create(titulo="Zelda TOTK", plataforma="Switch", genero="Aventura", fecha=2023, descripcion="")
    return repo


def test_list_by_query_and_platform(tmp_path: Path):
    engine = get_engine(tmp_path / "t.db")
    create_schema(engine)
    try:
        with get_session(engine) as s:
            repo = _seed(s)
            res = repo.list(q="zelda", plataforma="Switch")
            assert len(res) == 1 and res[0].titulo.startswith("Zelda")
    finally:
        engine.dispose()


def test_list_by_year_range(tmp_path: Path):
    engine = get_engine(tmp_path / "t2.db")
    create_schema(engine)
    try:
        with get_session(engine) as s:
            repo = _seed(s)
            res = repo.list(desde=2017, hasta=2018)
            titles = [j.titulo for j in res]
            assert "Hollow Knight" in titles and "Celeste" in titles
            assert all(2017 <= j.fecha <= 2018 for j in res)
    finally:
        engine.dispose()
=======
from pathlib import Path
from mgl.infra.db import get_engine, create_schema, get_session
from mgl.repos.juegos import JuegosRepo


def _seed(session):
    repo = JuegosRepo(session)
    repo.create(titulo="Halo", plataforma="Xbox", genero="FPS", fecha=2001, descripcion="")
    repo.create(titulo="Hollow Knight", plataforma="PC", genero="Metroidvania", fecha=2017, descripcion="")
    repo.create(titulo="Celeste", plataforma="PC", genero="Plataformas", fecha=2018, descripcion="")
    repo.create(titulo="Zelda TOTK", plataforma="Switch", genero="Aventura", fecha=2023, descripcion="")
    return repo


def test_list_by_query_and_platform(tmp_path: Path):
    engine = get_engine(tmp_path / "t.db")
    create_schema(engine)
    try:
        with get_session(engine) as s:
            repo = _seed(s)
            res = repo.list(q="zelda", plataforma="Switch")
            assert len(res) == 1 and res[0].titulo.startswith("Zelda")
    finally:
        engine.dispose()


def test_list_by_year_range(tmp_path: Path):
    engine = get_engine(tmp_path / "t2.db")
    create_schema(engine)
    try:
        with get_session(engine) as s:
            repo = _seed(s)
            res = repo.list(desde=2017, hasta=2018)
            titles = [j.titulo for j in res]
            assert "Hollow Knight" in titles and "Celeste" in titles
            assert all(2017 <= j.fecha <= 2018 for j in res)
    finally:
        engine.dispose()
>>>>>>> f8d9f59 (Subir proyecto MyGameList completo)
