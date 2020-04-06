"""add video_status_column

Revision ID: e2f9b72401c4
Revises: 730a40d8a94d
Create Date: 2020-04-06 20:32:51.127022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f9b72401c4'
down_revision = '730a40d8a94d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('videos', sa.Column('status', sa.String(10), nullable = False, server_default = 'NEW'))


def downgrade():
    op.drop_column('videos', 'status')
