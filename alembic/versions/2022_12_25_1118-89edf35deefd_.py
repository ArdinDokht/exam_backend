"""empty message

Revision ID: 89edf35deefd
Revises: 1d0f30f1bced
Create Date: 2022-12-25 11:18:30.483877

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '89edf35deefd'
down_revision = '1d0f30f1bced'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exam_question', sa.Column('negative_score', sa.Float(), nullable=False, server_default='0'))
    op.alter_column('exam_question', 'score',
                    existing_type=sa.INTEGER(),
                    type_=sa.Float(),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exam_question', 'score',
                    existing_type=sa.Float(),
                    type_=sa.INTEGER(),
                    existing_nullable=False)
    op.drop_column('exam_question', 'negative_score')
    # ### end Alembic commands ###
