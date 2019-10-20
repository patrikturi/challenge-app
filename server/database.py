from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

_engine = create_engine('sqlite:///:memory:', convert_unicode=True, echo=True)


_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
session = scoped_session(_session_maker)


def init_db():
    import server.models
    Base.metadata.create_all(bind=_engine)


def drop_tables():
    Base.metadata.drop_all(bind=_engine)
