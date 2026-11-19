from flask import Blueprint, jsonify, request
from pydantic import TypeAdapter

from schemas.personas_schema import Texto80
from services import recomendaciones_service as svc

bp = Blueprint("recomendaciones", __name__, url_prefix="/api")

LIMITE_DEFECTO, LIMITE_MAX = 10, 50
_id_valido = TypeAdapter(Texto80)


def _limite() -> int:
    pedido = request.args.get("limit", LIMITE_DEFECTO, type=int)
    return max(1, min(pedido, LIMITE_MAX))


@bp.get("/personas/<persona_id>/sugerencias/amigos")
def por_amigos(persona_id: str):
    return jsonify(svc.sugerencias_por_amigos(persona_id, _limite()))


@bp.get("/personas/<persona_id>/sugerencias/intereses")
def por_intereses(persona_id: str):
    return jsonify(svc.sugerencias_por_intereses(persona_id, _limite()))


@bp.get("/personas/<persona_id>/vecindad")
def vecindad(persona_id: str):
    return jsonify(svc.vecindad(persona_id))


@bp.get("/camino")
def camino():
    desde = _id_valido.validate_python(request.args.get("desde", ""))
    hasta = _id_valido.validate_python(request.args.get("hasta", ""))
    return jsonify(svc.camino_mas_corto(desde, hasta))


@bp.get("/populares")
def populares():
    return jsonify(svc.mas_conectadas(_limite()))
