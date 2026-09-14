"""add_unidad_to_componente

Revision ID: a232c0166a7e
Revises: b2c3d4e5f6a7
Create Date: 2026-06-30 05:40:17.648206
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# Identificadores de revision usados por Alembic.
revision: str = 'a232c0166a7e'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Usar VARCHAR + CHECK para evitar conflictos con tipos enum pre-existentes
    op.add_column('componente', sa.Column(
        'precio_unitario',
        sa.Numeric(precision=10, scale=2),
        nullable=False,
        server_default='0.00',
    ))
    op.add_column('componente', sa.Column(
        'unidad',
        sa.String(length=2),
        nullable=False,
        server_default='g',
    ))
    op.create_check_constraint(
        'ck_componente_unidad',
        'componente',
        "unidad IN ('ml', 'l', 'g', 'kg')",
    )


def downgrade() -> None:
    op.drop_constraint('ck_componente_unidad', 'componente', type_='check')
    op.drop_column('componente', 'unidad')
    op.drop_column('componente', 'precio_unitario')
