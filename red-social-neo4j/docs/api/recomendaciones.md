# Recomendaciones y consultas de grafo

Todas son `GET`, parametrizadas y de solo lectura. `limit` va de 1 a 50 (por defecto 10). `404` si la persona no existe.

| Endpoint | Qué devuelve | Patrón Cypher |
|---|---|---|
| `/api/personas/{id}/sugerencias/amigos` | Amigos de amigos que aún no son amigos: `id, nombre, amigos_en_comun, por_medio_de` | `(yo)-[:AMIGO_DE]-(amigo)-[:AMIGO_DE]-(sug) WHERE NOT (yo)-[:AMIGO_DE]-(sug)` |
| `/api/personas/{id}/sugerencias/intereses` | Personas con intereses en común que no son amigas | `(yo)-[:INTERESADO_EN]->(i)<-[:INTERESADO_EN]-(sug)` |
| `/api/personas/{id}/vecindad` | Personas a 1 y 2 saltos con su `distancia` | `[:AMIGO_DE*1..2]` con `min(length(p))` |
| `/api/camino?desde={id}&hasta={id}` | `{camino: [nombres], saltos}` | `shortestPath((a)-[:AMIGO_DE*..10]-(b))` |
| `/api/populares` | Personas por número de amigos | `COUNT { (p)-[:AMIGO_DE]-() }` |

## Casos de borde
- `/camino` con el mismo id en ambos extremos devuelve `{camino: [], saltos: 0}` (shortestPath daría error con nodos iguales).
- `/camino` sin ruta de hasta 10 saltos devuelve `404`. Sin `desde` o `hasta`, `422`.
