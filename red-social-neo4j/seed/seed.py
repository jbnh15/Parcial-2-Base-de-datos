"""Crea constraints y carga datos de EJEMPLO (personas ficticias inventadas para la demo).

Es idempotente: usa MERGE con ids fijos, así que se puede correr varias veces sin duplicar.
Uso: python -m seed.seed
"""

from db.neo4j_client import get_driver, run_query

# id, nombre, edad, ciudad, intereses
PERSONAS = [
    ("p01", "Ana Cetina", 21, "Mérida", ["Fútbol", "Música", "Cine"]),
    ("p02", "Luis Pech", 22, "Mérida", ["Videojuegos", "Programación"]),
    ("p03", "Carla Uc", 20, "Mérida", ["Cine", "Fotografía", "Viajes"]),
    ("p04", "Diego Canul", 23, "Mérida", ["Programación", "Anime", "Música"]),
    ("p05", "Sofía Balam", 21, "Mérida", ["Cocina", "Viajes"]),
    ("p06", "Mateo Ríos", 24, "Ciudad de México", ["Fútbol", "Programación"]),
    ("p07", "Valeria Soto", 22, "Ciudad de México", ["Música", "Cine", "Fotografía"]),
    ("p08", "Andrés Luna", 25, "Ciudad de México", ["Videojuegos", "Anime"]),
    ("p09", "Camila Vega", 21, "Ciudad de México", ["Senderismo", "Viajes"]),
    ("p10", "Hugo Garza", 23, "Monterrey", ["Fútbol", "Senderismo"]),
    ("p11", "Regina Treviño", 22, "Monterrey", ["Cocina", "Música"]),
    ("p12", "Pablo Ibarra", 24, "Guadalajara", ["Programación", "Videojuegos"]),
    ("p13", "Daniela Ochoa", 20, "Guadalajara", ["Fotografía", "Cine"]),
    ("p14", "Emilio Ruiz", 26, "Guadalajara", ["Fútbol", "Cocina", "Anime"]),
]

# Pares de ids, se guardan en un solo sentido. p04-p06 y p09-p10 unen las tres ciudades.
AMISTADES = [
    ("p01", "p02", "2023-02-10"), ("p01", "p03", "2023-03-01"), ("p02", "p03", "2023-03-15"),
    ("p02", "p04", "2023-05-20"), ("p03", "p05", "2023-06-02"), ("p04", "p05", "2023-09-12"),
    ("p06", "p07", "2022-11-05"), ("p06", "p08", "2022-12-18"), ("p07", "p09", "2023-01-22"),
    ("p08", "p09", "2023-04-09"), ("p10", "p11", "2023-07-30"), ("p10", "p12", "2023-08-14"),
    ("p11", "p13", "2023-10-03"), ("p12", "p14", "2023-10-21"), ("p13", "p14", "2023-11-11"),
    ("p04", "p06", "2024-01-15"), ("p09", "p10", "2024-02-27"),
]  # fmt: skip


def cargar() -> None:
    run_query("CREATE CONSTRAINT persona_id IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE")
    run_query(
        "CREATE CONSTRAINT interes_nombre IF NOT EXISTS FOR (i:Interes) REQUIRE i.nombre IS UNIQUE"
    )
    run_query(
        """
        UNWIND $personas AS fila
        MERGE (p:Persona {id: fila.id})
          SET p.nombre = fila.nombre, p.edad = fila.edad, p.ciudad = fila.ciudad
        WITH p, fila
        UNWIND fila.intereses AS nombre
        MERGE (i:Interes {nombre: nombre})
        MERGE (p)-[:INTERESADO_EN]->(i)
        """,
        personas=[
            {"id": i, "nombre": n, "edad": e, "ciudad": c, "intereses": ints}
            for i, n, e, c, ints in PERSONAS
        ],
    )
    run_query(
        """
        UNWIND $amistades AS fila
        MATCH (a:Persona {id: fila.a}), (b:Persona {id: fila.b})
        MERGE (a)-[r:AMIGO_DE]-(b)
          ON CREATE SET r.desde = date(fila.desde)
        """,
        amistades=[{"a": a, "b": b, "desde": d} for a, b, d in AMISTADES],
    )


if __name__ == "__main__":
    cargar()
    resumen = run_query(
        "MATCH (p:Persona) WITH count(p) AS personas "
        "MATCH ()-[r:AMIGO_DE]->() RETURN personas, count(r) AS amistades"
    )[0]
    print(f"Listo: {resumen['personas']} personas y {resumen['amistades']} amistades en la nube")
    get_driver().close()
