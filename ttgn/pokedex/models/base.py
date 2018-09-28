"""SQLAlchemy model declarative base configuration."""
import inflect
import sqlalchemy
from sqlalchemy.ext import declarative

from ttgn.pokedex.utils import snake_case

engine = inflect.engine()

class Base():
    """Base class for SQLAlchemy declarative base."""
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # pylint: disable=no-self-argument
    @declarative.declared_attr
    def __pluralname__(cls):
        name = snake_case(cls.__name__).rsplit('_', 1)
        name.append(engine.plural(name.pop()))
        return '_'.join(name)

    # pylint: disable=no-self-argument
    @declarative.declared_attr
    def __tablename__(cls):
        """Generate the table name from the full module path of a model
        class."""
        return "{}_{}".format(
            cls.__module__.replace('.', '_'), cls.__pluralname__)


Base = declarative.declarative_base(cls=Base)


class Language(Base):
    """Model representing an IANA language subtag for translation
    identification."""
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    language = sqlalchemy.Column(sqlalchemy.String(3), nullable=False)
    script = sqlalchemy.Column(sqlalchemy.String(8))
    region = sqlalchemy.Column(sqlalchemy.String(2))
    variant = sqlalchemy.Column(sqlalchemy.String(16))
