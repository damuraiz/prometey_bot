"""add video_and_context

Revision ID: 730a40d8a94d
Revises: 7d693c0df1ee
Create Date: 2020-04-05 02:46:07.548580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '730a40d8a94d'
down_revision = '7d693c0df1ee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('videos',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('url', sa.String(200)),
                    sa.Column('duration', sa.Integer),
                    sa.Column('content_id', sa.Integer, sa.ForeignKey('contents.id'), nullable=False)
                    )

    op.add_column('users', sa.Column('current_content_id', sa.Integer))
    op.create_foreign_key(
        constraint_name="contents_ibfk",
        source_table="users",
        referent_table="contents",
        local_cols=["current_content_id"],
        remote_cols=["id"])


def downgrade():
    #op.drop_index('current_content_id', 'users', type_='foreignkey')
    #op.drop_constraint(None, 'current_content_id', 'users', type_='foreignkey')
    #op.drop_column('users', 'current_content_id')
    op.drop_constraint(constraint_name="contents_ibfk", table_name="users", type_="foreignkey")
    op.drop_column("users", 'current_content_id')
    op.drop_table('videos')
