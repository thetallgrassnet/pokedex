"""Version Groups and Versions

Revision ID: 317f62cffc9a
Revises: 763b433aaf4a
Create Date: 2018-09-20 07:27:20.649971

"""
from alembic import context, op
import sqlalchemy as sa
import ttgn.pokedex.utils


# revision identifiers, used by Alembic.
revision = '317f62cffc9a'
down_revision = '763b433aaf4a'
branch_labels = None
depends_on = None


def upgrade():
    if not ttgn.pokedex.utils.if_x_argument('no-schema', False):
        schema_upgrade()

    if not ttgn.pokedex.utils.if_x_argument('no-data', False):
        data_upgrade()


def downgrade():
    if not ttgn.pokedex.utils.if_x_argument('no-data', False):
        data_downgrade()

    if not ttgn.pokedex.utils.if_x_argument('no-schema', False):
        schema_downgrade()


def schema_upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ttgn_pokedex_models_versions_version_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['generation_id'], ['ttgn_pokedex_models_versions_generation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ttgn_pokedex_models_versions_version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('version_group_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('acronym', sa.String(length=2), nullable=False),
    sa.ForeignKeyConstraint(['version_group_id'], ['ttgn_pokedex_models_versions_version_group.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('acronym'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def schema_downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ttgn_pokedex_models_versions_version')
    op.drop_table('ttgn_pokedex_models_versions_version_group')
    # ### end Alembic commands ###


def data_upgrade():
    try:
        ttgn.pokedex.utils.load_data_migration_if_exists('317f62cffc9a', 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    ttgn.pokedex.utils.load_data_migration_if_exists('317f62cffc9a', 'downgrade')