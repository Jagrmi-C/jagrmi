"""Added persons table

Revision ID: 742c4f1aaab1
Revises: 
Create Date: 2019-08-31 02:44:12.443192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '742c4f1aaab1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('birthdate', sa.String(length=50), nullable=True),
    sa.Column('birthplace', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_table('person_table')
    # ### end Alembic commands ###
