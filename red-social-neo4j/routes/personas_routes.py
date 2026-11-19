"""Endpoints de personas e intereses. Solo HTTP: validan la entrada y delegan en services/. Ver docs/api/personas.md."""

from flask import Blueprint, jsonify, request

from schemas.personas_schema import InteresIn, PersonaIn, PersonaUpdate
from services import personas_service

bp = Blueprint("personas", __name__, url_prefix="/api/personas")


def _json() -> dict:
    return request.get_json(silent=True) or {}


@bp.get("")
def listar():
    """GET /api/personas: lista todas las personas con sus intereses."""
    return jsonify(personas_service.listar())


@bp.post("")
def crear():
    """POST /api/personas: crea una persona y sus intereses."""
    return jsonify(personas_service.crear(PersonaIn.model_validate(_json()))), 201


@bp.get("/<persona_id>")
def obtener(persona_id: str):
    """GET /api/personas/<id>: una persona o 404."""
    return jsonify(personas_service.obtener(persona_id))


@bp.put("/<persona_id>")
def actualizar(persona_id: str):
    """PUT /api/personas/<id>: actualiza nombre, edad o ciudad."""
    return jsonify(personas_service.actualizar(persona_id, PersonaUpdate.model_validate(_json())))


@bp.delete("/<persona_id>")
def eliminar(persona_id: str):
    """DELETE /api/personas/<id>: borra la persona y todas sus relaciones."""
    personas_service.eliminar(persona_id)
    return "", 204


@bp.post("/<persona_id>/intereses")
def agregar_interes(persona_id: str):
    """POST /api/personas/<id>/intereses: agrega un interés sin duplicarlo."""
    persona = personas_service.agregar_interes(persona_id, InteresIn.model_validate(_json()))
    return jsonify(persona), 201
