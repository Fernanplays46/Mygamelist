"""Funciones puras de filtrado/búsqueda (para tests rápidos)."""

from __future__ import annotations

from typing import Iterable, List, Dict, Any

def apply_filters(juegos: Iterable[dict], q: str | None = None, genero: str | None = None, plataforma: str | None = None, desde: int | None = None, hasta: int | None = None) -> List[dict]:
    res: List[dict] = []
    for j in juegos:
        if q and q.lower() not in j["titulo"].lower():
            continue
        if genero and j["genero"] != genero:
            continue
        if plataforma and j["plataforma"] != plataforma:
            continue
        if desde is not None and j["fecha"] < desde:
            continue
        if hasta is not None and j["fecha"] > hasta:
            continue
        res.append(j)
    return res
