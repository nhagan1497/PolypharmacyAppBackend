"""user_id to string

Revision ID: 04698043c694
Revises: 67b483a2897d
Create Date: 2024-08-31 10:03:22.562410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04698043c694'
down_revision: Union[str, None] = '67b483a2897d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('pill_consumptions', 'user_id',
               existing_type=sa.Integer(),
               type_=sa.String(),
               existing_nullable=True)

    op.alter_column('pill_schedules', 'user_id',
                    existing_type=sa.Integer(),
                    type_=sa.String(),
                    existing_nullable=True)

    op.drop_table('users')
    # Recreate the 'users' table with 'uid' as a string
    op.create_table(
        'users',
        sa.Column('uid', sa.String(255), primary_key=True),
        sa.Column('name', sa.String(), nullable=True)
    )

def downgrade() -> None:
    op.alter_column('pill_consumptions', 'user_id',
               existing_type=sa.String(),
               type_=sa.Integer(),
               existing_nullable=True)

    op.alter_column('pill_schedules', 'user_id',
                    existing_type=sa.String(),
                    type_=sa.Integer(),
                    existing_nullable=True)

    op.drop_table('users')
    # Recreate the 'users' table with 'uid' as a string
    op.create_table(
        'users',
        sa.Column('uid', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True)
    )
