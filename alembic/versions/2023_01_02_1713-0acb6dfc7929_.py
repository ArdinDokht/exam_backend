"""empty message

Revision ID: 0acb6dfc7929
Revises: 9b80d99db10e
Create Date: 2023-01-02 17:13:18.756720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0acb6dfc7929'
down_revision = '9b80d99db10e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_exam_user_unique', 'exam_user_question', ['exam_user_id', 'exam_question_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_exam_user_unique', 'exam_user_question', type_='unique')
    # ### end Alembic commands ###
