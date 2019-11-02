from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

echo = False

Base = declarative_base()

_engine = create_engine('sqlite:///:memory:', convert_unicode=True, echo=echo)


_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
session = scoped_session(_session_maker)


def init_db():
    Base.metadata.create_all(bind=_engine)


def drop_tables():
    Base.metadata.drop_all(bind=_engine)
