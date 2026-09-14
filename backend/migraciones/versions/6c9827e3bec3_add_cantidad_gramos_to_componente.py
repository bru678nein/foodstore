from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = '6c9827e3bec3'
down_revision: Union[str, None] = 'dfa6644c6960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('componente', sa.Column('cantidad_gramos', sa.Integer(), server_default='0', nullable=False))
    op.add_column('orden', sa.Column('tipo_entrega', sqlmodel.sql.sqltypes.AutoString(length=20), server_default='LOCAL', nullable=False))
    op.alter_column('orden', 'domicilio_id',
               existing_type=sa.INTEGER(),
               nullable=True)

def downgrade() -> None:
    op.alter_column('orden', 'domicilio_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('orden', 'tipo_entrega')
    op.drop_column('componente', 'cantidad_gramos')
