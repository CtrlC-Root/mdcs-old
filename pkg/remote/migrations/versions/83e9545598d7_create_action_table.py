"""create action table

Revision ID: 83e9545598d7
Revises:
Create Date: 2018-06-23 21:05:26.725647

"""
from alembic import op
import sqlalchemy as sa

from mdcs_remote.models.task import TaskState


# revision identifiers, used by Alembic.
revision = '83e9545598d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'action',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('title', sa.String(32), unique=True, nullable=False),
        sa.Column('description', sa.String(64), nullable=False),
        sa.Column('content', sa.Text(), nullable=False))

    op.create_table(
        'task',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('action_uuid', sa.String(22), sa.ForeignKey('action.uuid'), nullable=False),
        sa.Column('state', sa.Enum(TaskState), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.Column('output', sa.Text(), nullable=False))


def downgrade():
    op.drop_table('task')
    op.drop_table('action')
