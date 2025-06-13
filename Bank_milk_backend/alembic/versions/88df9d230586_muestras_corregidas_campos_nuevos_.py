"""muestras corregidas campos nuevos agregados

Revision ID: 88df9d230586
Revises: 50fc5851bbff
Create Date: 2025-06-06 11:10:15.753404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88df9d230586'
down_revision: Union[str, None] = '50fc5851bbff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('muestras', sa.Column('metodo_extraccion', sa.Enum('manual', 'electrico', 'mixto', name='metodoextraccion'), nullable=False))
    op.add_column('muestras', sa.Column('medicamentos_hoy', sa.Enum('si', 'no', name='respuestasino'), nullable=False))
    op.add_column('muestras', sa.Column('condicion_salud_hoy', sa.Enum('si', 'no', name='respuestasino'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    pass
