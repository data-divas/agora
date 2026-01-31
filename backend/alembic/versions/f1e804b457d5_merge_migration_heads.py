"""merge migration heads

Revision ID: f1e804b457d5
Revises: b758169dd143
Create Date: 2026-01-31 14:49:09.533515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e804b457d5'
down_revision: Union[str, Sequence[str], None] = 'b758169dd143'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
