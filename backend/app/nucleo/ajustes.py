from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_RAIZ = Path(__file__).resolve().parent.parent.parent.parent

class Ajustes(BaseSettings):

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "foodstore_new"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/foodstore_new"

    clave_secreta: str = "cambia-esta-clave-minimo-32-caracteres-obligatorio"
    algoritmo: str = "HS256"
    minutos_acceso: int = 30
    dias_renovacion: int = 7

    debug: bool = True
    nombre_app: str = "Food Store API"
    version: str = "1.0.0"
    prefijo_api: str = "/api/v1"
    origenes_cors: str = "http://localhost:5173,http://localhost:3000"

    nube_cdn: str = ""
    api_key_cdn: str = ""
    api_secret_cdn: str = ""
    tamanio_maximo_mb: int = 5

    url_frontend: str = "http://localhost:5173"
    url_api: str = "http://localhost:8000"

    token_mp: str = ""
    clave_publica_mp: str = ""
    secreto_webhook_mp: str = ""

    model_config = SettingsConfigDict(
        env_file=str(_RAIZ / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def origenes_lista(self) -> list[str]:
        return [o.strip() for o in self.origenes_cors.split(",") if o.strip()]

@lru_cache
def obtener_ajustes() -> Ajustes:
    return Ajustes()

ajustes = obtener_ajustes()
