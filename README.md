# Parcial 2 Base de Datos Avanzadas

José Bernardo Noguera Hernandez

Red social en grafo con Python, Flask y Neo4j AuraDB (base de datos en la nube). Permite hacer CRUD de personas y amistades, y consultar recomendaciones de amigos, intereses en común y el camino más corto entre dos personas.

El código está en la carpeta `red-social-neo4j/`.

## Requisitos
- Python 3.11 o superior y [uv](https://docs.astral.sh/uv/)
- Una instancia gratuita de Neo4j AuraDB (https://console.neo4j.io)

## Cómo correrlo
```bash
cd red-social-neo4j
uv venv .venv
make install
cp .env.example .env    # y pon NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD
make seed               # aplica seed/schema.cypher y carga datos de ejemplo (ficticios)
make run                # http://127.0.0.1:5000
```

La documentación de la API está en `red-social-neo4j/docs/api/`.
