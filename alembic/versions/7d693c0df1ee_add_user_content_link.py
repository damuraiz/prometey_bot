"""add user_content_link

Revision ID: 7d693c0df1ee
Revises: 
Create Date: 2020-04-04 21:13:49.861926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d693c0df1ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('contents', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False))


def downgrade():
    op.drop_column('contents', 'user_id')
