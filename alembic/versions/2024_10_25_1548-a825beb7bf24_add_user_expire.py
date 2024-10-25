"""add_user_expire

Revision ID: a825beb7bf24
Revises: 0fcdf8cc24f8
Create Date: 2024-10-25 15:48:13.736933

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a825beb7bf24'
down_revision: Union[str, None] = '0fcdf8cc24f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('expired_at', sa.DateTime(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'expired_at')
