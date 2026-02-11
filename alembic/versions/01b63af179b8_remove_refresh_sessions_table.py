"""remove refresh_sessions table

Revision ID: 01b63af179b8
Revises: 56761f108a31
Create Date: 2026-02-11 01:02:27.274626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01b63af179b8'
down_revision: Union[str, Sequence[str], None] = '56761f108a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('refresh_sessions')
