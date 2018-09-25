"""Handles database connection and session management for Pokédex instances."""
import logging
import os
from contextlib import contextmanager

import pkg_resources

from alembic import command, config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DATABASE_URI = 'sqlite:///{}'.format(
    pkg_resources.resource_filename(__name__, 'pokedex.sqlite3'))


class Pokedex:
    """Wrapper for the SQLAlchemy database engine and session object."""

    def __init__(self,
                 engine_or_uri=DEFAULT_DATABASE_URI,
                 migrate=True,
                 alembic_cfg=None,
                 debug=False):
        """Initialize the database if necessary, and create the engine.

        Args:
            engine_or_uri (str|sqlalchemy.engine.Engine): Existing SQLAlchemy
                engine or database connection string to use. Defaults to an on-
                disk SQLite database ``pokedex.sqlite3`` in the root directory
                of the ``ttgn.pokedex`` package.
            migrate (bool): If True, automatically run database migrations on
                instantiation.
            alembic_cfg (alembic.config.Config): Existing Alembic configuration
                to use for running migrations. Must include the Pokédex
                migrations in its ``versions_location``.
            debug (bool): If True, output detailed SQLAlchemy debug logging.
                Mostly for development, and only used if an existing engine
                was not passed in with the ``engine`` parameter.
        """
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if isinstance(engine_or_uri, Engine):
            engine = engine_or_uri
        else:
            self.logger.info(
                'Using Pokédex database at {}'.format(engine_or_uri))
            engine = create_engine(engine_or_uri, echo=self.debug)

        self._Session = sessionmaker(bind=engine)

        if migrate:
            if alembic_cfg is None:
                alembic_cfg = config.Config(
                    pkg_resources.resource_filename(__name__, 'alembic.ini'))

            alembic_cfg.attributes['connectable'] = engine

            self.logger.debug('Running migrations')
            command.upgrade(alembic_cfg, 'ttgn.pokedex@head')

    def query(self, *args, **kwargs):
        """Perform a single query against the database."""
        with self.session_scope() as session:
            return session.query(*args, **kwargs)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of database operations.

        This method should only be used in advanced cases where a series of
        operations need to be treated as a discrete transaction, e.g. running
        multiple select queries in building a single HTTP response."""
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
