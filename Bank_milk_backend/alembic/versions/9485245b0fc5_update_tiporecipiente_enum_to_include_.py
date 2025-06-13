"""Update tiporecipiente enum to include plastico_sin_bpa

Revision ID: 9485245b0fc5
Revises: 88df9d230586
Create Date: 2025-06-09 17:54:08.436930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '9485245b0fc5'
down_revision: Union[str, None] = '88df9d230586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('DROP TYPE IF EXISTS tiporecipiente CASCADE')
    tiporecipiente = sa.Enum('vidrio', 'plastico_sin_bpa', 'bolsa', name='tiporecipiente')
    tiporecipiente.create(op.get_bind())
    op.alter_column('muestras', 'tipo_de_recipiente',
                    existing_type=sa.Enum('vidrio', 'plastico_sin_bpa', 'bolsa', name='tiporecipiente'),
                    type_=sa.Enum('vidrio', 'plastico_sin_bpa', 'bolsa', name='tiporecipiente'),
                    postgresql_using='tipo_de_recipiente::text::tiporecipiente')

def downgrade() -> None:
    op.execute('DROP TYPE tiporecipiente')
    old_tiporecipiente = sa.Enum('vidrio', 'plastico', 'bolsa', name='tiporecipiente')
    old_tiporecipiente.create(op.get_bind())
    op.alter_column('muestras', 'tipo_de_recipiente',
                    existing_type=sa.Enum('vidrio', 'plastico_sin_bpa', 'bolsa', name='tiporecipiente'),
                    type_=sa.Enum('vidrio', 'plastico', 'bolsa', name='tiporecipiente'),
                    postgresql_using='tipo_de_recipiente::text::tiporecipiente')