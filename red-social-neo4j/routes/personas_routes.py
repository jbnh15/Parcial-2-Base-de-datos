from flask import Blueprint, jsonify, request

from schemas.personas_schema import InteresIn, PersonaIn, PersonaUpdate
from services import personas_service

bp = Blueprint("personas", __name__, url_prefix="/api/personas")


def _json() -> dict:
    return request.get_json(silent=True) or {}


@bp.get("")
def listar():
    return jsonify(personas_service.listar())


@bp.post("")
def crear():
    return jsonify(personas_service.crear(PersonaIn.model_validate(_json()))), 201


@bp.get("/<persona_id>")
def obtener(persona_id: str):
    return jsonify(personas_service.obtener(persona_id))


@bp.put("/<persona_id>")
def actualizar(persona_id: str):
    return jsonify(personas_service.actualizar(persona_id, PersonaUpdate.model_validate(_json())))


@bp.delete("/<persona_id>")
def eliminar(persona_id: str):
    personas_service.eliminar(persona_id)
    return "", 204


@bp.post("/<persona_id>/intereses")
def agregar_interes(persona_id: str):
    persona = personas_service.agregar_interes(persona_id, InteresIn.model_validate(_json()))
    return jsonify(persona), 201
