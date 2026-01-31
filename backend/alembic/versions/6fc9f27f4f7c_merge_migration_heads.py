"""merge migration heads

Revision ID: 6fc9f27f4f7c
Revises: 1cadf5eea9b8, bd2f8882c5ba
Create Date: 2026-01-31 14:43:51.120379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fc9f27f4f7c'
down_revision: Union[str, Sequence[str], None] = ('1cadf5eea9b8', 'bd2f8882c5ba')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
