"""Entorno de ejecucion de Alembic para Food Store API."""
from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from app.nucleo.ajustes import ajustes

# Importa todas las entidades para poblar SQLModel.metadata.
from app.persistencia import entidades  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", ajustes.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def ejecutar_migraciones_offline() -> None:
    """Ejecuta las migraciones en modo offline (sin conexion viva)."""
    context.configure(
        url=ajustes.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def ejecutar_migraciones_online() -> None:
    """Ejecuta las migraciones con una conexion activa."""
    from sqlalchemy import engine_from_config, pool

    seccion = config.get_section(config.config_ini_section, {})
    seccion["sqlalchemy.url"] = ajustes.database_url
    motor = engine_from_config(
        seccion, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with motor.connect() as conexion:
        context.configure(
            connection=conexion,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    ejecutar_migraciones_offline()
else:
    ejecutar_migraciones_online()
