"""set_all_article_prices_to_one

Revision ID: 1f33ee7d86c5
Revises: a232c0166a7e
Create Date: 2026-06-30 14:14:45.468266
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# Identificadores de revision usados por Alembic.
revision: str = '1f33ee7d86c5'
down_revision: Union[str, None] = 'a232c0166a7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE articulo SET precio_unitario = 100.00")


def downgrade() -> None:
    pass
