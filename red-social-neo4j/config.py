import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str


def get_settings() -> Settings:
    """Lee las credenciales del entorno y falla con un mensaje claro si falta alguna."""
    load_dotenv()
    nombres = ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD")
    faltantes = [n for n in nombres if not os.getenv(n)]
    if faltantes:
        raise RuntimeError(f"Faltan variables de entorno: {', '.join(faltantes)}. Revisa tu .env")
    return Settings(*(os.environ[n] for n in nombres))
