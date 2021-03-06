"""Added google table

Revision ID: d5f849fcb806
Revises: 742c4f1aaab1
Create Date: 2019-09-07 17:06:52.656603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f849fcb806'
down_revision = '742c4f1aaab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_google',
    sa.Column('google_id', sa.String(length=50), nullable=False),
    sa.Column('google_user', sa.String(length=50), nullable=True),
    sa.Column('google_email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('google_id')
    )
    op.add_column('person_table', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('person_table', 'birthdate')
    op.drop_column('person_table', 'birthplace')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person_table', sa.Column('birthplace', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('person_table', sa.Column('birthdate', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('person_table', 'is_active')
    op.drop_table('user_google')
    # ### end Alembic commands ###
