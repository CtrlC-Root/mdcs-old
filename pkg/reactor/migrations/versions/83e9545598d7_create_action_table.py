"""create action table

Revision ID: 83e9545598d7
Revises:
Create Date: 2018-06-23 21:05:26.725647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83e9545598d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'action',
        sa.Column('uuid', sa.String(22), nullable=False, primary_key=True),
        sa.Column('title', sa.String(64), nullable=False, unique=True),
        sa.Column('content', sa.Text(), nullable=False))

    op.create_table(
        'task',
        sa.Column('uuid', sa.String(22), nullable=False, primary_key=True),
        sa.Column('action_uuid', sa.String(22), sa.ForeignKey('action.uuid')),
        sa.Column('created', sa.DateTime()))


def downgrade():
    op.drop_table('task')
    op.drop_table('action')
