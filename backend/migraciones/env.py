"""Punto de entrada requerido por Alembic — la logica real esta en entorno.py."""
# Alembic busca este nombre fijo; el contenido original vive en entorno.py.
from migraciones.entorno import *  # noqa: F401, F403
