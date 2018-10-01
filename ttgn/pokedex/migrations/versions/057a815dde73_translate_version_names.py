"""Translate version names

Revision ID: 057a815dde73
Revises: 1888d425f419
Create Date: 2018-09-30 08:12:50.024412

"""
import sqlalchemy as sa
from alembic import context, op

from ttgn.pokedex.migrations.data import if_x_argument, load_data_migrations
from ttgn.pokedex.migrations.veekun import create_migration_from_veekun

# revision identifiers, used by Alembic.
revision = '057a815dde73'
down_revision = '1888d425f419'
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
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ttgn_pokedex_models_multilang_version_translations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version_id', sa.Integer(), nullable=False),
        sa.Column('local_language_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=False),
        sa.ForeignKeyConstraint(
            ['local_language_id'],
            ['ttgn_pokedex_models_multilang_languages.id'],
        ),
        sa.ForeignKeyConstraint(
            ['version_id'],
            ['ttgn_pokedex_models_versions_versions.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('version_id', 'local_language_id'))
    # ### end Alembic commands ###


def schema_downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ttgn_pokedex_models_multilang_version_translations')
    # ### end Alembic commands ###


def data_upgrade():
    create_migration_from_veekun('version_names', revision,
                                 'versions.VersionTranslation',
                                 _fix_ja_local_language_id)

    try:
        load_data_migrations(revision, 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    load_data_migrations(revision, 'downgrade')


def _fix_ja_local_language_id(row):
    """Bypass the usual mapping of ja-Hrkt."""
    if row['local_language_id'] == '2':
        row['local_language_id'] = '1'

    return row
