"""empty message

Revision ID: db90585b69f1
Revises: ae51781af4dc
Create Date: 2022-12-24 12:56:48.385572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db90585b69f1'
down_revision = 'ae51781af4dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education_system_school',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_agency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('education_system_class_room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['education_system_school.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.Column('agency_id', sa.Integer(), nullable=False),
    sa.Column('classroom_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agency_id'], ['user_agency.id'], ),
    sa.ForeignKeyConstraint(['classroom_id'], ['education_system_class_room.id'], ),
    sa.ForeignKeyConstraint(['grade_id'], ['education_system_grade.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_user')
    op.drop_table('education_system_class_room')
    op.drop_table('user_agency')
    op.drop_table('education_system_school')
    # ### end Alembic commands ###
