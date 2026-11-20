"""add username to users

Revision ID: 5f0013aa4ec8
Revises: d7e3a5b1c9f2
Create Date: 2026-11-20 07:48:02.439219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f0013aa4ec8'
down_revision: Union[str, Sequence[str], None] = 'd7e3a5b1c9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=True))
    op.execute("UPDATE users SET username = LEFT(split_part(email, '@', 1), 50)")
    op.alter_column('users', 'username', nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'username')

