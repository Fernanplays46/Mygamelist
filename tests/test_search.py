from mgl.services.search import apply_filters

def test_apply_filters_query_and_genero():
    juegos = [
        {"titulo": "Halo", "genero": "FPS", "plataforma": "Xbox", "fecha": 2001},
        {"titulo": "Hollow Knight", "genero": "Metroidvania", "plataforma": "PC", "fecha": 2017},
    ]
    res = apply_filters(juegos, q="ho", genero="Metroidvania")
    assert len(res) == 1
    assert res[0]["titulo"] == "Hollow Knight"
