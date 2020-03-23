"""add purchase price

Revision ID: 5b87cd933ee0
Revises: 17b8de79914a
Create Date: 2020-03-22 19:48:53.049760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b87cd933ee0'
down_revision = '17b8de79914a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('purchase_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'purchase_price')
    # ### end Alembic commands ###
