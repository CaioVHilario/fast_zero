"""Create column updated_at

Revision ID: 0c9139726c47
Revises: 9291b6105587
Create Date: 2026-01-12 14:55:36.886355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c9139726c47'
down_revision: Union[str, Sequence[str], None] = '9291b6105587'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'users', 
        sa.Column(
            'updated_at', 
            sa.DateTime(), 
            server_default=sa.text('(CURRENT_TIMESTAMP)'), 
            nullable=False
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('users', 'updated_at')
