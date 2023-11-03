"""add content column to posts table

Revision ID: c70b126a6f6c
Revises: 7e6b23cd3cec
Create Date: 2023-11-03 14:00:50.569338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c70b126a6f6c'
down_revision: Union[str, None] = '7e6b23cd3cec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
