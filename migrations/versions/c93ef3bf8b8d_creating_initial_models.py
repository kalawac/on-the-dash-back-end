"""creating initial models

Revision ID: c93ef3bf8b8d
Revises: 
Create Date: 2023-02-08 14:22:26.031056

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c93ef3bf8b8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('lname', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Enum('FEMALE', 'MALE', 'NONBINARY', 'OTHER', 'UNKNOWN', name='gender'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('event_type', sa.Enum('CONF_FORUM', 'MEETING', 'TA', 'TRAINING', 'OTHER', name='eventtype'), nullable=True),
    sa.Column('subjects', sa.Enum('CONF_FORUM', 'MEETING', 'TA', 'TRAINING', 'OTHER', name='eventtype'), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('indicator',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('org_sector', sa.Enum('ACADEMIA', 'NGO', 'GOVT', 'MEDIA', 'BUSINESS', 'CSR', 'SOC_ENT', 'IDP', 'OTHER', name='orgsector'), nullable=True),
    sa.Column('work_focus', sa.Enum('INDIGENOUS', 'LGBTI', 'RELIGIOUS_FREEDOM', 'WOMENS_RIGHTS', 'OTHER', name='wf'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('org')
    op.drop_table('indicator')
    op.drop_table('event')
    op.drop_table('contact')
    # ### end Alembic commands ###