"""Add estado column to muestras table

Revision ID: ca7b6e3a5f3f
Revises: 9485245b0fc5
Create Date: 2025-06-11 12:55:43.440717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.models.muestra import EstadoMuestra


# revision identifiers, used by Alembic.
revision: str = 'ca7b6e3a5f3f'
down_revision: Union[str, None] = '9485245b0fc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear el tipo ENUM en PostgreSQL
    estado_enum = sa.Enum(EstadoMuestra, name="estado_muestra")
    estado_enum.create(op.get_bind())  # <-- esto crea el tipo ENUM en la BD

    # Luego agregar la columna
    op.add_column('muestras', sa.Column('estado', estado_enum, nullable=False, server_default='sin_analisis'))


# downgrade
def downgrade():
    # Eliminar la columna primero
    op.drop_column('muestras', 'estado')

    # Luego eliminar el tipo ENUM
    estado_enum = sa.Enum(EstadoMuestra, name="estado_muestra")
    estado_enum.drop(op.get_bind())
