"""peso y estaturacorregidos

Revision ID: 50fc5851bbff
Revises: 40c589ffbc23
Create Date: 2025-06-06 10:27:00.099083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50fc5851bbff'
down_revision: Union[str, None] = '40c589ffbc23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'formularios_ingreso', 'peso',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column(
        'formularios_ingreso', 'estatura',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False
    )

def downgrade() -> None:
    op.alter_column(
        'formularios_ingreso', 'peso',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False
    )
    op.alter_column(
        'formularios_ingreso', 'estatura',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False
    )
