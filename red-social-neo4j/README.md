# Red social en grafo (Flask + Neo4j AuraDB)

Parcial 2 de Base de Datos Avanzada. App en Python y Flask conectada a una instancia **Neo4j AuraDB** en la nube. Modela personas, amistades e intereses como grafo, con CRUD completo y consultas de recomendación y de caminos.

## Requerimientos
- Python 3.11 o superior y [uv](https://docs.astral.sh/uv/) (o pip)
- Una instancia gratuita de AuraDB: <https://console.neo4j.io> (crea una *AuraDB Free* y guarda la contraseña que te muestra una sola vez)

## Instalación
```bash
uv venv .venv
make install                 # instala dependencias en .venv
cp .env.example .env         # y rellena NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD
```
Las credenciales viven solo en `.env` (ignorado por git). La app falla al arrancar con un mensaje claro si falta alguna.

## Ejecución
```bash
make seed    # crea constraints y carga datos de ejemplo (ficticios, idempotente)
make run     # http://127.0.0.1:5000
```
Si la instancia Free estuvo inactiva, AuraDB la pausa: reactívala desde la consola antes de correr el seed.

## Datos de ejemplo
`seed/seed.py` carga 14 personas y 17 amistades **inventadas para la demo**, repartidas en tres grupos de ciudades conectados por dos puentes. No son datos reales.

## Estructura
```
app.py            crea la app y mapea errores a HTTP
config.py         variables de entorno
db/               driver único de Neo4j
routes/           endpoints (solo HTTP)
services/         lógica y todo el Cypher
schemas/          validación de entrada con Pydantic
seed/             constraints y datos iniciales
tests/            pytest, sin tocar la nube
docs/api/         un archivo por recurso
```

## Verificación
```bash
make check   # ruff + pytest
```
La API está documentada en `docs/api/`.
