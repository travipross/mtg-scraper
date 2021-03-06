"""add card prices

Revision ID: 17b8de79914a
Revises: 1665e2d7ea5e
Create Date: 2020-03-22 19:29:22.720617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b8de79914a'
down_revision = '1665e2d7ea5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('current_price', sa.Float(), nullable=True))
    op.add_column('card', sa.Column('daily_change', sa.Float(), nullable=True))
    op.add_column('card', sa.Column('highest_price', sa.Float(), nullable=True))
    op.add_column('card', sa.Column('lowest_price', sa.Float(), nullable=True))
    op.add_column('card', sa.Column('time_updated', sa.DateTime(), nullable=True))
    op.add_column('card', sa.Column('weekly_change', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'weekly_change')
    op.drop_column('card', 'time_updated')
    op.drop_column('card', 'lowest_price')
    op.drop_column('card', 'highest_price')
    op.drop_column('card', 'daily_change')
    op.drop_column('card', 'current_price')
    # ### end Alembic commands ###
