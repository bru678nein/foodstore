from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

revision: str = 'dfa6644c6960'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_table('articulo_rubro')
    op.drop_index(op.f('ix_rubro_etiqueta'), table_name='rubro')
    op.drop_table('rubro')
    op.add_column('articulo', sa.Column('unidad_venta_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'articulo', 'unidad_medida', ['unidad_venta_id'], ['id'])
    op.add_column('cobro', sa.Column('mp_status_detail', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True))
    op.add_column('cobro', sa.Column('transaction_amount', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('cobro', sa.Column('payment_method_id', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True))
    op.add_column('composicion_articulo', sa.Column('cantidad', sa.Numeric(precision=10, scale=3), nullable=False, server_default='1.000'))
    op.add_column('composicion_articulo', sa.Column('unidad_medida_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'composicion_articulo', 'unidad_medida', ['unidad_medida_id'], ['id'])
    op.add_column('orden', sa.Column('forma_pago_codigo', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='EFECTIVO'))
    op.add_column('orden', sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'))
    op.add_column('orden', sa.Column('descuento', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'))
    op.add_column('orden', sa.Column('costo_envio', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'))
    op.add_column('orden', sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'))
    op.drop_column('orden', 'monto_total')
    op.add_column('partida_orden', sa.Column('subtotal_snap', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'))
    op.drop_column('partida_orden', 'importe_parcial')

def downgrade() -> None:
    op.add_column('partida_orden', sa.Column('importe_parcial', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.drop_column('partida_orden', 'subtotal_snap')
    op.add_column('orden', sa.Column('monto_total', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.drop_column('orden', 'total')
    op.drop_column('orden', 'costo_envio')
    op.drop_column('orden', 'descuento')
    op.drop_column('orden', 'subtotal')
    op.drop_column('orden', 'forma_pago_codigo')
    op.drop_constraint(None, 'composicion_articulo', type_='foreignkey')
    op.drop_column('composicion_articulo', 'unidad_medida_id')
    op.drop_column('composicion_articulo', 'cantidad')
    op.drop_column('cobro', 'payment_method_id')
    op.drop_column('cobro', 'transaction_amount')
    op.drop_column('cobro', 'mp_status_detail')
    op.drop_constraint(None, 'articulo', type_='foreignkey')
    op.drop_column('articulo', 'unidad_venta_id')
    op.create_table('articulo_rubro',
    sa.Column('articulo_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rubro_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['articulo_id'], ['articulo.id'], name=op.f('articulo_rubro_articulo_id_fkey')),
    sa.ForeignKeyConstraint(['rubro_id'], ['rubro.id'], name=op.f('articulo_rubro_rubro_id_fkey')),
    sa.PrimaryKeyConstraint('articulo_id', 'rubro_id', name=op.f('articulo_rubro_pkey'))
    )
    op.create_table('rubro',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('etiqueta', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('descripcion', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('imagen_url', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('imagen_id_cdn', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('padre_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('eliminado_en', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['padre_id'], ['rubro.id'], name=op.f('rubro_padre_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('rubro_pkey'))
    )
    op.create_index(op.f('ix_rubro_etiqueta'), 'rubro', ['etiqueta'], unique=False)
