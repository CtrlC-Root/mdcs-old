"""initial schema

Revision ID: f3f458260b8b
Revises:
Create Date: 2019-01-06 15:03:41.223165

"""
from alembic import op
import sqlalchemy as sa

from mdcs_remote.models import ConfigType, ControlType, TaskState


# revision identifiers, used by Alembic.
revision = 'f3f458260b8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'controlset',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('name', sa.String(32), unique=True, nullable=False),
        sa.Column('description', sa.String(64), nullable=False),
        sa.Column('config_type', sa.Enum(ConfigType), nullable=False),
        sa.Column('config', sa.Text(), nullable=False))

    op.create_table(
        'control',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('controlset_uuid', sa.String(22), sa.ForeignKey('controlset.uuid'), nullable=False),
        sa.Column('type', sa.Enum(ControlType), nullable=False),
        sa.Column('description', sa.String(64), nullable=False))

    op.create_table(
        'task',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('controlset_uuid', sa.String(22), sa.ForeignKey('controlset.uuid'), nullable=False),
        sa.Column('state', sa.Enum(TaskState), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.Column('input', sa.JSON(), nullable=False),
        sa.Column('output', sa.JSON(), nullable=False))

    op.create_table(
        'button_control',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('control_uuid', sa.String(22), sa.ForeignKey('control.uuid'), nullable=False),
        sa.Column('title', sa.String(16), nullable=False))

    op.create_table(
        'color_control',
        sa.Column('uuid', sa.String(22), primary_key=True, nullable=False),
        sa.Column('control_uuid', sa.String(22), sa.ForeignKey('control.uuid'), nullable=False))


def downgrade():
    op.drop_table('color_control')
    op.drop_table('button_control')

    op.drop_table('task')
    op.drop_table('control')
    op.drop_table('controlset')
