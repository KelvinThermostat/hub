from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./kelvin/data/kelvin.db'
Engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
Session = sessionmaker(Engine)
Base = declarative_base()


def create():
    """Initialize database structure."""
    Base.metadata.create_all(Engine)


def drop():
    """Destroy database structure."""
    Base.metadata.drop_all(Engine)
