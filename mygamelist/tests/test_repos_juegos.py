from pathlib import Path
from mgl.infra.db import get_engine, create_schema, get_session
from mgl.repos.juegos import JuegosRepo
from mgl.domain.models import Juego

def test_repo_insert_and_get(tmp_path: Path):
    engine = get_engine(tmp_path / "test.db")
    create_schema(engine)
    with get_session(engine) as session:
        repo = JuegosRepo(session)
        j = repo.create(titulo="Celeste", plataforma="PC", genero="Plataformas", fecha=2018, descripcion="Indie top")
        got = repo.get(j.id)
        assert got is not None
        assert got.titulo == "Celeste"
