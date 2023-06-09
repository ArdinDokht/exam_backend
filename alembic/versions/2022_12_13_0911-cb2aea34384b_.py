"""empty message

Revision ID: cb2aea34384b
Revises: b3bdfd727e53
Create Date: 2022-12-13 09:11:09.202205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb2aea34384b'
down_revision = 'b3bdfd727e53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question_question', 'answer_text',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question_question', 'answer_text',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
