"""Generations

Revision ID: 763b433aaf4a
Revises:
Create Date: 2018-09-19 12:55:45.996673

"""
import sqlalchemy as sa
from alembic import context, op

from ttgn.pokedex.migrations.data import if_x_argument, load_data_migrations

# revision identifiers, used by Alembic.
revision = '763b433aaf4a'
down_revision = None
branch_labels = ['ttgn.pokedex']
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
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ttgn_pokedex_models_versions_generations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    # ### end Alembic commands ###


def schema_downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ttgn_pokedex_models_versions_generations')
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
