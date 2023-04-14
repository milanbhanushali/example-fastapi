"""Add Content Column To Post Table

Revision ID: da76e799203f
Revises: da1ec22be116
Create Date: 2023-04-14 16:04:23.632756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da76e799203f'
down_revision = 'da1ec22be116'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
