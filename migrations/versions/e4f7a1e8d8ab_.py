"""empty message

Revision ID: e4f7a1e8d8ab
Revises: 2393fcb920e1
Create Date: 2022-08-13 14:45:47.197376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f7a1e8d8ab'
down_revision = '2393fcb920e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('artists', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'genres',
               existing_type=sa.VARCHAR(length=180),
               nullable=True)
    op.alter_column('venues', 'website_link',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('venues', 'website_link',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('venues', 'genres',
               existing_type=sa.VARCHAR(length=180),
               nullable=False)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('artists', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###