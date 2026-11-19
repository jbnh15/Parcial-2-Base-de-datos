import pytest

from schemas.personas_schema import AmistadIn
from services import amistades_service, personas_service, recomendaciones_service
from services.errors import ConflictError, NotFoundError


def fake(monkeypatch, modulo, filas):
    """Reemplaza run_query del módulo y guarda las llamadas hechas."""
    llamadas = []

    def run_query(query, **params):
        llamadas.append((query, params))
        return filas

    monkeypatch.setattr(modulo, "run_query", run_query)
    return llamadas


def test_obtener_inexistente_lanza_not_found(monkeypatch):
    fake(monkeypatch, personas_service, [])
    with pytest.raises(NotFoundError):
        personas_service.obtener("x")


def test_eliminar_sin_filas_borradas_lanza_not_found(monkeypatch):
    fake(monkeypatch, personas_service, [{"borradas": 0}])
    with pytest.raises(NotFoundError):
        personas_service.eliminar("x")


def test_amistad_repetida_lanza_conflict(monkeypatch):
    fila = {"persona_a": "A", "persona_b": "B", "desde": "2024-01-01", "ya_existia": True}
    fake(monkeypatch, amistades_service, [fila])
    with pytest.raises(ConflictError):
        amistades_service.crear(AmistadIn(persona_a_id="a", persona_b_id="b"))


def test_amistad_nueva_no_expone_bandera_interna(monkeypatch):
    fila = {"persona_a": "A", "persona_b": "B", "desde": "2024-01-01", "ya_existia": False}
    fake(monkeypatch, amistades_service, [fila])
    resultado = amistades_service.crear(AmistadIn(persona_a_id="a", persona_b_id="b"))
    assert "ya_existia" not in resultado


def test_amistad_con_persona_inexistente(monkeypatch):
    fake(monkeypatch, amistades_service, [])
    with pytest.raises(NotFoundError):
        amistades_service.crear(AmistadIn(persona_a_id="a", persona_b_id="b"))


def test_camino_a_si_misma_no_consulta_shortest_path(monkeypatch):
    llamadas = fake(monkeypatch, recomendaciones_service, [{"id": "p01"}])
    assert recomendaciones_service.camino_mas_corto("p01", "p01") == {"camino": [], "saltos": 0}
    assert all("shortestPath" not in q for q, _ in llamadas)


def test_camino_inexistente_lanza_not_found(monkeypatch):
    def run_query(query, **params):
        return [] if "shortestPath" in query else [{"id": "ok"}]

    monkeypatch.setattr(recomendaciones_service, "run_query", run_query)
    with pytest.raises(NotFoundError):
        recomendaciones_service.camino_mas_corto("a", "b")


def test_sugerencias_pasan_parametros_sin_concatenar(monkeypatch):
    llamadas = fake(monkeypatch, recomendaciones_service, [{"id": "p01"}])
    recomendaciones_service.sugerencias_por_amigos("p01'; MATCH (n) DETACH DELETE n //", 5)
    query, params = llamadas[-1]
    assert "DETACH" not in query and params["limite"] == 5
