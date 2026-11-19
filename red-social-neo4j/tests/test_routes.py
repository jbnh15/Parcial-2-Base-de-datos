import pytest

from app import create_app
from services import amistades_service, personas_service, recomendaciones_service
from services.errors import ConflictError, NotFoundError


@pytest.fixture
def client():
    return create_app().test_client()


def test_crear_persona_devuelve_201(client, monkeypatch):
    monkeypatch.setattr(personas_service, "crear", lambda datos: {"id": "1", **datos.model_dump()})
    r = client.post("/api/personas", json={"nombre": "Ana", "edad": 20, "ciudad": "Mérida"})
    assert r.status_code == 201 and r.json["nombre"] == "Ana"


def test_crear_persona_invalida_devuelve_422(client):
    r = client.post("/api/personas", json={"nombre": "Ana", "edad": 3, "ciudad": "Mérida"})
    assert r.status_code == 422 and r.json["error"] == "Datos inválidos"


def test_persona_inexistente_devuelve_404(client, monkeypatch):
    def no_existe(_):
        raise NotFoundError("No existe")

    monkeypatch.setattr(personas_service, "obtener", no_existe)
    assert client.get("/api/personas/x").status_code == 404


def test_eliminar_devuelve_204(client, monkeypatch):
    monkeypatch.setattr(personas_service, "eliminar", lambda _: None)
    assert client.delete("/api/personas/x").status_code == 204


def test_amistad_repetida_devuelve_409(client, monkeypatch):
    def repetida(_):
        raise ConflictError("ya son amigas")

    monkeypatch.setattr(amistades_service, "crear", repetida)
    r = client.post("/api/amistades", json={"persona_a_id": "a", "persona_b_id": "b"})
    assert r.status_code == 409


def test_amistad_consigo_misma_devuelve_422(client):
    r = client.post("/api/amistades", json={"persona_a_id": "a", "persona_b_id": "a"})
    assert r.status_code == 422


def test_limit_se_acota(client, monkeypatch):
    recibido = {}

    def captura(limite):
        recibido["limite"] = limite
        return []

    monkeypatch.setattr(recomendaciones_service, "mas_conectadas", captura)
    client.get("/api/populares?limit=9999")
    assert recibido["limite"] == 50


def test_camino_sin_parametros_devuelve_422(client):
    assert client.get("/api/camino").status_code == 422


def test_error_de_neo4j_no_filtra_detalle(client, monkeypatch):
    from neo4j.exceptions import ServiceUnavailable

    def cae(*_):
        raise ServiceUnavailable("host secreto.databases.neo4j.io caído")

    monkeypatch.setattr(personas_service, "listar", lambda: cae())
    r = client.get("/api/personas")
    assert r.status_code == 503 and "secreto" not in r.get_data(as_text=True)


def test_index_carga(client):
    assert client.get("/").status_code == 200
