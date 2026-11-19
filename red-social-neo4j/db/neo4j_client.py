"""Cliente único de Neo4j: un solo driver compartido y un helper para ejecutar Cypher parametrizado."""

from functools import lru_cache
from typing import Any

from neo4j import Driver, GraphDatabase

from config import get_settings


@lru_cache(maxsize=1)
def get_driver() -> Driver:
    """Crea el driver una sola vez y comprueba la conexión. Falla rápido si las credenciales son malas."""
    s = get_settings()
    driver = GraphDatabase.driver(s.neo4j_uri, auth=(s.neo4j_user, s.neo4j_password))
    driver.verify_connectivity()
    return driver


def run_query(query: str, **params: Any) -> list[dict[str, Any]]:
    """Ejecuta Cypher parametrizado y devuelve cada fila como dict."""
    records, _, _ = get_driver().execute_query(query, parameters_=params)
    return [r.data() for r in records]
