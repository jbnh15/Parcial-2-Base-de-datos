# Personas

Base: `/api/personas`. Sin autenticación (proyecto académico).

## GET /api/personas
Lista todas las personas con sus intereses, ordenadas por nombre. `200`.
Cypher: `MATCH (p:Persona) ... collect(i.nombre)`.

## POST /api/personas
Crea una persona y sus intereses. Los nodos `Interes` se reutilizan con `MERGE`.
```json
{"nombre": "Ana", "edad": 21, "ciudad": "Mérida", "intereses": ["Cine", "Música"]}
```
- `201` persona creada con su `id` (UUID generado en Neo4j).
- `422` datos inválidos: edad fuera de 13 a 120, textos vacíos o campos extra.

## GET /api/personas/{id}
`200` persona con intereses. `404` si no existe.

## PUT /api/personas/{id}
Actualiza `nombre`, `edad` o `ciudad` (al menos uno, no acepta `null`). `SET p += $cambios`.
`200` persona actualizada, `404`, `422`.

## DELETE /api/personas/{id}
`DETACH DELETE`: borra la persona y todas sus amistades e intereses vinculados. Los nodos `Interes` quedan. `204` o `404`.

## POST /api/personas/{id}/intereses
```json
{"nombre": "Fotografía"}
```
`MERGE` del interés y de la relación `INTERESADO_EN`, así que repetirlo no duplica. `201` persona actualizada, `404`, `422`.

## Errores comunes
`503` si AuraDB no responde. El detalle queda en el log del servidor, no en la respuesta.
