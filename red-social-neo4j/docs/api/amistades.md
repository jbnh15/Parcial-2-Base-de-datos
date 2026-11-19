# Amistades

La relación `AMIGO_DE` se guarda en un solo sentido y se consulta sin dirección, así que es simétrica.

## GET /api/personas/{id}/amigos
`200` lista `[{id, nombre, desde}]` ordenada por nombre. `404` si la persona no existe.

## POST /api/amistades
```json
{"persona_a_id": "p01", "persona_b_id": "p05", "desde": "2024-05-01"}
```
`desde` es opcional (por defecto, hoy). `MERGE (a)-[:AMIGO_DE]-(b)` sin dirección evita duplicar la amistad aunque exista en el sentido contrario.
- `201` `{persona_a, persona_b, desde}`
- `404` alguna persona no existe
- `409` ya eran amigas
- `422` mismo id en ambos campos o formato inválido

## DELETE /api/amistades/{a}/{b}
Borra la relación sin importar su sentido. `204` o `404` si no existía.
