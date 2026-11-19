from flask import Blueprint, jsonify, request

from schemas.personas_schema import AmistadIn
from services import amistades_service

bp = Blueprint("amistades", __name__, url_prefix="/api")


@bp.get("/personas/<persona_id>/amigos")
def listar_amigos(persona_id: str):
    return jsonify(amistades_service.listar_amigos(persona_id))


@bp.post("/amistades")
def crear():
    datos = AmistadIn.model_validate(request.get_json(silent=True) or {})
    return jsonify(amistades_service.crear(datos)), 201


@bp.delete("/amistades/<persona_a_id>/<persona_b_id>")
def eliminar(persona_a_id: str, persona_b_id: str):
    amistades_service.eliminar(persona_a_id, persona_b_id)
    return "", 204
