"""create votes table

Revision ID: 9e5b5b26eb7a
Revises: 70ba45e3eac2
Create Date: 2023-01-22 13:48:45.270829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e5b5b26eb7a'
down_revision = '70ba45e3eac2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'votes',
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    )

def downgrade():
    op.drop_table('votes')
