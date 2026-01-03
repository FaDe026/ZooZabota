"""merge 8c1c and dd44

Revision ID: 8409cdc361c9
Revises: 1856a5ff3459, 695b1916bdb6
Create Date: 2026-01-03 03:16:33.502024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8409cdc361c9'
down_revision: Union[str, None] = ('1856a5ff3459', '695b1916bdb6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
