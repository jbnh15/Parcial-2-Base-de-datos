"""Lógica y Cypher de personas e intereses."""

from typing import Any

from db.neo4j_client import run_query
from schemas.personas_schema import InteresIn, PersonaIn, PersonaUpdate
from services.errors import NotFoundError

_CON_INTERESES = """
OPTIONAL MATCH (p)-[:INTERESADO_EN]->(i:Interes)
WITH p, collect(i.nombre) AS intereses
ORDER BY p.nombre
RETURN p{.*, intereses: intereses} AS persona
"""


def listar() -> list[dict[str, Any]]:
    """Todas las personas con la lista de sus intereses."""
    filas = run_query("MATCH (p:Persona)" + _CON_INTERESES)
    return [f["persona"] for f in filas]


def obtener(persona_id: str) -> dict[str, Any]:
    """Una persona con sus intereses. Lanza NotFoundError si no existe."""
    filas = run_query("MATCH (p:Persona {id: $id})" + _CON_INTERESES, id=persona_id)
    if not filas:
        raise NotFoundError(f"No existe la persona {persona_id}")
    return filas[0]["persona"]


def crear(datos: PersonaIn) -> dict[str, Any]:
    """Crea la persona y hace MERGE de sus intereses para compartir un solo nodo por interés."""
    filas = run_query(
        """
        CREATE (p:Persona {id: randomUUID(), nombre: $nombre, edad: $edad, ciudad: $ciudad})
        FOREACH (nombre IN $intereses |
            MERGE (i:Interes {nombre: nombre})
            MERGE (p)-[:INTERESADO_EN]->(i))
        RETURN p{.*, intereses: $intereses} AS persona
        """,
        **datos.model_dump(),
    )
    return filas[0]["persona"]


def actualizar(persona_id: str, cambios: PersonaUpdate) -> dict[str, Any]:
    """Actualiza solo los campos enviados."""
    filas = run_query(
        "MATCH (p:Persona {id: $id}) SET p += $cambios RETURN p.id AS id",
        id=persona_id,
        cambios=cambios.model_dump(exclude_unset=True),
    )
    if not filas:
        raise NotFoundError(f"No existe la persona {persona_id}")
    return obtener(persona_id)


def agregar_interes(persona_id: str, interes: InteresIn) -> dict[str, Any]:
    """MERGE del interés y de la relación, así repetirlo no duplica nada."""
    run_query(
        """
        MATCH (p:Persona {id: $id})
        MERGE (i:Interes {nombre: $nombre})
        MERGE (p)-[:INTERESADO_EN]->(i)
        """,
        id=persona_id,
        nombre=interes.nombre,
    )
    return obtener(persona_id)  # lanza NotFoundError si la persona no existe


def eliminar(persona_id: str) -> None:
    """DETACH DELETE: borra la persona y sus relaciones. Los nodos Interes se conservan."""
    filas = run_query(
        "MATCH (p:Persona {id: $id}) DETACH DELETE p RETURN count(*) AS borradas", id=persona_id
    )
    if not filas or filas[0]["borradas"] == 0:
        raise NotFoundError(f"No existe la persona {persona_id}")
