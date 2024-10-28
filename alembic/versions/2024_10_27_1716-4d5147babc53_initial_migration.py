"""initial_migration

Revision ID: 4d5147babc53
Revises: 
Create Date: 2024-10-27 17:16:41.307369

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d5147babc53'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('tg_id', sa.BigInteger(), nullable=False),
        sa.Column('fullname', sa.String(), nullable=False),
        sa.Column('username', sa.String(length=32), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('expired_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('tg_id'),
    )
    op.create_table(
        'links',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_marzban_id', sa.UUID(), nullable=False),
        sa.Column('user_tg_id', sa.BigInteger(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_tg_id'],
            ['users.tg_id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_tg_id', 'url'),
    )


def downgrade() -> None:
    op.drop_table('links')
    op.drop_table('users')
