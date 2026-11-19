// Script de base de datos: restricciones de unicidad (cada una crea su índice).
// Se puede pegar completo en Neo4j Browser, o lo aplica seed/seed.py. Es idempotente.

CREATE CONSTRAINT persona_id IF NOT EXISTS
FOR (p:Persona) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT interes_nombre IF NOT EXISTS
FOR (i:Interes) REQUIRE i.nombre IS UNIQUE;
