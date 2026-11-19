from flask import Flask, jsonify, render_template
from neo4j.exceptions import DriverError, Neo4jError
from pydantic import ValidationError

from routes import amistades_routes, personas_routes, recomendaciones_routes
from services.errors import ConflictError, NotFoundError


def create_app() -> Flask:
    app = Flask(__name__)
    for modulo in (personas_routes, amistades_routes, recomendaciones_routes):
        app.register_blueprint(modulo.bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(ValidationError)
    def entrada_invalida(e: ValidationError):
        detalle = e.errors(include_url=False, include_context=False, include_input=False)
        return jsonify(error="Datos inválidos", detalle=detalle), 422

    @app.errorhandler(NotFoundError)
    def no_encontrado(e: NotFoundError):
        return jsonify(error=str(e)), 404

    @app.errorhandler(ConflictError)
    def conflicto(e: ConflictError):
        return jsonify(error=str(e)), 409

    @app.errorhandler(Neo4jError)
    @app.errorhandler(DriverError)
    def base_no_disponible(e: Exception):
        app.logger.exception("Error de Neo4j")  # el detalle queda en el log, no en la respuesta
        return jsonify(error="La base de datos no está disponible, intenta de nuevo"), 503

    return app


app = create_app()
