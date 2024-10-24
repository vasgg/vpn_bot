"""initial migration

Revision ID: 0fcdf8cc24f8
Revises: 
Create Date: 2024-10-17 17:35:25.368415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0fcdf8cc24f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('fullname', sa.String(), nullable=False),
        sa.Column('username', sa.String(length=32), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id'),
    )
    op.create_table(
        'keys',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('expired_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'key'),
    )


def downgrade() -> None:
    op.drop_table('keys')
    op.drop_table('users')
