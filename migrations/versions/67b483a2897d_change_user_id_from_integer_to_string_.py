"""Change user_id from Integer to String 2nd

Revision ID: 67b483a2897d
Revises: ee3c9ef802e5
Create Date: 2024-08-31 08:55:37.053884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67b483a2897d'
down_revision: Union[str, None] = 'ee3c9ef802e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('pills', 'user_id',
               existing_type=sa.Integer(),
               type_=sa.String(),
               existing_nullable=True)


def downgrade() -> None:
    op.alter_column('pills', 'user_id',
               existing_type=sa.String(),
               type_=sa.Integer(),
               existing_nullable=True)
