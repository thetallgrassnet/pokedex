"""Languages

Revision ID: 088903c1ed2a
Revises: 317f62cffc9a
Create Date: 2018-09-26 15:16:24.522720

"""
import sqlalchemy as sa
from alembic import context, op

from ttgn.pokedex.migrations.data import if_x_argument, load_data_migrations

# revision identifiers, used by Alembic.
revision = '088903c1ed2a'
down_revision = '317f62cffc9a'
branch_labels = None
depends_on = None


def upgrade():
    if not if_x_argument('no-schema', False):
        schema_upgrade()

    if not if_x_argument('no-data', False):
        data_upgrade()


def downgrade():
    if not if_x_argument('no-data', False):
        data_downgrade()

    if not if_x_argument('no-schema', False):
        schema_downgrade()


def schema_upgrade():
    op.create_table(
        'ttgn_pokedex_models_base_language',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('language', sa.String(length=3), nullable=False),
        sa.Column('script', sa.String(length=8), nullable=True),
        sa.Column('region', sa.String(length=2), nullable=True),
        sa.Column('variant', sa.String(length=16), nullable=True),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('order'),
        sa.UniqueConstraint('language', 'script', 'region', 'variant'))


def schema_downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ttgn_pokedex_models_base_language')
    # ### end Alembic commands ###


def data_upgrade():
    try:
        load_data_migrations(revision, 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    load_data_migrations(revision, 'downgrade')
