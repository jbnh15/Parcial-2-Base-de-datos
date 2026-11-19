"""Lógica y Cypher de amistades. AMIGO_DE se guarda en un sentido y se consulta sin dirección."""

from typing import Any

from db.neo4j_client import run_query
from schemas.personas_schema import AmistadIn
from services.errors import ConflictError, NotFoundError


def listar_amigos(persona_id: str) -> list[dict[str, Any]]:
    """Amigos de una persona con la fecha de amistad."""
    existe = run_query("MATCH (p:Persona {id: $id}) RETURN p.id AS id", id=persona_id)
    if not existe:
        raise NotFoundError(f"No existe la persona {persona_id}")
    return run_query(
        """
        MATCH (:Persona {id: $id})-[r:AMIGO_DE]-(f:Persona)
        RETURN f.id AS id, f.nombre AS nombre, toString(r.desde) AS desde
        ORDER BY nombre
        """,
        id=persona_id,
    )


def crear(datos: AmistadIn) -> dict[str, Any]:
    # MERGE sin dirección: si ya existe en cualquier sentido no se duplica
    """Crea la amistad con MERGE sin dirección, para no duplicarla si ya existe al revés."""
    filas = run_query(
        """
        MATCH (a:Persona {id: $a}), (b:Persona {id: $b})
        OPTIONAL MATCH (a)-[previa:AMIGO_DE]-(b)
        WITH a, b, previa IS NOT NULL AS ya_existia
        MERGE (a)-[r:AMIGO_DE]-(b)
          ON CREATE SET r.desde = date($desde)
        RETURN a.nombre AS persona_a, b.nombre AS persona_b,
               toString(r.desde) AS desde, ya_existia
        """,
        a=datos.persona_a_id,
        b=datos.persona_b_id,
        desde=datos.desde.isoformat(),
    )
    if not filas:
        raise NotFoundError("Alguna de las dos personas no existe")
    if filas[0].pop("ya_existia"):
        raise ConflictError("Esas dos personas ya son amigas")
    return filas[0]


def eliminar(persona_a_id: str, persona_b_id: str) -> None:
    """Borra la amistad sin importar en qué sentido se guardó."""
    filas = run_query(
        """
        MATCH (:Persona {id: $a})-[r:AMIGO_DE]-(:Persona {id: $b})
        DELETE r
        RETURN count(*) AS borradas
        """,
        a=persona_a_id,
        b=persona_b_id,
    )
    if filas[0]["borradas"] == 0:
        raise NotFoundError("Esa amistad no existe")
