"""
Create action table.

Revision ID: d0930a2c149c
Revises:
Create Date: 2018-06-08 20:23:29.814577
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0930a2c149c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'action',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False))


def downgrade():
    op.drop_table('action')
