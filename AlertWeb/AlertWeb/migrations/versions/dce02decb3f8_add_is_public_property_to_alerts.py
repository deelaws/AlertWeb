"""Add is_public property to Alerts

Revision ID: dce02decb3f8
Revises: 
Create Date: 2016-09-18 19:42:42.902042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dce02decb3f8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rescue_alert', sa.Column('is_public', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rescue_alert', 'is_public')
    ### end Alembic commands ###
