"""user_image

Revision ID: 0c4931255aef
Revises: ad06ee692a42
Create Date: 2022-02-04 18:20:46.432416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4931255aef'
down_revision = 'ad06ee692a42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###