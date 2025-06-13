"""agregar fecha_nacimiento a formularios_ingreso

Revision ID: 40c589ffbc23
Revises: de988d2a807f
Create Date: 2025-06-06 09:01:46.001938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c589ffbc23'
down_revision: Union[str, None] = 'de988d2a807f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar la columna fecha_nacimiento
    op.add_column('formularios_ingreso', sa.Column('fecha_nacimiento', sa.Date(), nullable=False, server_default='2025-01-01'))
    # Omitir estatura porque ya existe
    # op.add_column('formularios_ingreso', sa.Column('estatura', sa.Integer(), nullable=False, server_default='0'))
    # Agregar las otras columnas si no existen
    if not column_exists('formularios_ingreso', 'edad_gestacional_nacimiento'):
        op.add_column('formularios_ingreso', sa.Column('edad_gestacional_nacimiento', sa.Integer(), nullable=False, server_default='0'))
    if not column_exists('formularios_ingreso', 'tipo_alimentacion'):
        op.add_column('formularios_ingreso', sa.Column('tipo_alimentacion', sa.String(), nullable=False, server_default='Lactancia exclusiva'))
    if not column_exists('formularios_ingreso', 'condicion_medica_bebe'):
        op.add_column('formularios_ingreso', sa.Column('condicion_medica_bebe', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar las columnas agregadas
    op.drop_column('formularios_ingreso', 'fecha_nacimiento')
    # Omitir estatura porque ya existía antes de esta migración
    # op.drop_column('formularios_ingreso', 'estatura')
    if column_exists('formularios_ingreso', 'edad_gestacional_nacimiento'):
        op.drop_column('formularios_ingreso', 'edad_gestacional_nacimiento')
    if column_exists('formularios_ingreso', 'tipo_alimentacion'):
        op.drop_column('formularios_ingreso', 'tipo_alimentacion')
    if column_exists('formularios_ingreso', 'condicion_medica_bebe'):
        op.drop_column('formularios_ingreso', 'condicion_medica_bebe')


# Función auxiliar para verificar si una columna existe
def column_exists(table_name, column_name):
    from sqlalchemy import inspect
    inspector = inspect(op.get_bind())
    columns = inspector.get_columns(table_name)
    return any(c['name'] == column_name for c in columns)
