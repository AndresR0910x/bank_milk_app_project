"""nuevos datos agregados al formulario de ingreso

Revision ID: de988d2a807f
Revises: 
Create Date: 2025-06-06 08:18:34.043351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de988d2a807f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Renombrar columnas existentes
    op.alter_column('formularios_ingreso', 'fecha_nacimiento', new_column_name='fecha_parto')
    op.alter_column('formularios_ingreso', 'semanas_del_parto', new_column_name='semanas_gestacion')

    # Modificar tipo de dato de numero_de_parto (Integer -> String)
    op.alter_column('formularios_ingreso', 'numero_de_parto', type_=sa.String(), existing_type=sa.Integer())

    # Eliminar columna obsoleta
    op.drop_column('formularios_ingreso', 'tamaño')

    # Agregar nuevas columnas
    op.add_column('formularios_ingreso', sa.Column('tipo_parto', sa.String(), nullable=False, server_default="natural"))
    op.add_column('formularios_ingreso', sa.Column('condiciones_medicas', sa.String(), nullable=True))
    op.add_column('formularios_ingreso', sa.Column('uso_medicamentos', sa.String(), nullable=True))
    op.add_column('formularios_ingreso', sa.Column('consumo_sustancias', sa.String(), nullable=True))
    op.add_column('formularios_ingreso', sa.Column('alergias', sa.String(), nullable=True))
    op.add_column('formularios_ingreso', sa.Column('enfermedades_relevantes', sa.String(), nullable=True))
    op.add_column('formularios_ingreso', sa.Column('estatura', sa.Integer(), nullable=False, server_default="0"))
    op.add_column('formularios_ingreso', sa.Column('edad_gestacional_nacimiento', sa.Integer(), nullable=False, server_default="0"))
    op.add_column('formularios_ingreso', sa.Column('tipo_alimentacion', sa.String(), nullable=False, server_default="Lactancia exclusiva"))
    op.add_column('formularios_ingreso', sa.Column('condicion_medica_bebe', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir la adición de nuevas columnas
    op.drop_column('formularios_ingreso', 'condicion_medica_bebe')
    op.drop_column('formularios_ingreso', 'tipo_alimentacion')
    op.drop_column('formularios_ingreso', 'edad_gestacional_nacimiento')
    op.drop_column('formularios_ingreso', 'estatura')
    op.drop_column('formularios_ingreso', 'enfermedades_relevantes')
    op.drop_column('formularios_ingreso', 'alergias')
    op.drop_column('formularios_ingreso', 'consumo_sustancias')
    op.drop_column('formularios_ingreso', 'uso_medicamentos')
    op.drop_column('formularios_ingreso', 'condiciones_medicas')
    op.drop_column('formularios_ingreso', 'tipo_parto')

    # Restaurar columna eliminada
    op.add_column('formularios_ingreso', sa.Column('tamaño', sa.Integer(), nullable=False, server_default="0"))

    # Revertir cambio de tipo de dato de numero_de_parto (String -> Integer)
    op.alter_column('formularios_ingreso', 'numero_de_parto', type_=sa.Integer(), existing_type=sa.String())

    # Revertir renombramiento de columnas
    op.alter_column('formularios_ingreso', 'semanas_gestacion', new_column_name='semanas_del_parto')
    op.alter_column('formularios_ingreso', 'fecha_parto', new_column_name='fecha_nacimiento')