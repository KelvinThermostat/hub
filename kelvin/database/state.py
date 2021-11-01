from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import String

from . import Base, Session


class State(Base):
    __tablename__ = 'state'

    key: str = Column(String, primary_key=True, unique=True, nullable=False)
    value: str = Column(String, nullable=False)
    date_modified: datetime = Column(DateTime,
                                     onupdate=func.current_timestamp())

    @staticmethod
    def get(key: str, default: None):
        item = Session().query(State).filter_by(key=key).first()

        if item:
            return item.value
        else:
            return default

    @staticmethod
    def save(key: str, value: object):
        session = Session()
        item = session.query(State).filter_by(key=key).first()

        if not item:
            item = State()
            item.key = key

        item.value = value

        session.add(item)
        session.commit()
