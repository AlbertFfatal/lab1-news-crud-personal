"""add auth fields and refresh sessions

Revision ID: 56761f108a31
Revises: ff6aacbaa7d2
Create Date: 2026-02-09 22:27:27.640977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56761f108a31'
down_revision: Union[str, Sequence[str], None] = 'ff6aacbaa7d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

def upgrade():
    # Добавляем поля в users
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('users', sa.Column('password_hash', sa.String(), nullable=True))

    # Создаём таблицу refresh_sessions
    op.create_table('refresh_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('refresh_token'),
        sa.Index('ix_refresh_sessions_refresh_token', 'refresh_token')
    )

    # Мок-админ (обновляем первого verified пользователя)
    op.execute("UPDATE users SET is_admin = true WHERE id = 1")

def downgrade():
    op.drop_table('refresh_sessions')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'is_admin')