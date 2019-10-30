from sqlalchemy import Column, Integer, String, BigInteger, Date, inspect
from server.database import Base


class CustomBaseMixin:

    def asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        name = self.__class__.__name__
        props = ', '.join([f'{key}={value}' for key, value in sorted(self.asdict().items())])
        return f'<{name}({props})>'


class Challenge(Base, CustomBaseMixin):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)


class Competitor(Base, CustomBaseMixin):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)
    name = Column(String)
    calories = Column(Integer)

    display_name = Column(String)
