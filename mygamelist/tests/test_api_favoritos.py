from fastapi.testclient import TestClient
from mgl.api import app

def test_favoritos_flow():
    client = TestClient(app)

    # 1) Crear juego vía API (usa la misma DB global que la app)
    nuevo = {
        "titulo": "Celeste",
        "plataforma": "PC",
        "genero": "Plataformas",
        "fecha": 2018,
        "descripcion": "",
    }
    r = client.post("/juegos", json=nuevo)
    assert r.status_code == 201
    jid = r.json()["id"]

    # 2) Buscarlo
    r = client.get("/juegos", params={"q": "Celeste"})
    assert r.status_code == 200
    assert any(j["id"] == jid for j in r.json())

    # 3) Añadir a favoritos y comprobar
    assert client.post(f"/favoritos/{jid}").status_code == 204
    r = client.get("/favoritos")
    assert r.status_code == 200
    assert any(j["id"] == jid for j in r.json())
