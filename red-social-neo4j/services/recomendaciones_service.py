from typing import Any

from db.neo4j_client import run_query
from services.errors import NotFoundError

MAX_SALTOS_CAMINO = 10  # tope para que shortestPath no recorra todo el grafo


def _exigir_persona(persona_id: str) -> None:
    if not run_query("MATCH (p:Persona {id: $id}) RETURN p.id AS id", id=persona_id):
        raise NotFoundError(f"No existe la persona {persona_id}")


def sugerencias_por_amigos(persona_id: str, limite: int) -> list[dict[str, Any]]:
    """Amigos de amigos que todavía no son amigos, con más amigos en común primero."""
    _exigir_persona(persona_id)
    return run_query(
        """
        MATCH (yo:Persona {id: $id})-[:AMIGO_DE]-(amigo:Persona)-[:AMIGO_DE]-(sug:Persona)
        WHERE sug <> yo AND NOT (yo)-[:AMIGO_DE]-(sug)
        RETURN sug.id AS id, sug.nombre AS nombre,
               count(DISTINCT amigo) AS amigos_en_comun,
               collect(DISTINCT amigo.nombre) AS por_medio_de
        ORDER BY amigos_en_comun DESC, nombre
        LIMIT $limite
        """,
        id=persona_id,
        limite=limite,
    )


def sugerencias_por_intereses(persona_id: str, limite: int) -> list[dict[str, Any]]:
    """Personas con intereses compartidos que todavía no son amigas."""
    _exigir_persona(persona_id)
    return run_query(
        """
        MATCH (yo:Persona {id: $id})-[:INTERESADO_EN]->(i:Interes)<-[:INTERESADO_EN]-(sug:Persona)
        WHERE sug <> yo AND NOT (yo)-[:AMIGO_DE]-(sug)
        RETURN sug.id AS id, sug.nombre AS nombre,
               count(i) AS intereses_en_comun, collect(i.nombre) AS intereses
        ORDER BY intereses_en_comun DESC, nombre
        LIMIT $limite
        """,
        id=persona_id,
        limite=limite,
    )


def camino_mas_corto(desde_id: str, hasta_id: str) -> dict[str, Any]:
    """Cadena de amistades más corta entre dos personas."""
    _exigir_persona(desde_id)
    _exigir_persona(hasta_id)
    if desde_id == hasta_id:  # shortestPath da error si inicio y fin son el mismo nodo
        return {"camino": [], "saltos": 0}
    filas = run_query(
        f"""
        MATCH (a:Persona {{id: $desde}}), (b:Persona {{id: $hasta}})
        MATCH p = shortestPath((a)-[:AMIGO_DE*..{MAX_SALTOS_CAMINO}]-(b))
        RETURN [n IN nodes(p) | n.nombre] AS camino, length(p) AS saltos
        """,
        desde=desde_id,
        hasta=hasta_id,
    )
    if not filas:
        raise NotFoundError(f"No hay camino de hasta {MAX_SALTOS_CAMINO} saltos entre esas personas")
    return filas[0]


def vecindad(persona_id: str) -> list[dict[str, Any]]:
    """Personas a 1 y 2 saltos, con su distancia mínima."""
    _exigir_persona(persona_id)
    return run_query(
        """
        MATCH p = (yo:Persona {id: $id})-[:AMIGO_DE*1..2]-(v:Persona)
        WHERE v <> yo
        RETURN v.id AS id, v.nombre AS nombre, min(length(p)) AS distancia
        ORDER BY distancia, nombre
        """,
        id=persona_id,
    )


def mas_conectadas(limite: int) -> list[dict[str, Any]]:
    return run_query(
        """
        MATCH (p:Persona)
        RETURN p.id AS id, p.nombre AS nombre, COUNT { (p)-[:AMIGO_DE]-() } AS amigos
        ORDER BY amigos DESC, nombre
        LIMIT $limite
        """,
        limite=limite,
    )
