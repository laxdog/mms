"""empty message

Revision ID: 3bea1373e506
Revises: bce5b6fc0787
Create Date: 2017-03-31 20:17:14.122669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bea1373e506'
down_revision = 'bce5b6fc0787'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('membership_plan', sa.Column('price', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('membership_plan', 'price')
    # ### end Alembic commands ###
